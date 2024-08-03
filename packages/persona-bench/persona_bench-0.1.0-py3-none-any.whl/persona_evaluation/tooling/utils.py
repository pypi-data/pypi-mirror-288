# -*- coding: utf-8 -*-
import json
import logging
import re
from typing import List

from inspect_ai.dataset import Sample
from pydantic import BaseModel, Field, ValidationError

from persona_evaluation.tooling.prompts import persona_keys


def create_sample(prism_row, personas_row, extra_metadata=None):
    if isinstance(personas_row, tuple):
        personas_idx = personas_row[0]
        personas_row = personas_row[1]

    metadata = {
        "persona": personas_row.to_dict(),
        "_persona_idx": personas_idx,
    }
    metadata.update(extra_metadata or {})

    return Sample(
        input=prism_row["question"],
        metadata=metadata,
    )


def convert_to_dict(pandas_row_str):

    # If the input is already a dictionary, return it
    if isinstance(pandas_row_str, dict):
        return pandas_row_str

    # Split the string into lines
    lines = pandas_row_str.strip().split("\n")

    # Initialize an empty dictionary
    result_dict = {}

    # Process each line to extract key-value pairs
    for line in lines:
        # Use regular expression to handle keys and values with spaces
        parts = re.split(r"\s{2,}", line.strip(), maxsplit=1)
        if len(parts) == 2:
            key, value = parts
            result_dict[key.strip()] = value.strip()
        else:
            # Handle lines that do not split into exactly two parts
            continue

    return result_dict


def validate_attribute_str(attribute: str):
    """
    Validates that the attribute is in the persona keys
    """
    if attribute not in persona_keys:
        raise ValidationError(
            f"Attribute {attribute} not in persona keys. Please use one of {persona_keys}"
        )


class AttributeValues(BaseModel):
    attribute: str = Field(str, description="Attribute to filter on")
    values: List[str] = Field(list[str], description="Values to filter on")


class Intersection(BaseModel):
    attributes: List[AttributeValues] = Field(
        list[AttributeValues],
        description="List of attributes and their values to filter on",
    )


# load and validate the json file
def load_intersections(path):
    with open(path) as f:
        intersections = f.read()
    try:
        objs = json.loads(intersections)
        assert isinstance(objs, list)
        intersections = [Intersection(**x) for x in objs]
    except ValidationError as e:
        raise ValueError(f"Error validating intersections: {e}")

    return intersections


try:
    import tiktoken
    from transformers import AutoTokenizer

    # get the llama 3 tokenizer
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-70B")
    enc = tiktoken.get_encoding("o200k_base")

    gpt4o = tiktoken.encoding_for_model("gpt-4o")
    gpt4 = tiktoken.encoding_for_model("gpt-4-turbo")
    gpt35 = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokenizers = {
        "gpt-4o": gpt4o,
        "gpt-4": gpt4,
        "gpt-3.5": gpt35,
        "llama-370b": tokenizer,
    }

    def get_token_count(text: str, model: str):
        """
        Get the token count for a given model

        Args:
        text : str : the text to encode
        model : str : the model to encode with

        Returns:
        int : the token count
        """

        if model == "llama_3":
            return len(tokenizers["llama3"](text)["input_ids"])

        else:
            return len(tokenizers[model].encode(text))

    def get_file_name(mode: str, model: str):
        return f"logs/{model}_{mode}.json"

    def get_token_count_over_log(model, mode):
        with open(get_file_name(mode, model)) as f:
            data = json.load(f)

        # first, get all the input messages
        samples = data["samples"]
        input_count = 0
        output_count = 0
        for sample in samples:
            messages = sample["messages"]

            for message in messages[:-1]:
                input_count += get_token_count(message["content"], model)

            output_count += get_token_count(messages[-1]["content"], model)

            metadata = sample["metadata"]
            if "pydantic_output" in metadata:
                for k, v in metadata["pydantic_output"].items():
                    output_count += get_token_count(v, model)

        return {"input": input_count, "output": output_count}

except Exception as e:
    logging.warning("Unable to load tiktoken, token count functions will not work")
