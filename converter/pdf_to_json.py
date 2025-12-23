"""
PDF/Text to Game Input Converter

Converts text documents (PDF or plain text) into game controller inputs
for use with game emulators. Each character is mapped to a specific button
press, creating a deterministic sequence that can "play" a game.

Author: Ricardo Martins
Repository: https://github.com/RiGraMa/GameScript-PDF-to-Game-Inputs-Converter
"""

import re
import json
import argparse
import logging
from pathlib import Path
from PyPDF2 import PdfReader

# Configure logging for clean console output
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

# Character to button mapping for Nintendo DS
DS_BUTTON_MAPPING = {
    # Letters A-Z mapped to various buttons
    "A": "UP", "B": "DOWN", "C": "LEFT", "D": "RIGHT",
    "E": "A", "F": "B", "G": "START", "H": "SELECT",
    "I": "L", "J": "R", "K": "UP", "L": "DOWN",
    "M": "LEFT", "N": "RIGHT", "O": "A", "P": "B",
    "Q": "L", "R": "R", "S": "START", "T": "SELECT",
    "U": "LEFT", "V": "RIGHT", "W": "UP", "X": "DOWN",
    "Y": "A", "Z": "B",
    # Special characters
    " ": "NO_INPUT",   # Space = no button press
    ".": "A",          # Period = A button
    ",": "B",          # Comma = B button
    ";": "START",      # Semicolon = Start
    ":": "SELECT",     # Colon = Select
    "\n": "NO_INPUT"   # Newline = no button press
}

# Character to button mapping for Game Boy
GB_BUTTON_MAPPING = {
    # Letters A-Z mapped to various buttons
    "A": "UP", "B": "DOWN", "C": "LEFT", "D": "RIGHT",
    "E": "A", "F": "B", "G": "START", "H": "SELECT",
    "I": "A", "J": "B", "K": "UP", "L": "DOWN",
    "M": "LEFT", "N": "RIGHT", "O": "A", "P": "B",
    "Q": "START", "R": "SELECT", "S": "START", "T": "SELECT",
    "U": "LEFT", "V": "RIGHT", "W": "UP", "X": "DOWN",
    "Y": "A", "Z": "B",
    # Special characters
    " ": "NO_INPUT",
    ".": "A",
    ",": "B",
    ";": "START",
    ":": "SELECT",
    "\n": "NO_INPUT"
}


def extract_text_from_pdf(pdf_path):
    """
    Extract all text content from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Concatenated text from all pages
        
    Raises:
        ValueError: If PDF contains no extractable text
        RuntimeError: If PDF cannot be read or processed
        
    Example:
        >>> text = extract_text_from_pdf("document.pdf")
        >>> print(len(text))
        45823
    """
    try:
        reader = PdfReader(pdf_path)
        
        # Extract text from each page that contains text
        text_parts = [
            page.extract_text() 
            for page in reader.pages 
            if page.extract_text()
        ]
        
        # Combine all pages into single string
        text = "".join(text_parts)
        
        if not text:
            raise ValueError(
                f"No text could be extracted from PDF: {pdf_path}\n"
                "The file may be image-based or encrypted."
            )
            
        return text
        
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")


def process_text(text):
    """
    Clean and normalize text for button mapping.
    
    Converts text to uppercase and removes excessive whitespace
    to ensure consistent mapping to game inputs.
    
    Args:
        text (str): Raw text to process
        
    Returns:
        str: Processed text (uppercase, single spaces)
        
    Raises:
        ValueError: If text is empty after processing
        
    Example:
        >>> process_text("  Hello   World  ")
        'HELLO WORLD'
    """
    # Normalize whitespace: replace multiple spaces with single space
    processed_text = re.sub(r'\s+', ' ', text.strip())
    
    # Convert to uppercase for consistent mapping
    processed_text = processed_text.upper()
    
    if not processed_text:
        raise ValueError("Input text is empty after processing")
        
    return processed_text


def map_text_to_inputs(text, system="ds"):
    """
    Convert text characters to game controller inputs.
    
    Each character in the text is mapped to a specific button press
    based on the selected gaming system (Nintendo DS or Game Boy).
    
    Args:
        text (str): Processed text to convert
        system (str): Gaming system - "ds" or "gb" (default: "ds")
        
    Returns:
        list: Sequence of button names (e.g., ["UP", "A", "START"])
        
    Example:
        >>> map_text_to_inputs("HELLO", system="ds")
        ['SELECT', 'A', 'DOWN', 'DOWN', 'A']
    """
    # Select appropriate button mapping
    mapping = DS_BUTTON_MAPPING if system == "ds" else GB_BUTTON_MAPPING
    
    # Map each character to its button (default to NO_INPUT if not found)
    return [mapping.get(char, "NO_INPUT") for char in text]


def display_conversion_summary(input_file, output_file, num_inputs, system):
    """
    Display a formatted summary of the conversion process.
    
    Args:
        input_file (str): Source file path
        output_file (str): Destination file path
        num_inputs (int): Number of inputs generated
        system (str): System used for mapping
    """
    logging.info("\n" + "="*60)
    logging.info(" CONVERSION COMPLETE")
    logging.info("="*60)
    logging.info(f" Source:      {input_file}")
    logging.info(f" Output:      {output_file}")
    logging.info(f" System:      {system.upper()}")
    logging.info(f" Total inputs: {num_inputs:,}")
    logging.info("="*60)


def main(input_file, output_file, system):
    """
    Main conversion pipeline: text/PDF → processed text → game inputs → JSON.
    
    Args:
        input_file (str): Path to input file (.pdf or .txt)
        output_file (str): Path for output JSON file
        system (str): Target gaming system ("ds" or "gb")
        
    Process:
        1. Read file (PDF or text)
        2. Clean and normalize text
        3. Map characters to button inputs
        4. Save as JSON
    """
    try:
        # Step 1: Read input file
        input_path = Path(input_file)
        
        if not input_path.exists():
            logging.error(f" Error: File not found: {input_file}")
            return
        
        if input_file.lower().endswith(".pdf"):
            logging.info(f" Reading PDF: {input_file}")
            text = extract_text_from_pdf(input_file)
        else:
            logging.info(f" Reading text file: {input_file}")
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read()
        
        # Step 2: Process text
        logging.info(" Processing text...")
        processed_text = process_text(text)
        
        # Step 3: Map to game inputs
        logging.info(f" Mapping to {system.upper()} button inputs...")
        input_sequence = map_text_to_inputs(processed_text, system)
        
        # Step 4: Save to JSON
        logging.info(f" Saving to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(input_sequence, f, indent=2)
        
        # Display summary
        display_conversion_summary(
            input_file, 
            output_file, 
            len(input_sequence), 
            system
        )
        
    except Exception as e:
        logging.error(f"\n Error: {e}")


if __name__ == "__main__":
    # Command-line interface
    parser = argparse.ArgumentParser(
        description="Convert text documents to game controller inputs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert PDF to DS inputs
  python %(prog)s document.pdf output.json
  
  # Convert PDF to Game Boy inputs
  python %(prog)s document.pdf output.json --system gb
  
  # Convert text file
  python %(prog)s document.txt output.json --system ds

Supported Systems:
  ds  - Nintendo DS (default)
  gb  - Game Boy / Game Boy Advance

Output:
  JSON file containing array of button names
  Compatible with emulator automation scripts
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Input file (PDF or text)"
    )
    
    parser.add_argument(
        "output_file",
        help="Output JSON file path"
    )
    
    parser.add_argument(
        "--system",
        choices=["ds", "gb"],
        default="ds",
        help="Target gaming system (default: ds)"
    )
    
    args = parser.parse_args()
    
    # Run conversion
    main(args.input_file, args.output_file, args.system)