# -*- coding: utf-8 -*-
import json
import os
from typing import List

import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv
from inspect_ai import Task, task
from pydantic import BaseModel, Field

from persona_evaluation.tooling.prompts import persona_keys
from persona_evaluation.tooling.scorer import model_critique
from persona_evaluation.tooling.solver import (
    generate_and_validate,
    mode,
    modes,
    prompt_template_from_metadata,
)
from persona_evaluation.tooling.utils import create_sample

load_dotenv()

# load our filtered prism dataset
prism_dataset = load_dataset("RLAIF/PRISM-filter")

# load our personas dataset. TODO make public
splits = {
    "train": "data/train-00000-of-00001.parquet",
    "test": "data/test-00000-of-00001.parquet",
}
df = pd.read_parquet("hf://datasets/RLAIF/Synthetic-Personas-Final/" + splits["train"])

# in Sample, input is "question" from prism_dataset and metadata is an entire row (expressed as a json string) from personas_dataset


class LooAttributes(BaseModel):
    attributes: List[str] = Field(..., description="The attributes to leave out")


# load the loo attributes
with open(os.getenv("LOO_ATTRIBUTES"), "r") as f:
    loo_attributes = json.load(f)
loo_attributes = LooAttributes(**loo_attributes).attributes

for attribute in loo_attributes:
    # make sure its in persona_keys
    if attribute not in persona_keys:
        raise ValueError(
            f"Attribute {attribute} not found in persona_keys. Available keys are {persona_keys}"
        )


def create_loo_sample(prism_row, personas_row):
    """
    Takes a row from prism, which denotes a question, and a row from personas, which denotes a demographic
    Takes the persona and permutes over the attributes constructing a number of question LOO papers
    """
    persona_idx = personas_row[0]
    persona = personas_row[1]

    # drop the attributes to form the baseline persona
    baseline = persona.copy().drop(loo_attributes)

    loo_personas = [(persona_idx, baseline)]
    for attribute in loo_attributes:
        try:
            loo_persona = persona.copy().drop(attribute)
        except KeyError:
            raise ValueError(
                f"Attribute {attribute} not found in persona {persona_idx}"
            )

        # attribute is a column in personas row, we can drop that column
        loo_personas.append((persona_idx, loo_persona))

    return [create_sample(prism_row, loo_persona) for loo_persona in loo_personas]


# create samples from prism_dataset['train']
# take the first 100 of prism. make sure its still a HF dataset
prism_dataset["train"] = prism_dataset["train"].select(range(30))
df = df.head(30)

dataset = [
    create_loo_sample(prism_row, persona)
    for prism_row, persona in zip(prism_dataset["train"], df.iterrows())
]

# flatten the list
dataset = [sample for sublist in dataset for sample in sublist]


@task
def prism_personalization():
    return Task(
        dataset=dataset,
        plan=[
            prompt_template_from_metadata(
                modes[mode]["system_prompt"], modes[mode]["format"]
            ),
            generate_and_validate(),
        ],  # TODO better plan
        scorer=model_critique(),
    )
