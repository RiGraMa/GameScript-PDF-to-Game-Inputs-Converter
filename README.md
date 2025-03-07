# GameScript: PDF to Game Inputs Converter

Convert any PDF file into game inputs for Nintendo DS or Game Boy! This tool is perfect for automating gameplay or creating fun projects.

## Features
- Convert PDF text to Nintendo DS or Game Boy inputs.
- Supports both `.pdf` and `.txt` files.
- Easy-to-use command-line interface.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RiGraMa/GameScript-PDF-to-Game-Inputs-Converter.git
   cd GameScript-PDF-to-Game-Inputs-Converter

2. Set up the virtual environment:
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

3. Install dependencies:
    pip install -r requirements.txt

## Usage 

1. Place your PDF or text file in the samples/ folder (or use the provided portuguese_constitution.pdf).

2. Run the converter
    python converter/pdf_to_json.py samples/portuguese_constitution.pdf output.json --system ds
    Replace ds with gb for Game Boy inputs.
    The output will be saved in output.json.


## Example

Convert the Portuguese Constitution to Nintendo DS inputs:
python converter/pdf_to_json.py samples/portuguese_constitution.pdf portuguese_ds.json --system ds