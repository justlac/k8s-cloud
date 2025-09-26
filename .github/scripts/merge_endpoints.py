#!/usr/bin/env python3
"""
Script to merge multiple gatus-endpoints.yml files into a single combined file.
Usage: python3 merge_endpoints.py <combined_file> <file1> [file2] [file3] ...
"""

import sys
import yaml
from pathlib import Path


def merge_endpoint_files(combined_file_path, *input_files):
    """
    Merge multiple gatus endpoint YAML files into a single combined file.

    Args:
        combined_file_path: Path to the output combined file
        *input_files: Variable number of input YAML files to merge
    """
    # Initialize with empty endpoints array if file doesn't exist or is empty
    combined_data = {"endpoints": []}

    # Load existing combined file if it exists
    combined_path = Path(combined_file_path)
    if combined_path.exists() and combined_path.stat().st_size > 0:
        try:
            with open(combined_path, "r", encoding="utf-8") as f:
                combined_data = yaml.safe_load(f) or {"endpoints": []}
        except Exception as e:
            print(f"Warning: Could not load existing combined file: {e}")
            combined_data = {"endpoints": []}

    # Process each input file
    total_endpoints_added = 0
    for file_path in input_files:
        input_path = Path(file_path)
        if not input_path.exists():
            print(f"Warning: File {file_path} does not exist, skipping")
            continue

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                file_data = yaml.safe_load(f)

            if file_data and "endpoints" in file_data and file_data["endpoints"]:
                endpoint_count = len(file_data["endpoints"])
                print(f"  🔄 Processing: {file_path} ({endpoint_count} endpoints)")
                combined_data["endpoints"].extend(file_data["endpoints"])
                total_endpoints_added += endpoint_count
            else:
                print(f"  ⚠️  No endpoints found in: {file_path}")

        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
            continue

    # Write the combined file
    try:
        with open(combined_path, "w", encoding="utf-8") as f:
            yaml.dump(
                combined_data, f, default_flow_style=False, sort_keys=False, indent=2
            )

        final_count = len(combined_data["endpoints"])
        print(f"  ✅ Combined file now has: {final_count} endpoints")
        return final_count

    except Exception as e:
        print(f"❌ Error writing combined file: {e}")
        return 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 merge_endpoints.py <combined_file> [file1] [file2] ...")
        print("If no input files are provided, will create an empty endpoints file")
        sys.exit(1)

    combined_file = sys.argv[1]
    input_files = sys.argv[2:] if len(sys.argv) > 2 else []

    if not input_files:
        # Create empty endpoints file
        print(f"Creating empty endpoints file: {combined_file}")
        with open(combined_file, "w", encoding="utf-8") as f:
            yaml.dump(
                {"endpoints": []},
                f,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
            )
        return

    print(f"Merging {len(input_files)} files into {combined_file}")
    final_count = merge_endpoint_files(combined_file, *input_files)

    if final_count > 0:
        print(f"✅ Successfully merged {final_count} endpoints")
    else:
        print("⚠️  No endpoints were merged")


if __name__ == "__main__":
    main()
