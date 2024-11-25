"""
Module with console scripts.
"""

import json
from pathlib import Path

import click
import openai

from instruct_online_courses import settings, logger
from instruct_online_courses.generation_processing import get_generated_triplets, post_process_response


@click.command()
@click.argument("data-path", type=click.Path(exists=True, file_okay=True))
@click.argument("save-path", type=click.Path(exists=False, file_okay=True))
@click.option("--prompt", type=click.Path(exists=True, file_okay=True), default=None, help="Requirements prompt.")
def generate_instructions(data_path: str | Path, save_path, prompt: str | Path):
    """Data generation using openai API and jsonlines data from DATA_PATH."""
    client = openai.Client(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_API_BASE)
    # Generate triplets for each line.
    with open(prompt) as f:
        prompt_str = f.read()
    with open(save_path, "a", encoding="utf-8") as save_file, open(data_path, "r", encoding="utf-8") as data_file:
        for line in data_file:
            contents = get_generated_triplets(client, line, prompt_str)
            triplets = post_process_response(contents)
            for triplet in triplets:
                logger.debug(f"Writing triplet: {triplet}")
                save_file.write(json.dumps(triplet, ensure_ascii=False) + "\n")
