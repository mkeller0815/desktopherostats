#!/usr/bin/env python3
"""
Desktop Heroes PXT Data Extractor

This script extracts character levels, map progress, and kill statistics
from Desktop Heroes .pxt save files.
"""

import base64
import json
import sys
import os
from pathlib import Path


def decode_pxt_file(filepath):
    """Decode a base64-encoded .pxt file and return JSON data."""
    try:
        with open(filepath, 'rb') as f:
            encoded_data = f.read()

        # Decode base64
        decoded_data = base64.b64decode(encoded_data)

        # Parse JSON
        data = json.loads(decoded_data)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except base64.binascii.Error:
        print(f"Error: File '{filepath}' is not a valid base64-encoded file.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Decoded data is not valid JSON.")
        sys.exit(1)


def extract_character_levels(data):
    """Extract character levels from gameStore."""
    heroes = ["edric", "serewyn", "corin", "alaric"]
    levels = {}

    if 'gameStore' in data and 'characters' in data['gameStore']:
        characters = data['gameStore']['characters']
        for hero in heroes:
            char_key = f"char_{hero}"
            if char_key in characters:
                levels[hero] = characters[char_key].get('level', 0)
            else:
                levels[hero] = 0

    return levels


def extract_map_data(data):
    """Extract map maxLevel and kill counts per character."""
    heroes = ["edric", "serewyn", "corin", "alaric"]
    map_data = {}

    if 'progressStore' in data and 'map' in data['progressStore']:
        map_store = data['progressStore']['map']

        for hero in heroes:
            char_key = f"char_{hero}"
            map_data[hero] = {}

            if char_key in map_store:
                char_maps = map_store[char_key]

                # Extract all maps for this character
                for map_key, map_info in char_maps.items():
                    if map_key.startswith('map:'):
                        map_name = map_key.replace('map:', '')
                        map_data[hero][map_name] = {
                            'maxLevel': map_info.get('maxLevel', 0),
                            'totalKillCount': map_info.get('totalKillCount', 0),
                            'killCount': map_info.get('killCount', 0),
                            'furtherKillCount': map_info.get('furtherKillCount', 0),
                            'difficulty': map_info.get('difficulty', 0),
                            'distance': map_info.get('distance', 0)
                        }

    return map_data


def extract_total_kills_per_hero(data):
    """Extract total kills per hero from progressStore."""
    kills = {}

    if 'progressStore' in data and 'kill' in data['progressStore']:
        kill_store = data['progressStore']['kill']

        if 'byCharacter' in kill_store:
            by_character = kill_store['byCharacter']

            heroes = ["edric", "serewyn", "corin", "alaric"]
            for hero in heroes:
                char_key = f"char_{hero}"
                kills[hero] = by_character.get(char_key, 0)

    return kills


def print_results(levels, map_data, total_kills):
    """Print extracted data in a formatted way."""
    heroes = ["edric", "serewyn", "corin", "alaric"]

    print("=" * 170)
    print("DESKTOP HEROES - CHARACTER DATA")
    print("=" * 170)

    # Character Levels
    print("\nCHARACTER LEVELS:")
    print("-" * 50)
    for hero in heroes:
        hero_name = hero.capitalize()
        level = levels.get(hero, 0)
        print(f"  {hero_name:12} Level {level}")

    # Total Kills per Hero
    print("\nTOTAL KILLS PER HERO:")
    print("-" * 50)
    for hero in heroes:
        hero_name = hero.capitalize()
        kills = total_kills.get(hero, 0)
        print(f"  {hero_name:12} {kills:,} kills")

    # Map Data - Filter maps with at least one kill
    print("\nMAP PROGRESS:")
    print("=" * 170)

    # Get all unique map names and filter those with at least one kill
    all_maps = set()
    for hero_maps in map_data.values():
        all_maps.update(hero_maps.keys())

    # Define custom map order
    map_order = ['forest', 'desert', 'jungle', 'water', 'village', 'graveyard',
                 'swamp', 'castle', 'dungeon', 'cave', 'inferno', 'snow', 'mountain']

    # Filter maps: only include if at least one hero has kills, maintain custom order
    maps_with_kills = []
    for map_name in map_order:
        if map_name in all_maps:
            has_kills = False
            for hero in heroes:
                if map_name in map_data.get(hero, {}):
                    if map_data[hero][map_name]['totalKillCount'] > 0:
                        has_kills = True
                        break
            if has_kills:
                maps_with_kills.append(map_name)

    # Add any maps not in the predefined order (in case new maps exist)
    for map_name in sorted(all_maps):
        if map_name not in map_order:
            has_kills = False
            for hero in heroes:
                if map_name in map_data.get(hero, {}):
                    if map_data[hero][map_name]['totalKillCount'] > 0:
                        has_kills = True
                        break
            if has_kills:
                maps_with_kills.append(map_name)

    # Print table header with Difficulty, Distance, Level, and Kills for each hero
    header = f"{'Map':<15} | {'Difficulty':>10} | {'Distance':>12} |"
    for hero in heroes:
        hero_name = hero.capitalize()
        header += f" {hero_name + ' Lvl':>12} | {hero_name + ' Kills':>14} |"
    print(header)
    print("-" * 170)

    # Print data for each map
    for map_name in maps_with_kills:
        # Get difficulty and distance from first hero that has this map (they should be the same for all heroes)
        difficulty = 0
        distance = 0
        for hero in heroes:
            if map_name in map_data.get(hero, {}):
                difficulty = map_data[hero][map_name]['difficulty']
                distance = map_data[hero][map_name]['distance']
                break

        row = f"{map_name.capitalize():<15} | {difficulty:>10} | {distance:>12,} |"
        for hero in heroes:
            if map_name in map_data.get(hero, {}):
                max_level = map_data[hero][map_name]['maxLevel']
                kills = map_data[hero][map_name]['totalKillCount']
                row += f" {max_level:>12} | {kills:>14,} |"
            else:
                row += f" {'N/A':>12} | {0:>14} |"
        print(row)

    print("\n" + "=" * 170)


def main():
    """Main function to extract and display Desktop Heroes data."""
    # Check for command line argument
    if len(sys.argv) > 1:
        pxt_file = sys.argv[1]
    else:
        # Look for .pxt file in current directory
        pxt_files = list(Path('.').glob('*.pxt'))

        if not pxt_files:
            print("Error: No .pxt files found in current directory.")
            print("Usage: python extract_pxt_data.py [path/to/file.pxt]")
            sys.exit(1)

        if len(pxt_files) > 1:
            print("Multiple .pxt files found. Please specify which one to use:")
            for i, f in enumerate(pxt_files, 1):
                print(f"  {i}. {f}")
            print("\nUsage: python extract_pxt_data.py [path/to/file.pxt]")
            sys.exit(1)

        pxt_file = pxt_files[0]

    print(f"Reading data from: {pxt_file}\n")

    # Decode and extract data
    data = decode_pxt_file(pxt_file)
    levels = extract_character_levels(data)
    map_data = extract_map_data(data)
    total_kills = extract_total_kills_per_hero(data)

    # Display results
    print_results(levels, map_data, total_kills)


if __name__ == "__main__":
    main()
