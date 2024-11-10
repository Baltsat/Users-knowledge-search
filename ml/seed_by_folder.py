import os
import json
from tqdm import tqdm
from pipelines import process_doc


def seed_by_folder(folder: str = "../content"):
    files = list(filter((lambda f: "pdf_processed" in f), os.listdir(folder)))

    for fileName in tqdm(files):
        with open(f"../content/{fileName}", "r", encoding="utf8") as file:
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
