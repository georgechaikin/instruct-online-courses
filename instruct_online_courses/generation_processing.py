"""
Code for data generation.
"""

import re
from typing import TypedDict

import openai

from instruct_online_courses import settings, logger


class DataTriplet(TypedDict):
    Instruction: str
    Input: str
    Output: str


def get_generated_triplets(
        client: openai.Client,
        triplet: str,
        prompt: str,
        num_triplets: int = settings.num_triplets,
        model_name=settings.model_name,
        max_tokens=settings.max_tokens,
) -> str:
    """Data generation using OpenAI API.

    Args:
        client: openai Client object.
        triplet: Triplet that is used to generate data.
        prompt: Prompt with num_triplets, triplet arguments and instruction.
        num_triplets: Number of triplets to generate.
        model_name: Model that should be used for generation.
        max_tokens: Max tokens.

    Returns:

    """
    instruction_prompt = prompt.format(num_triplets=num_triplets, triplet=triplet)
    completion_batch = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a creative assistant that generates dataset for instruct tuning."},
            {"role": "user", "content": instruction_prompt},
        ],
        max_tokens=max_tokens,
    )
    return completion_batch.choices[0].message.content


def post_process_response(contents: str) -> list[DataTriplet]:
    """Post processes the generated text into the list of data triplets.

    Args:
        contents: List of generated strings with triplets.

    Returns:
        List of triplets (dictionaries with "Instruction", "Input" and "Output" keys).
    """
    logger.debug(f"Postprocessing the string: {contents}")
    result: list[DataTriplet] = []

    triplet_pattern = r"Instruction:\s*(.*?)\s*Input:\s*(.*?)\s*Output:\s*(.*)"

    for triplet in re.findall(triplet_pattern, contents):
        instruction, input_value, output_value = triplet
        result.append({"Instruction": instruction, "Input": input_value, "Output": output_value})
    return result
