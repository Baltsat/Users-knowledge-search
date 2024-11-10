import os
import json
from tqdm import tqdm
from pipelines import process_doc


def seed_by_file(fileName: str, base_url: str = "../content"):
    with open(f"{base_url}/{fileName}", "r", encoding="utf8") as file:
        data = json.load(file)
        number = fileName.split(".")[0]
        formatted = []
        for [k, v] in data.items():
            formatted.append(
                {
                    "fileName": f"{number}.pdf",
                    "slide": k,
                    "description": v,
                }
            )
        process_doc(formatted)
