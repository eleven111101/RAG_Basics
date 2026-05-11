import json
import os

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_json(data, filename="scenarios.json"):

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    logger.info(
        f"JSON Saved Successfully: {output_path}"
    )