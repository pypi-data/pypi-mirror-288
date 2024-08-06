import json
from functools import wraps
from time import time
from typing import Callable, List

import attrs
import click
import requests
from openai import OpenAI
from tqdm import tqdm
from vals.cli.suite import pull_suite, update_suite
from vals.sdk.auth import _get_auth_token
from vals.sdk.run import get_run_url, start_run
from vals.sdk.util import be_host

in_tokens = 0
out_tokens = 0


def parse_test_suite_id_from_url(test_suite_url: str) -> str:
    start_index = test_suite_url.find("test_suite_id=") + len("test_suite_id=")
    return test_suite_url[start_index:]


def read_file(file_id: str):
    response = requests.post(
        url=f"{be_host()}/read_file_text/?file_id={file_id}",
        headers={"Authorization": _get_auth_token()},
    )
    return response.text


def run_evaluations(
    test_suite_url: str,
    generate_fn: Callable[[str], str],
    description="Ran automatically using the PRL SDK",
    maximum_threads=4,
    verbosity=1,
    model_under_test="sdk",
    **kwargs,
):
    test_suite_id = parse_test_suite_id_from_url(test_suite_url)

    suite_data = pull_suite(test_suite_id, include_id=True)

    if verbosity == 0:
        iterator = suite_data["tests"]
    else:
        iterator = tqdm(suite_data["tests"])

    global in_tokens, out_tokens
    metadata = {}

    uses_files = False
    for test in suite_data["tests"]:
        if "file_id" in test and test["file_id"] is not None:
            uses_files = True

    uses_file_uids = False
    for test in suite_data["tests"]:
        if (
            "file_uids" in test
            and test["file_uids"] is not None
            and len(test["file_uids"]) > 0
        ):
            uses_file_uids = True

    for test in iterator:
        start = time()

        if uses_files:
            if "file_id" in test and test["file_id"] is not None:
                file_id = test["file_id"]
                kwargs["file_text"] = read_file(file_id)
            else:
                kwargs["file_text"] = ""

        if uses_file_uids:
            if "file_uids" in test and test["file_uids"] is not None:
                file_uids = test["file_uids"]
                kwargs["file_uids"] = file_uids
            else:
                kwargs["file_uids"] = []

        fixed_output = generate_fn(test["input_under_test"], **kwargs)
        test["fixed_output"] = fixed_output

        end = time()
        metadata[test["id"]] = {
            "in_tokens": in_tokens,
            "out_tokens": out_tokens,
            "duration_seconds": end - start,
        }
        in_tokens = 0
        out_tokens = 0

    update_suite(test_suite_id, suite_data)
    run_id = start_run(
        test_suite_id,
        {
            "use_fixed_output": True,
            "description": description,
            "maximum_threads": maximum_threads,
            "model_under_test": model_under_test,
            **kwargs,
        },
        metadata_map=metadata,
    )
    run_url = get_run_url(run_id)

    if verbosity >= 1:
        click.secho(
            "Successfully updated test suite with new fixed outputs and started a new run.",
            fg="green",
        )
        click.secho(run_url, bold=True)

    return run_id


def wrap_chatcompletion(func: Callable):
    @wraps(func)
    def wrapper(**kwargs):
        response = func(**kwargs)
        global in_tokens, out_tokens

        in_tokens += response.usage.prompt_tokens
        out_tokens += response.usage.completion_tokens

        return response

    return wrapper


# External Facing
def patch(client: OpenAI):
    client.chat.completions.create = wrap_chatcompletion(client.chat.completions.create)
    return client
