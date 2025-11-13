#!/usr/bin/env python3
"""
create_sample.py

Generate a stratified sample of the battles dataset (Parquet or CSV) for faster iteration.

Usage:
    python create_sample.py [--pct PERCENTAGE] [--stratify COLUMN]

Examples:
    python create_sample.py                          # 10% sample
    python create_sample.py --pct 15                 # 15% sample
    python create_sample.py --stratify "arena.id"    # Stratify by arena
"""

import argparse
import os
import sys
import duckdb

# Add src/ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from duckdb_utils import get_connection, create_battles_view, create_sample


def main():
    parser = argparse.ArgumentParser(
        description='Create a sample of battles dataset (Parquet or CSV) for faster analysis'
    )
    parser.add_argument(
        '--pct',
        type=float,
        default=10.0,
        help='Percentage of data to sample (default: 10.0)'
    )
    parser.add_argument(
        '--stratify',
        type=str,
        default=None,
        help='Column to stratify by (e.g., "arena.id")'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='artifacts/sample_battles_10pct.parquet',
        help='Output file path (default: artifacts/sample_battles_10pct.parquet)'
    )
    parser.add_argument(
        '--input',
        type=str,
        default=None,
        help='Path to battles.parquet or battles.csv (default: auto-detect battles.parquet)'
    )

    args = parser.parse_args()

    # Auto-detect input file (prefer Parquet, fallback to CSV)
    if args.input is None:
        if os.path.exists('battles.parquet'):
            args.input = 'battles.parquet'
            print("Using battles.parquet (auto-detected)")
        elif os.path.exists('battles.csv'):
            args.input = 'battles.csv'
            print("Using battles.csv (auto-detected, Parquet not found)")
        else:
            print("[ERROR] Neither battles.parquet nor battles.csv found!")
            print(f"Current directory: {os.getcwd()}")
            sys.exit(1)
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"[ERROR] {args.input} not found!")
        print(f"Current directory: {os.getcwd()}")
        sys.exit(1)

    # Get file size
    file_size_gb = os.path.getsize(args.input) / (1024**3)
    print(f"Input file: {args.input} ({file_size_gb:.2f} GB)")
    print(f"Sample percentage: {args.pct}%")
    print(f"Output: {args.output}")
    if args.stratify:
        print(f"Stratifying by: {args.stratify}")

    # Create connection
    print("\nConnecting to DuckDB...")
    con = get_connection()

    # Create view (automatically uses Parquet if available)
    print("Creating view over dataset...")
    create_battles_view(con, args.input)

    # Create sample
    print(f"\nGenerating {args.pct}% sample...")
    sample_df = create_sample(
        con,
        view_name='battles',
        sample_pct=args.pct,
        output_path=args.output,
        stratify_by=args.stratify
    )

    print(f"\n✓ Sample created successfully!")
    print(f"  - Rows: {len(sample_df):,}")
    print(f"  - Columns: {len(sample_df.columns)}")
    print(f"  - Saved to: {args.output}")

    # Show sample stats
    output_size_mb = os.path.getsize(args.output) / (1024**2)
    compression_ratio = (file_size_gb * 1024) / output_size_mb
    print(f"  - File size: {output_size_mb:.1f} MB")
    print(f"  - Compression: {compression_ratio:.1f}x smaller than CSV")

    print(f"\nNext steps:")
    print(f"  1. Use this sample in Jupyter notebooks for fast iteration")
    print(f"  2. Upload to Google Drive for Colab access")
    print(f"  3. Run full queries on battles.parquet for faster performance")


if __name__ == '__main__':
    main()
