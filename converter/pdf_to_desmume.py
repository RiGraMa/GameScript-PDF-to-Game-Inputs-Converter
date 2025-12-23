"""
PDF/Text to DeSmuME - Complete Pipeline

Single command to convert any document (PDF or text) into a playable
DeSmuME Lua script. Runs both conversion steps automatically.

Pipeline:
1. Extract text from PDF/TXT → JSON inputs
2. Convert JSON → Lua script for DeSmuME

Author: Ricardo Martins
Repository: https://github.com/RiGraMa/GameScript-PDF-to-Game-Inputs-Converter
"""

import argparse
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """
    Execute a command and handle errors.
    
    Args:
        command (list): Command and arguments to execute
        description (str): Human-readable description of the step
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=False,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {description} failed!")
        print(f"Command: {' '.join(command)}")
        return False
    except FileNotFoundError:
        print(f"\n[ERROR] Could not find Python or script file")
        print(f"Command: {' '.join(command)}")
        return False


def display_header(input_file, document_name, system):
    """Display pipeline header with configuration"""
    print("\n" + "="*60)
    print("PDF/TEXT TO DESMUME - COMPLETE PIPELINE")
    print("="*60)
    print(f"\nInput file:     {input_file}")
    print(f"Document name:  {document_name}")
    print(f"System:         {system.upper()}")
    print(f"\nThis will generate:")
    print(f"  1. JSON file with game inputs")
    print(f"  2. Text file for Lua script (game_inputs.txt)")
    print(f"  3. Lua script for DeSmuME (document_player.lua)")
    print("="*60)


def display_final_summary(document_name):
    """Display final instructions after successful conversion"""
    print("\n" + "="*60)
    print("SUCCESS! ALL FILES GENERATED")
    print("="*60)
    print(f"\nYour document '{document_name}' is ready to play Pokemon!")
    print("\nGenerated files:")
    print("  • constitution_inputs.json (intermediate file)")
    print("  • game_inputs.txt (button sequence)")
    print("  • document_player.lua (DeSmuME script)")
    print("\nNext steps:")
    print("  1. Copy game_inputs.txt and document_player.lua to DeSmuME folder")
    print("  2. Open DeSmuME and load a Pokemon DS ROM")
    print("  3. Tools -> Lua Scripting -> New Lua Script Window")
    print("  4. Load document_player.lua")
    print(f"  5. Watch '{document_name}' play Pokemon!")
    print("\nTip: You can delete constitution_inputs.json if you don't need it")
    print("="*60 + "\n")


def main():
    """
    Main pipeline controller.
    
    Orchestrates both conversion steps:
    1. PDF/Text → JSON (via pdf_to_json.py)
    2. JSON → Lua (via json_to_lua_converter.py)
    """
    parser = argparse.ArgumentParser(
        description="Convert PDF/Text to DeSmuME Lua script - Complete Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (will prompt for document name)
  python %(prog)s document.pdf
  
  # Specify document name
  python %(prog)s portuguese_constitution.pdf --name "Portuguese Constitution"
  
  # Use Game Boy mapping instead of Nintendo DS
  python %(prog)s document.txt --name "My Thesis" --system gb
  
  # Full custom configuration
  python %(prog)s document.pdf --name "Recipe Book" --system ds

What this does:
  1. Extracts text from your PDF/TXT file
  2. Converts each character to game button inputs
  3. Generates DeSmuME Lua script that plays the game
  
Output files:
  • constitution_inputs.json (can be deleted after)
  • game_inputs.txt (needed by Lua script)
  • document_player.lua (load this in DeSmuME)

Supported systems:
  ds - Nintendo DS (default)
  gb - Game Boy / Game Boy Advance
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Input file (PDF or TXT)"
    )
    
    parser.add_argument(
        "--name",
        default=None,
        help='Document name for display (e.g., "My Thesis", "Constitution")'
    )
    
    parser.add_argument(
        "--system",
        choices=["ds", "gb"],
        default="ds",
        help="Target gaming system (default: ds)"
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"[ERROR] File not found: {args.input_file}")
        return 1
    
    # Get document name (from argument or generate from filename)
    if args.name:
        document_name = args.name
    else:
        document_name = (
            input_path.stem
            .replace('_', ' ')
            .replace('-', ' ')
            .title()
        )
        print(f"\n[INFO] Using auto-generated document name: '{document_name}'")
        print(f"       (Use --name to specify custom name)")
    
    # Define intermediate JSON filename
    json_file = "constitution_inputs.json"
    
    # Display pipeline configuration
    display_header(args.input_file, document_name, args.system)
    
    # Get script directory (where this master script is located)
    script_dir = Path(__file__).parent
    
    # STEP 1: PDF/Text to JSON
    pdf_to_json_script = script_dir / "pdf_to_json.py"
    step1_command = [
        sys.executable,  # Use same Python interpreter
        str(pdf_to_json_script),
        args.input_file,
        json_file,
        "--system", args.system
    ]
    
    if not run_command(step1_command, "Converting document to JSON inputs"):
        return 1
    
    # STEP 2: JSON to Lua
    json_to_lua_script = script_dir / "json_to_lua_converter.py"
    step2_command = [
        sys.executable,
        str(json_to_lua_script),
        json_file,
        "--name", document_name
    ]
    
    if not run_command(step2_command, "Generating DeSmuME Lua script"):
        return 1
    
    # Display final summary
    display_final_summary(document_name)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())