# -*- coding: utf-8 -*-
import os

import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv
from inspect_ai import Task, task

from persona_evaluation.tooling.scorer import model_critique
from persona_evaluation.tooling.solver import (
    generate_and_validate,
    mode,
    modes,
    prompt_template_from_metadata,
)
from persona_evaluation.tooling.utils import create_sample

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # todo

# load our filtered prism dataset
prism_dataset = load_dataset("RLAIF/PRISM-filter")

# load our personas dataset. TODO make public
splits = {
    "train": "data/train-00000-of-00001.parquet",
    "test": "data/test-00000-of-00001.parquet",
}
df = pd.read_parquet("hf://datasets/RLAIF/Synthetic-Personas-Final/" + splits["train"])

# create samples from prism_dataset['train']

dataset = [
    create_sample(prism_row, persona)
    for prism_row, persona in zip(prism_dataset["train"], df.iterrows())
]


# system_prompt = system_prompt.format(demographic=str(row_dict)) + format

# take the first five of the dataset
dataset = dataset[:300]


@task
def prism_personalization():
    return Task(
        dataset=dataset,
        plan=[
            prompt_template_from_metadata(
                modes[mode]["system_prompt"], modes[mode]["format"]
            ),
            generate_and_validate(),
        ],
        scorer=model_critique(),
    )
