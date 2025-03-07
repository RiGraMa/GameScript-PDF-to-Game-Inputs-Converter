# Import necessary libraries
import re  # Regular expressions for text processing
import json  # For saving the output as JSON
import argparse  # For handling command-line arguments
import logging  # For logging messages
from PyPDF2 import PdfReader  # For extracting text from PDF files

# Set up logging to display messages with a simple format
logging.basicConfig(level=logging.INFO, format="%(message)s")

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.

    Raises:
        ValueError: If no text is extracted from the PDF.
        RuntimeError: If there is an error during PDF processing.
    """
    try:
        # Create a PdfReader object to read the PDF
        reader = PdfReader(pdf_path)
        # Extract text from each page and join it into a single string
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        # Check if the extracted text is empty
        if not text:
            raise ValueError("No text could be extracted from the PDF.")
        return text
    except Exception as e:
        # Raise an error if something goes wrong during extraction
        raise RuntimeError(f"Failed to extract text from PDF: {e}")

def process_text(text):
    """
    Cleans and normalizes text for input mapping.

    Args:
        text (str): The raw text to process.

    Returns:
        str: The processed text (uppercase, no extra spaces).

    Raises:
        ValueError: If the processed text is empty.
    """
    # Remove extra spaces and normalize the text to uppercase
    processed_text = re.sub(r'\s+', ' ', text.strip()).upper()
    # Check if the processed text is empty
    if not processed_text:
        raise ValueError("The input text is empty after processing.")
    return processed_text

def map_text_to_inputs(text, system="ds"):
    """
    Maps characters to game inputs based on the selected system.

    Args:
        text (str): The processed text to map to inputs.
        system (str): The system to use for mapping ("ds" or "gb").

    Returns:
        list: A list of game inputs corresponding to the text.
    """
    # Nintendo DS input mapping
    ds_mapping = {
        "A": "UP", "B": "DOWN", "C": "LEFT", "D": "RIGHT",
        "E": "A", "F": "B", "G": "START", "H": "SELECT",
        "I": "L", "J": "R", "K": "UP", "L": "DOWN",  # Reusing "UP" and "DOWN"
        "M": "LEFT", "N": "RIGHT", "O": "A", "P": "B",  # Reusing "A" and "B"
        "Q": "L", "R": "R", "S": "START", "T": "SELECT",  # Reusing "L", "R", "START", "SELECT"
        "U": "LEFT", "V": "RIGHT", "W": "UP", "X": "DOWN",  # Reusing "LEFT", "RIGHT", "UP", "DOWN"
        "Y": "A", "Z": "B",  # Reusing "A" and "B"
        " ": "NO_INPUT", ".": "A", ",": "B", ";": "START", ":": "SELECT",
        "\n": "NO_INPUT"
    }

    # Game Boy input mapping
    gb_mapping = {
        "A": "UP", "B": "DOWN", "C": "LEFT", "D": "RIGHT",
        "E": "A", "F": "B", "G": "START", "H": "SELECT",
        "I": "A", "J": "B", "K": "UP", "L": "DOWN",  # Reusing "UP" and "DOWN"
        "M": "LEFT", "N": "RIGHT", "O": "A", "P": "B",  # Reusing "A" and "B"
        "Q": "START", "R": "SELECT", "S": "START", "T": "SELECT",  # Reusing "START" and "SELECT"
        "U": "LEFT", "V": "RIGHT", "W": "UP", "X": "DOWN",  # Reusing "LEFT", "RIGHT", "UP", "DOWN"
        "Y": "A", "Z": "B",  # Reusing "A" and "B"
        " ": "NO_INPUT", ".": "A", ",": "B", ";": "START", ":": "SELECT",
        "\n": "NO_INPUT"
    }

    # Select the mapping based on the system
    mapping = ds_mapping if system == "ds" else gb_mapping
    # Map each character to its corresponding input
    return [mapping.get(char, "NO_INPUT") for char in text]

def main(input_file, output_file, system):
    """
    Processes a text or PDF file and saves game inputs as JSON.

    Args:
        input_file (str): Path to the input text or PDF file.
        output_file (str): Path to save the JSON output.
        system (str): The system to use for mapping ("ds" or "gb").
    """
    try:
        # Check if the input file is a PDF
        if input_file.lower().endswith(".pdf"):
            text = extract_text_from_pdf(input_file)
        else:
            # Read the input file as plain text
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read()
        
        # Process the text (clean and normalize)
        processed_text = process_text(text)
        # Map the text to game inputs
        input_sequence = map_text_to_inputs(processed_text, system)
        
        # Save the input sequence as a JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(input_sequence, f, indent=2)
        
        # Log a success message
        logging.info(f"Input sequence saved to {output_file}")
    except Exception as e:
        # Log an error message if something goes wrong
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Convert text to game inputs.")
    parser.add_argument("input_file", help="Path to the input text or PDF file.")
    parser.add_argument("output_file", help="Path to save the JSON output.")
    parser.add_argument("--system", choices=["ds", "gb"], default="ds",
                        help="Select the system: 'ds' for Nintendo DS or 'gb' for Game Boy.")
    # Parse the arguments
    args = parser.parse_args()
    # Call the main function with the parsed arguments
    main(args.input_file, args.output_file, args.system)

# C:\Users\ricar\myenv\Scripts\activate

# to run "python text_to_inputs.py portConst.pdf portConst.json"
