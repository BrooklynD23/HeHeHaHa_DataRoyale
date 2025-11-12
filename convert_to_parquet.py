#!/usr/bin/env python3
"""
Convert battles.csv to Parquet format for faster queries.

This script converts the large CSV file to Parquet format, which:
- Is 5-10x smaller (compressed)
- Is 10-50x faster for repeated queries
- Still works with DuckDB (just change the file path)

Usage:
    python convert_to_parquet.py [--input battles.csv] [--output battles.parquet]

After conversion, update your notebooks to use:
    con.execute("CREATE VIEW battles AS SELECT * FROM read_parquet('battles.parquet')")
"""

import argparse
import os
import sys
import time
from pathlib import Path

import duckdb


def get_file_size_mb(filepath: str) -> float:
    """Get file size in MB."""
    return os.path.getsize(filepath) / (1024 ** 2)


def get_file_size_gb(filepath: str) -> float:
    """Get file size in GB."""
    return os.path.getsize(filepath) / (1024 ** 3)


def convert_csv_to_parquet(
    csv_path: str,
    parquet_path: str,
    chunk_size: int = 1_000_000
) -> None:
    """
    Convert CSV to Parquet using DuckDB.
    
    Processes in chunks to handle large files efficiently.
    
    Args:
        csv_path: Path to input CSV file
        parquet_path: Path to output Parquet file
        chunk_size: Number of rows to process per chunk
    """
    print("=" * 70)
    print("CSV to Parquet Converter")
    print("=" * 70)
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"[ERROR] {csv_path} not found!")
        sys.exit(1)
    
    # Check if output already exists
    if os.path.exists(parquet_path):
        response = input(f"[WARNING] {parquet_path} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    # Get input file size
    csv_size_gb = get_file_size_gb(csv_path)
    print(f"\nInput file: {csv_path}")
    print(f"  Size: {csv_size_gb:.2f} GB")
    
    # Create DuckDB connection
    print("\nConnecting to DuckDB...")
    con = duckdb.connect()
    
    # Set encoding to UTF-8 for output
    import sys
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Get row count (for progress tracking)
    print("Counting rows in CSV...")
    csv_path_escaped = csv_path.replace("\\", "/").replace("'", "''")
    
    # Count rows (this will be approximate but fast)
    print("  Counting (this may take a minute)...")
    row_count = con.sql(f"SELECT COUNT(*) as cnt FROM read_csv_auto('{csv_path_escaped}', SAMPLE_SIZE=-1, IGNORE_ERRORS=true)").df()['cnt'].iloc[0]
    print(f"  Total rows: {row_count:,}")
    
    # Convert to Parquet
    print(f"\nConverting to Parquet...")
    print(f"  Output: {parquet_path}")
    print(f"  This may take 5-15 minutes depending on your system...")
    
    start_time = time.time()
    
    # Use DuckDB's COPY command directly - this is the most efficient
    # DuckDB will handle type inference and conversion automatically
    parquet_path_escaped = parquet_path.replace("\\", "/").replace("'", "''")
    
    try:
        # Try with auto type inference first
        try:
            print("  Attempting conversion with auto type inference...")
            con.execute(f"""
                COPY (
                    SELECT * FROM read_csv_auto('{csv_path_escaped}',
                        SAMPLE_SIZE=200000,
                        IGNORE_ERRORS=true,
                        hive_partitioning=0
                    )
                ) 
                TO '{parquet_path_escaped}' (FORMAT PARQUET, COMPRESSION 'snappy')
            """)
        except Exception as type_error:
            # If type inference fails, use ALL_VARCHAR approach
            print("  Auto type inference failed (type inconsistencies detected).")
            print("  Using ALL_VARCHAR mode (slower but handles all type conflicts)...")
            con.execute(f"""
                COPY (
                    SELECT * FROM read_csv('{csv_path_escaped}',
                        SAMPLE_SIZE=-1,
                        IGNORE_ERRORS=true,
                        ALL_VARCHAR=true,
                        header=true
                    )
                ) 
                TO '{parquet_path_escaped}' (FORMAT PARQUET, COMPRESSION 'snappy')
            """)
        
        elapsed = time.time() - start_time
        
        # Get output file size
        parquet_size_gb = get_file_size_gb(parquet_path)
        compression_ratio = csv_size_gb / parquet_size_gb if parquet_size_gb > 0 else 0
        
        print(f"\n[SUCCESS] Conversion complete!")
        print(f"  Time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
        print(f"  Output size: {parquet_size_gb:.2f} GB")
        print(f"  Compression: {compression_ratio:.1f}x smaller")
        print(f"  Space saved: {csv_size_gb - parquet_size_gb:.2f} GB")
        
        # Verify the Parquet file
        print(f"\nVerifying Parquet file...")
        con.execute(f"""
            CREATE TEMP VIEW temp_parquet AS
            SELECT * FROM read_parquet('{parquet_path_escaped}')
        """)
        parquet_row_count = con.sql("SELECT COUNT(*) as cnt FROM temp_parquet").df()['cnt'].iloc[0]
        
        if parquet_row_count == row_count:
            print(f"  [OK] Row count matches: {parquet_row_count:,}")
        else:
            print(f"  [WARNING] Row count mismatch!")
            print(f"    CSV: {row_count:,}, Parquet: {parquet_row_count:,}")
        
        # Show sample
        print(f"\nSample from Parquet file:")
        sample = con.sql("SELECT * FROM temp_parquet LIMIT 5").df()
        print(sample.head())
        
    except Exception as e:
        print(f"\n[ERROR] Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        con.close()
    
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("=" * 70)
    print("\n1. Update your notebooks to use Parquet:")
    print("   OLD: create_battles_view(con, 'battles.csv')")
    print("   NEW: con.execute(\"CREATE VIEW battles AS SELECT * FROM read_parquet('battles.parquet')\")")
    print("\n2. Or update duckdb_utils.py to support Parquet files")
    print("\n3. Enjoy 10-50x faster queries! 🚀")


def main():
    parser = argparse.ArgumentParser(
        description='Convert battles.csv to Parquet format for faster queries'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='battles.csv',
        help='Path to input CSV file (default: battles.csv)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='battles.parquet',
        help='Path to output Parquet file (default: battles.parquet)'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=1_000_000,
        help='Rows per chunk (default: 1,000,000)'
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    script_dir = Path(__file__).parent.absolute()
    
    # Handle relative paths
    if not os.path.isabs(args.input):
        csv_path = script_dir / args.input
    else:
        csv_path = Path(args.input)
    
    if not os.path.isabs(args.output):
        parquet_path = script_dir / args.output
    else:
        parquet_path = Path(args.output)
    
    # Ensure output directory exists
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    
    convert_csv_to_parquet(
        str(csv_path),
        str(parquet_path),
        args.chunk_size
    )


if __name__ == '__main__':
    main()

