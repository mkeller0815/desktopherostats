# Desktop Heroes PXT Data Extractor

A Python script to extract and display character data from Desktop Heroes `.pxt` save files.

## Features

- **Character Levels**: Shows the level of all 4 heroes (Edric, Serewyn, Corin, Alaric)
- **Total Kills**: Displays total kills for each hero across all maps
- **Map Progress**: Shows maximum level reached and kill count per hero for each map

## Usage

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

## Requirements

- Python 3.6 or higher
- No external dependencies (uses standard library only)

## Output

The script displays:
1. Character levels for all 4 heroes
2. Total kills per hero
3. Detailed map progress showing:
   - Maximum level reached by each hero on each map
   - Total kill count per hero per map

## Technical Details

The `.pxt` files are base64-encoded JSON files containing:
- `gameStore.characters` - Character levels and stats
- `progressStore.map` - Map progress including maxLevel and kill counts
- `progressStore.kill.byCharacter` - Total kills per character
