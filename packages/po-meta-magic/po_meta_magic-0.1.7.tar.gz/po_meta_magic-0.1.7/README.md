# `po_meta_magic`

## Overview

`po_meta_magic` is a Python package designed for extracting and processing text from images based on metadata and bounding box information. It includes functionalities for validating inputs, extracting text from specific regions of an image, formatting dates, and ensuring only allowed characters are included in the output.

## Installation
To install the package, use pip:

```bash
pip install po-meta-magic
```

### Parameters

- **image** (`PIL.Image.Image`):
  The image object from which text will be extracted.

- **meta_data** (`dict`):
  A dictionary where keys represent metadata types and values are dictionaries containing:
  - **bbox**:
    Bounding box coordinates as a tuple `(x_min, y_min, x_max, y_max)`.
  - **key**:
    The key or text to find and extract.
  - **date_format** (optional, `str`):
    Format for dates if the value is a date.
  - **optional_key_match** (optional, `bool`):
    If `True`, key is not required to be present in the text.
  - **allowed_chars** (optional, `str`):
    Characters to be kept in the text (e.g., `0-9A-Za-z`).
