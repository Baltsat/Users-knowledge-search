from copy import deepcopy
import json
from typing import Any, Iterable, Optional, Sequence, cast
from unstructured.documents.coordinates import PixelSpace

from unstructured.utils import Point
from unstructured.documents.elements import Element
from unstructured.staging.base import elements_to_dicts
from unstructured.partition.pdf import partition_pdf # version unstructured 0.11.5


# Define parameters for Unstructured's library

## include_page_breaks
# include page breaks (default is False)
include_page_breaks = True

## strategy
# The strategy to use for partitioning the PDF. Valid strategies are "hi_res", "ocr_only", and "fast".
# When using the "hi_res" strategy, the function uses a layout detection model to identify document elements.
# hi_res" is used for analyzing PDFs and extracting table structure (default is "auto")
strategy = "fast"

## infer_table_structure
# Only applicable if `strategy=hi_res`.
# If True, any Table elements that are extracted will also have a metadata field named "text_as_html" where the table's text content is rendered into an html string.
# I.e., rows and cells are preserved.
# Whether True or False, the "text" field is always present in any Table element and is the text content of the table (no structure).

if strategy == "hi_res": infer_table_structure = True
else: infer_table_structure = False

## extract_element_types
# Get images of tables
if infer_table_structure == True: extract_element_types=['Table']
else: extract_element_types=None

## max_characters
# The maximum number of characters to include in a partition (document element)
# If None is passed, no maximum is applied.
# Only applies to the "ocr_only" strategy (default is 1500)
if strategy != "ocr_only": max_characters = None

## languages
# The languages to use for the Tesseract agent.
# To use a language, you'll first need to install the appropriate Tesseract language pack.
languages = ["eng"] # example if more than one "eng+por" (default is "eng")

## model_name
# @requires_dependencies("unstructured_inference")
# yolox: best model for table extraction. Other options are yolox_quantized, detectron2_onnx and chipper depending on file layout
# source: https://unstructured-io.github.io/unstructured/best_practices/models.html
hi_res_model_name = "yolox"

def _fix_metadata_field_precision(elements: Iterable[Element]) -> list[Element]:
    out_elements: list[Element] = []
    for element in elements:
        el = deepcopy(element)
        if el.metadata.coordinates:
            precision = 1 if isinstance(el.metadata.coordinates.system, PixelSpace) else 2
            points = el.metadata.coordinates.points
            assert points is not None
            rounded_points: list[Point] = []
            for point in points:
                x, y = point
                rounded_point = (round(x, precision), round(y, precision))
                rounded_points.append(rounded_point)
            el.metadata.coordinates.points = tuple(rounded_points)

        if el.metadata.detection_class_prob:
            el.metadata.detection_class_prob = round(el.metadata.detection_class_prob, 5)

        out_elements.append(el)

    return out_elements

# Function to process each file's data
def process_data(data):
    page_texts = {}
    for entry in data:
        page_number = entry['metadata'].get('page_number')
        text = entry.get('text', '')
        if page_number and text:
            if page_number in page_texts:
                page_texts[page_number] += " " + text  # Concatenate text if page already exists
            else:
                page_texts[page_number] = text
    return page_texts

def _save_json(page_texts, filename, indent, encoding):
    json_str = json.dumps(page_texts, indent=indent, sort_keys=True, ensure_ascii=False)

    if filename is not None:
        with open(filename, "w", encoding=encoding) as f:
            f.write(json_str)
    return json_str
            
def _elements_to_json(
    elements: Iterable[Element],
    filename: Optional[str] = None,
    indent: int = 4,
    encoding: str = "utf-8",
) -> str:
    """Serialize `elements` to a JSON array.

    Also writes the JSON to `filename` if it is provided, encoded using `encoding`.

    The JSON is returned as a string.
    """
    # -- serialize `elements` as a JSON array (str) --
    precision_adjusted_elements = _fix_metadata_field_precision(elements)
    element_dicts = elements_to_dicts(precision_adjusted_elements)
     # Process the data
    res1 = _save_json(element_dicts, f'{filename}.json', indent, encoding)
    page_texts = process_data(element_dicts)
    res2 = _save_json(page_texts, f'{filename}_processed.json', indent, encoding)
    return res2

def process_and_save(filename):
    # Returns a List[Element] present in the pages of the parsed pdf document
    elements = partition_pdf(
            filename=filename,
            include_page_breaks=include_page_breaks,
            strategy=strategy,
            infer_table_structure=infer_table_structure,
            extract_element_types=extract_element_types,
            max_characters=max_characters,
            languages=languages,
            hi_res_model_name=hi_res_model_name,
    )

    # get output as json
    _elements_to_json(elements, filename=filename) # Takes a while for file to show up on the Google Colab
    
import os


if __name__ == "__main__":
    
    path = "./content/"
    
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if file.endswith(".pdf"):
                file_path = os.path.join(r, file)
                print("Path: ", file_path)
                # Open and read the JSON file
                process_and_save(file_path)
                # You can now access the data through the Pydantic model
                # print(model_data)