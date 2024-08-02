from datetime import datetime
from dateutil import parser
import pytesseract
from PIL import Image
import os
from functools import wraps
import re

def validate_inputs(func):
    """
    Decorator to validate inputs for the extract_meta function.

    Validates that:
    - The image is not None.
    - The meta_data is a dictionary.
    - Each value in meta_data is a dictionary containing a 'bbox' tuple and a 'key' string.

    Adds any validation errors to an 'errors' attribute on the function.
    """
    @wraps(func)
    def wrapper(image, meta_data=None):
        wrapper.errors = []  # Initialize an empty list for errors

        if image is None:
            wrapper.errors.append("Image must be provided and cannot be None.")

        if not isinstance(meta_data, dict):
            wrapper.errors.append("meta_data must be a dictionary.")
        else:
            for key, value in meta_data.items():
                if not isinstance(value, dict):
                    wrapper.errors.append(f"Value for '{key}' must be a dictionary.")
                else:
                    bbox = value.get('bbox')
                    key_value = value.get('key')

                    if not (isinstance(bbox, tuple) or isinstance(bbox, list)):
                        wrapper.errors.append(f"'bbox' for '{key}' must be a tuple.")

                    if not isinstance(key_value, str):
                        wrapper.errors.append(f"'key' for '{key}' must be a string.")

        return func(image, meta_data)
    return wrapper

@validate_inputs
def extract_meta(image, meta_data=None):
    if extract_meta.errors:
        print("Validation Errors:")
        return extract_meta.errors

    extracted_data = {}

    for idx_key, values in meta_data.items():
        bbox = values['bbox']
        key = values['key']
        date_format = values.get('date_format', None)
        optional_key_match = values.get('optional_key_match', False)
        allowed_chars = values.get('allowed_chars', None)

        cleaned_text = extract_meta_data(image, bbox, key, optional_key_match)

        if date_format:
            cleaned_text = make_required_format(cleaned_text, date_format)

        if allowed_chars:
            cleaned_text = keep_allowed_chars(cleaned_text, allowed_chars)

        extracted_data[idx_key] = cleaned_text

    return extracted_data


def keep_allowed_chars(text, allowed_chars):
    pattern = f'[^{allowed_chars}]'
    return re.sub(pattern, '', text)

# meta_data = {
#  'delivery_date': {
#         "bbox": (),
#         "key": '',
#         "date_format" : ''
#      },
# 'delivery_address': {
#         "bbox": (),
#         "key": '',
#         "optional_key_match": True
#     },
# 'po_number': {
#         "bbox": (),
#         "key": '',
#         "allowed_chars": '0-9A-Za-z'
#     }
# }

### PRIVATE METHODS

def extract_meta_data(image, bbox, key, optional_key_match, retry=0):
    img_width, img_height = image.size
    start_x = bbox[0] * img_width
    start_y = bbox[1] * img_height
    end_x = bbox[2] * img_width
    end_y = bbox[3] * img_height

    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    text = pytesseract.image_to_string(cropped_image)
    text = text.strip()

    removed_key_text = find_and_remove_key(text, key, optional_key_match)
    if not removed_key_text and retry<5:
        bigger_bbox = increase_bounding_box(bbox)
        return extract_meta_data(image, bigger_bbox, key, optional_key_match, retry+1)

    return removed_key_text

def make_required_format(date_text, required_format):
    try:
        parsed_date = parser.parse(date_text, fuzzy=True)
        formatted_date = parsed_date.strftime(required_format)
        return formatted_date
    except ValueError:
        raise ValueError("Date format not recognized")

def increase_bounding_box(bbox, increase_factor=0.1):
    x_min, y_min, x_max, y_max = bbox

    width = x_max - x_min
    height = y_max - y_min

    new_width = width * (1 + increase_factor)
    new_height = height * (1 + increase_factor)

    width_increase = (new_width - width) / 2
    height_increase = (new_height - height) / 2

    new_x_min = max(0, x_min - width_increase)
    new_y_min = max(0, y_min - height_increase)
    new_x_max = min(1, x_max + width_increase)
    new_y_max = min(1, y_max + height_increase)

    if new_x_min < 0:
        new_x_max -= new_x_min
        new_x_min = 0
    if new_y_min < 0:
        new_y_max -= new_y_min
        new_y_min = 0
    if new_x_max > 1:
        new_x_min -= (new_x_max - 1)
        new_x_max = 1
    if new_y_max > 1:
        new_y_min -= (new_y_max - 1)
        new_y_max = 1

    return (new_x_min, new_y_min, new_x_max, new_y_max)

def find_and_remove_key(text, key, optional_key_match):
    if optional_key_match:
        return text

    if key in text:
        text = text.replace(key, '')
        return text

    return ''