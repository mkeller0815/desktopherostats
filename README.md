# Desktop Heroes Stats

Game state analyzer for the Idle Game "Desktop Heroes"

## Overview

This project provides tools to extract and visualize character data from Desktop Heroes `.pxt` save files:

- **Python CLI Script** (`extract_pxt_data.py`) - Command-line tool for terminal output
- **Web Viewer** (`desktop_heros_viewer.html`) - Standalone HTML file for browser-based viewing

## Features

- **Character Levels**: Shows the level of all 4 heroes (Edric, Serewyn, Corin, Alaric)
- **Total Kills**: Displays total kills for each hero across all maps
- **Map Progress**: Shows maximum level reached and kill count per hero for each map
- **Custom Map Order**: Maps displayed in game progression order
- **No External Dependencies**: Both tools work standalone with no external libraries

## Python Script Usage

### Automatic Detection
If there's only one `.pxt` file in the current directory:
```bash
python3 extract_pxt_data.py
```

### Specify File
To extract data from a specific file:
```bash
python3 extract_pxt_data.py path/to/savefile.pxt
```

### Requirements
- Python 3.6 or higher
- No external dependencies (uses standard library only)

### Output
The script displays:
1. Character levels for all 4 heroes
2. Total kills per hero
3. Detailed map progress table showing:
   - Maximum level reached by each hero on each map
   - Total kill count per hero per map

## HTML Viewer Usage

### Online (GitHub Pages)

Visit the live viewer at: **https://mkeller0815.github.io/desktopherostats/**

### Local Usage

Simply open `desktop_heros_viewer.html` (or `index.html`) in any modern web browser and:
- Click the button to select a `.pxt` file, or
- Drag and drop a `.pxt` file onto the upload area

### Features
- Beautiful, responsive UI with gradient design
- Drag-and-drop file upload
- Client-side processing (data never leaves your computer)
- Works offline - no external dependencies
- Mobile-friendly

## Technical Details

The `.pxt` files are base64-encoded JSON files containing:
- `gameStore.characters` - Character levels and stats
- `progressStore.map` - Map progress including maxLevel and kill counts
- `progressStore.kill.byCharacter` - Total kills per character

Both tools decode the base64 data, parse the JSON structure, and extract relevant game statistics.

## File Structure

```
.
├── extract_pxt_data.py          # Python CLI script
├── desktop_heros_viewer.html    # Standalone HTML viewer
├── index.html                   # Symlink to HTML viewer (for GitHub Pages)
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.
