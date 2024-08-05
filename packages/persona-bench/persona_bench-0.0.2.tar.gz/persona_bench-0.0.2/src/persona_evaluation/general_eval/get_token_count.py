# -*- coding: utf-8 -*-


import argparse

from persona_evaluation.tooling.utils import get_token_count_over_log


def setup_args():
    parser = argparse.ArgumentParser(
        description="Get the token count for a given model"
    )
    parser.add_argument("--mode", type=str, help="The text to encode")
    return parser.parse_args()


if __name__ == "__main__":
    args = setup_args()
    # load the json

    models = ["gpt-3.5", "gpt-4", "gpt-4o", "llama-370b"]
    for model in models:
        print(f"Model: {model}")

        token_counts = get_token_count_over_log(model, args.mode)

        print(f"Input token count: {token_counts['input']}")
        print(f"Output token count: {token_counts['output']}")
