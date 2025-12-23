# GameScript: PDF to Game Inputs Converter

> Transform any text document into a playable video game experience! Watch the Portuguese Constitution, your thesis, or any PDF "play" Pokémon through deterministic button inputs.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is This?

This project converts text documents (PDF or plain text) into game controller inputs that can be played back in video game emulators. Each character in your document maps to a specific button press, creating a deterministic sequence that "plays" a game.

**Example:** The Portuguese Constitution pressing buttons in Pokémon for ~47 hours straight!

## Features

- **PDF & Text Support** - Extract and convert any text document
- **Multi-System Support** - Nintendo DS and Game Boy/GBA mappings
- **DeSmuME Automation** - Auto-generated Lua scripts for emulator control
- **Complete Pipeline** - Single command from PDF to playable script
- **Progress Tracking** - Real-time progress updates with time estimates
- **Modular Design** - Clean, maintainable, well-documented code

## Technical Concepts

This project demonstrates several software engineering concepts:

### **1. Command-Line Interface (CLI) Design**
- Built with `argparse` for robust argument parsing
- User-friendly help messages and examples
- Flexible options with sensible defaults

### **2. Subprocess Orchestration**
- Master script coordinates multiple CLI tools
- Process isolation and error handling
- Automated pipeline execution

### **3. File Format Conversions**
- PDF → Text extraction (`PyPDF2`)
- Text → JSON (structured data)
- JSON → Lua (emulator scripting)
- Text normalization and character mapping

### **4. External System Integration**
- Generates Lua scripts for DeSmuME emulator
- Proper API usage for `joypad.set()` control
- Frame-by-frame timing synchronization

### **5. Code Organization**
- Separation of concerns (each script has one job)
- Reusable functions with clear documentation
- Modular architecture for maintainability

## Requirements

- Python 3.8 or higher
- PyPDF2 library
- DeSmuME emulator (for playback)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RiGraMa/GameScript-PDF-to-Game-Inputs-Converter.git
   cd GameScript-PDF-to-Game-Inputs-Converter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### **Option 1: Master Script (Recommended)**

The easiest way, runs the entire pipeline with one command:

```bash
# Basic usage - auto-generates document name
python converter/pdf_to_desmume.py samples/portuguese_constitution.pdf

# Specify custom document name
python converter/pdf_to_desmume.py samples/portuguese_constitution.pdf --name "Portuguese Constitution"

# Use Game Boy mapping
python converter/pdf_to_desmume.py samples/my_thesis.pdf --name "My Thesis" --system gb

# Text files work too!
python converter/pdf_to_desmume.py samples/recipe.txt --name "Grandma's Recipes"
```

**Output:**
- `constitution_inputs.json` - Intermediate file (can delete)
- `game_inputs.txt` - Button sequence for Lua
- `document_player.lua` - DeSmuME automation script

### **Option 2: Step-by-Step (Individual Scripts)**

For more control over the process:

#### **Step 1: Convert PDF/Text to JSON**
```bash
# Convert PDF to Nintendo DS inputs
python converter/pdf_to_json.py samples/portuguese_constitution.pdf constitution.json --system ds

# Convert text file to Game Boy inputs
python converter/pdf_to_json.py samples/document.txt output.json --system gb
```

#### **Step 2: Generate DeSmuME Lua Script**
```bash
# Interactive mode (prompts for document name)
python converter/json_to_lua_converter.py constitution.json

# Specify document name
python converter/json_to_lua_converter.py constitution.json --name "Portuguese Constitution"

# Custom output filenames
python converter/json_to_lua_converter.py constitution.json \
    --name "My Document" \
    --txt-output custom_inputs.txt \
    --lua-output custom_player.lua
```

## Running in DeSmuME

1. **Copy generated files to DeSmuME directory:**
   - `game_inputs.txt`
   - `document_player.lua`

2. **Open DeSmuME and load a Pokémon DS ROM**
   - Pokémon Diamond, Pearl, Platinum
   - Pokémon HeartGold, SoulSilver
   - Any other non-pokemon DS game works

3. **Load the Lua script:**
   - `Tools` → `Lua Scripting` → `New Lua Script Window`
   - Browse and select `document_player.lua`
   - Click `Run`

4. **Watch your document play**
   - Progress updates every 100 inputs
   - Time estimates and completion summary
   - Sit back and enjoy the automation

## Project Structure

```
GameScript-PDF-to-Game-Inputs-Converter/
├── converter/
│   ├── pdf_to_json.py              # PDF/Text → JSON converter
│   ├── json_to_lua_converter.py    # JSON → Lua script generator
│   └── pdf_to_desmume.py           # Master pipeline script
├── samples/
│   ├── portuguese_constitution.pdf # Example PDF (47+ hours of gameplay!)
│   └── test.pdf                    # Test file
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # You are here!
```

## How It Works

### **Character Mapping**

Each character maps to a button press:

```python
# Nintendo DS Example
"A" → UP
"E" → A button
"G" → START
" " → NO_INPUT (no button press)
```

### **Frame Timing**

- 9 frames per input at 60 FPS
- ~6.67 inputs per second
- Deterministic and reproducible

### **Example Conversion Flow**

```
"HELLO" 
  ↓
['SELECT', 'A', 'DOWN', 'DOWN', 'A']
  ↓
Lua script sends to emulator frame-by-frame
  ↓
Game responds to button presses
```

## Use Cases

- **Entertainment:** Watch documents play video games
- **Art Projects:** Generative gameplay from literature
- **Education:** Demonstrate deterministic systems
- **Testing:** Automated game testing with reproducible inputs


## Example Metrics

**Portuguese Constitution:**
- **Characters:** ~200,000
- **Total Inputs:** ~200,000 button presses
- **Estimated Duration:** ~12 hours of continuous gameplay
- **JSON Size:** ~14 MB

## Contributing

Contributions are welcome! Ideas for improvement:

- [ ] Add more system mappings (GBA, SNES, etc.)
- [ ] GUI interface for non-technical users
- [ ] Support for other emulators (VBA, RetroArch)
- [ ] Custom character mapping configuration
- [ ] Video recording of gameplay
- [ ] Web-based converter

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

**Ricardo Martins**
- GitHub: [@RiGraMa](https://github.com/RiGraMa)
- Project: [GameScript](https://github.com/RiGraMa/GameScript-PDF-to-Game-Inputs-Converter)

*If the Constitution can run a country, it can also run Pokémon no?*