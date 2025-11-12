#!/usr/bin/env python3
"""
Convert Clash Royale card IDs to names using cards.json.

This script processes the battles.csv dataset to add card name columns
alongside existing card ID columns. It uses the cards.json file in the
Datasets folder to map card IDs to their names.

Usage:
    python id_to_name.py

The script will:
    - Read cards.json from Datasets/cards.json
    - Process battles.csv from Datasets/battles.csv
    - Create a new file Datasets/battles_with_names.csv with added name columns
    - Preserve all original columns and add new *_name columns

Behavior:
    - Builds id->name map from cards.json (RoyaleAPI format or Supercell /v1/cards).
    - Creates new *_name columns rather than overwriting originals.
    - Handles numeric ID columns and string columns containing ID lists.
    - Uses DuckDB for efficient processing of large CSV files.
"""

import os
import json
import re
from typing import Dict, List, Tuple
import duckdb
import pandas as pd
import numpy as np
from pathlib import Path


def get_project_paths():
    """Get absolute paths for project files."""
    script_dir = Path(__file__).parent.absolute()
    cards_path = script_dir / 'Datasets' / 'cards.json'
    battles_path = script_dir / 'Datasets' / 'battles.csv'
    output_path = script_dir / 'Datasets' / 'battles_with_names.csv'
    
    # Convert to absolute paths and normalize for cross-platform compatibility
    return {
        'cards': str(cards_path.resolve()),
        'battles': str(battles_path.resolve()),
        'output': str(output_path.resolve())
    }


def load_id_to_name(cards_path: str) -> Dict[int, str]:
    """Load card ID to name mapping from cards.json."""
    with open(cards_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Accept either a list of card dicts or {"items": [...]}
    items = data.get("items") if isinstance(data, dict) and "items" in data else data
    
    id_to_name = {}
    for c in items:
        try:
            cid = int(c["id"])
            name = str(c["name"])
            id_to_name[cid] = name
        except Exception:
            continue
    
    if not id_to_name:
        raise RuntimeError("No {id,name} pairs found in cards.json")
    
    print(f"✓ Loaded {len(id_to_name)} card mappings from cards.json")
    return id_to_name


DELIMS = [",", ";", "|", " "]


def split_tokens(s: str) -> Tuple[List[str], str]:
    """Split a string of IDs into tokens; return tokens and a chosen output delimiter."""
    s = s.strip()
    
    # JSON-like list: [26000000, 26000001]
    if s.startswith("[") and s.endswith("]"):
        toks = re.findall(r"-?\d+", s)
        return toks, ","
    
    for d in DELIMS:
        if d in s:
            toks = [t for t in re.split(rf"\s*{re.escape(d)}\s*", s) if t != ""]
            return toks, ","
    
    # Fallback: extract any integers found
    toks = re.findall(r"-?\d+", s)
    if toks:
        return toks, ","
    
    return [s], ","


def map_id_token(tok: str, id_to_name: Dict[int, str]) -> str:
    """Map a single token (ID) to card name."""
    try:
        cid = int(tok)
    except Exception:
        return tok  # non-integer token, leave as-is
    
    return id_to_name.get(cid, tok)  # unknown IDs left as original token


def looks_like_id_series(sample: List, id_keys: set, threshold: float = 0.6) -> bool:
    """Heuristic: does this column mostly contain IDs or ID lists that map to known IDs?"""
    seen = 0
    hits = 0
    
    for v in sample:
        if pd.isna(v):
            continue
        
        seen += 1
        
        if isinstance(v, (int, np.integer)):
            if int(v) in id_keys:
                hits += 1
        else:
            toks, _ = split_tokens(str(v))
            if not toks:
                continue
            
            # hit if most tokens are ints and at least one is in the mapping
            int_toks = [t for t in toks if re.fullmatch(r"-?\d+", t)]
            if int_toks and any(int(t) in id_keys for t in int_toks):
                hits += 1
        
        if seen >= 50:  # enough evidence
            break
    
    return seen > 0 and (hits / seen) >= threshold


def map_column_to_names(s: pd.Series, id_to_name: Dict[int, str]) -> pd.Series:
    """Map a pandas Series containing card IDs to card names."""
    id_keys = set(id_to_name.keys())
    
    def _map_cell(v):
        if pd.isna(v):
            return v
        
        if isinstance(v, (int, np.integer)):
            return id_to_name.get(int(v), v)
        
        # strings and other types
        toks, out_delim = split_tokens(str(v))
        mapped = [map_id_token(t, id_to_name) for t in toks]
        return out_delim.join(str(m) for m in mapped)
    
    # Vectorized where possible
    if np.issubdtype(s.dtype, np.number):
        return s.map(lambda x: id_to_name.get(int(x), x) if not pd.isna(x) else x)
    
    return s.astype("string").map(_map_cell)


def process_with_duckdb(battles_path: str, output_path: str, id_to_name: Dict[int, str]):
    """
    Process battles.csv using DuckDB for efficient handling of large files.
    
    This function:
    1. Creates a DuckDB view over battles.csv
    2. Identifies card ID columns
    3. Processes data in chunks to add name columns
    4. Writes output CSV
    """
    print(f"\nProcessing {battles_path}...")
    print("This may take a while for large files (9.2GB)...")
    
    # Create DuckDB connection
    con = duckdb.connect()
    
    # Create view over battles.csv
    print("Creating DuckDB view...")
    # Normalize path for DuckDB (use forward slashes, escape single quotes)
    battles_path_normalized = battles_path.replace("\\", "/").replace("'", "''")
    con.execute(f"""
        CREATE VIEW battles AS
        SELECT * FROM read_csv_auto('{battles_path_normalized}',
            SAMPLE_SIZE=-1,
            IGNORE_ERRORS=true,
            hive_partitioning=0
        )
    """)
    
    # Get schema to identify card columns
    schema = con.sql("DESCRIBE battles").df()
    all_columns = schema['column_name'].tolist()
    
    # Find card ID columns (winner.card1.id through winner.card8.id, same for loser)
    card_id_columns = []
    for col in all_columns:
        # Match patterns like winner.card1.id, loser.card2.id, etc.
        if re.match(r'^(winner|loser)\.card[1-8]\.id$', col):
            card_id_columns.append(col)
    
    print(f"\nFound {len(card_id_columns)} card ID columns to process")
    
    if not card_id_columns:
        print("⚠ Warning: No card ID columns found. Checking for other ID patterns...")
        # Fallback: look for any column with 'card' and 'id' in name
        for col in all_columns:
            if 'card' in col.lower() and 'id' in col.lower():
                card_id_columns.append(col)
                print(f"  Found: {col}")
    
    if not card_id_columns:
        print("❌ No card ID columns detected. Exiting.")
        return
    
    # Process in chunks to avoid memory issues
    chunk_size = 100000  # Process 100k rows at a time
    total_rows = con.sql("SELECT COUNT(*) as cnt FROM battles").df()['cnt'].iloc[0]
    print(f"Total rows: {total_rows:,}")
    print(f"Processing in chunks of {chunk_size:,} rows...")
    
    # Get all column names for SELECT
    all_cols_str = ', '.join([f'"{col}"' for col in all_columns])
    
    # Process first chunk to get structure
    first_chunk = con.sql(f"""
        SELECT {all_cols_str}
        FROM battles
        LIMIT {chunk_size}
    """).df()
    
    # Add name columns
    for col in card_id_columns:
        name_col = col.replace('.id', '.name')
        print(f"  Mapping {col} -> {name_col}...")
        first_chunk[name_col] = map_column_to_names(first_chunk[col], id_to_name)
    
    # Write header
    first_chunk.to_csv(output_path, index=False, mode='w', encoding='utf-8')
    print(f"  Processed rows 1-{len(first_chunk):,}")
    
    # Process remaining chunks
    offset = chunk_size
    while offset < total_rows:
        chunk = con.sql(f"""
            SELECT {all_cols_str}
            FROM battles
            LIMIT {chunk_size} OFFSET {offset}
        """).df()
        
        # Add name columns
        for col in card_id_columns:
            name_col = col.replace('.id', '.name')
            chunk[name_col] = map_column_to_names(chunk[col], id_to_name)
        
        # Append to file
        chunk.to_csv(output_path, index=False, mode='a', header=False, encoding='utf-8')
        print(f"  Processed rows {offset+1:,}-{offset+len(chunk):,}")
        
        offset += chunk_size
    
    con.close()
    print(f"\n✓ Processing complete!")
    print(f"  Output saved to: {output_path}")
    
    # Check output file size
    output_size_gb = os.path.getsize(output_path) / (1024**3)
    print(f"  Output file size: {output_size_gb:.2f} GB")


def main():
    """Main function to process card IDs to names."""
    print("=" * 60)
    print("Clash Royale Card ID to Name Converter")
    print("=" * 60)
    
    # Get paths
    paths = get_project_paths()
    
    # Check if files exist
    if not os.path.exists(paths['cards']):
        print(f"❌ Error: cards.json not found at {paths['cards']}")
        return
    
    if not os.path.exists(paths['battles']):
        print(f"❌ Error: battles.csv not found at {paths['battles']}")
        return
    
    # Load card mappings
    try:
        id_to_name = load_id_to_name(paths['cards'])
    except Exception as e:
        print(f"❌ Error loading cards.json: {e}")
        return
    
    # Process battles.csv
    try:
        process_with_duckdb(paths['battles'], paths['output'], id_to_name)
    except Exception as e:
        print(f"❌ Error processing battles.csv: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("✓ All done! You can now use battles_with_names.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()

