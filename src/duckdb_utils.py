"""
DuckDB Utility Functions

Helper functions for working with the large battles.csv dataset.
"""

import duckdb
import pandas as pd
from pathlib import Path
from typing import Optional, Union


def get_connection(db_path: Optional[str] = None) -> duckdb.DuckDBPyConnection:
    """
    Create a DuckDB connection.

    Args:
        db_path: Path to persistent database file. If None, creates in-memory DB.

    Returns:
        DuckDB connection object
    """
    if db_path:
        return duckdb.connect(db_path)
    return duckdb.connect()


def create_battles_view(
    con: duckdb.DuckDBPyConnection,
    csv_path: str = 'battles.csv',
    view_name: str = 'battles',
    sample_size: int = -1,
    prefer_parquet: bool = True
) -> None:
    """
    Create a view over the battles dataset (CSV or Parquet).

    Automatically uses Parquet if available (faster), otherwise falls back to CSV.
    Parquet files are typically 5-10x smaller and 10-50x faster for queries.

    Args:
        con: DuckDB connection
        csv_path: Path to battles.csv file (or battles.parquet)
        view_name: Name for the view (default: 'battles')
        sample_size: Number of rows to sample for type inference (-1 = all, CSV only)
        prefer_parquet: If True, automatically look for .parquet version of file

    Example:
        >>> con = get_connection()
        >>> create_battles_view(con, 'battles.csv')  # Uses battles.parquet if exists
        >>> df = con.sql("SELECT COUNT(*) FROM battles").df()
    """
    import os
    
    # Normalize path for DuckDB (forward slashes, escape quotes)
    def normalize_path(path: str) -> str:
        return path.replace("\\", "/").replace("'", "''")
    
    # Check for Parquet version if prefer_parquet is True
    file_path = csv_path
    if prefer_parquet and csv_path.endswith('.csv'):
        parquet_path = csv_path.replace('.csv', '.parquet')
        if os.path.exists(parquet_path):
            file_path = parquet_path
            print(f"✓ Found Parquet file: {parquet_path} (using this for faster queries)")
    
    # Determine file type and create appropriate view
    if file_path.endswith('.parquet'):
        # Use Parquet (faster, compressed)
        file_path_norm = normalize_path(file_path)
        con.execute(f"""
            CREATE OR REPLACE VIEW {view_name} AS
            SELECT * FROM read_parquet('{file_path_norm}')
        """)
        print(f"✓ Created view '{view_name}' from Parquet: {file_path}")
    else:
        # Use CSV (slower but no conversion needed)
        file_path_norm = normalize_path(file_path)
        con.execute(f"""
            CREATE OR REPLACE VIEW {view_name} AS
            SELECT * FROM read_csv_auto('{file_path_norm}',
                SAMPLE_SIZE={sample_size},
                IGNORE_ERRORS=true,
                hive_partitioning=0
            )
        """)
        print(f"✓ Created view '{view_name}' from CSV: {file_path}")
        if prefer_parquet:
            print(f"  💡 Tip: Convert to Parquet for 10-50x faster queries:")
            print(f"     python convert_to_parquet.py --input {file_path}")


def query_to_df(
    con: duckdb.DuckDBPyConnection,
    query: str,
    show_progress: bool = True
) -> pd.DataFrame:
    """
    Execute a SQL query and return results as pandas DataFrame.

    Args:
        con: DuckDB connection
        query: SQL query string
        show_progress: Whether to print query execution message

    Returns:
        pandas DataFrame with query results
    """
    if show_progress:
        print(f"Executing query...")

    result = con.sql(query).df()

    if show_progress:
        print(f"✓ Returned {len(result):,} rows, {len(result.columns)} columns")

    return result


def save_to_parquet(
    df: pd.DataFrame,
    filepath: Union[str, Path],
    compression: str = 'snappy'
) -> None:
    """
    Save DataFrame to Parquet format.

    Args:
        df: pandas DataFrame
        filepath: Output path (e.g., 'artifacts/card_stats.parquet')
        compression: Compression algorithm ('snappy', 'gzip', 'brotli')

    Example:
        >>> card_stats = query_to_df(con, "SELECT ...")
        >>> save_to_parquet(card_stats, 'artifacts/card_stats.parquet')
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(filepath, compression=compression, index=False)

    size_mb = filepath.stat().st_size / (1024 * 1024)
    print(f"✓ Saved {len(df):,} rows to {filepath} ({size_mb:.1f} MB)")


def load_from_parquet(filepath: Union[str, Path]) -> pd.DataFrame:
    """
    Load DataFrame from Parquet file.

    Args:
        filepath: Path to parquet file

    Returns:
        pandas DataFrame
    """
    df = pd.read_parquet(filepath)
    print(f"✓ Loaded {len(df):,} rows from {filepath}")
    return df


def create_sample(
    con: duckdb.DuckDBPyConnection,
    view_name: str = 'battles',
    sample_pct: float = 10.0,
    output_path: str = 'artifacts/sample_battles.parquet',
    stratify_by: Optional[str] = None
) -> pd.DataFrame:
    """
    Create a representative sample of the battles dataset.

    Args:
        con: DuckDB connection
        view_name: Name of the battles view
        sample_pct: Percentage of data to sample (0-100)
        output_path: Where to save the sample
        stratify_by: Column to stratify by (e.g., 'arena.id')

    Returns:
        pandas DataFrame with sampled data

    Example:
        >>> sample = create_sample(con, sample_pct=10, stratify_by='"arena.id"')
    """
    if stratify_by:
        # Stratified sampling (maintains distribution of stratify_by column)
        query = f"""
            SELECT * FROM {view_name}
            WHERE random() < {sample_pct / 100.0}
        """
    else:
        # Simple random sampling
        query = f"""
            SELECT * FROM {view_name}
            USING SAMPLE {sample_pct}% (bernoulli)
        """

    print(f"Creating {sample_pct}% sample...")
    sample_df = query_to_df(con, query, show_progress=False)

    save_to_parquet(sample_df, output_path)

    return sample_df


def get_schema(con: duckdb.DuckDBPyConnection, view_name: str = 'battles') -> pd.DataFrame:
    """
    Get the schema (column names and types) of a view.

    Args:
        con: DuckDB connection
        view_name: Name of the view

    Returns:
        DataFrame with columns: column_name, column_type, null, key, default, extra
    """
    schema = con.sql(f"DESCRIBE {view_name}").df()
    print(f"Schema for '{view_name}':")
    print(f"  {len(schema)} columns")
    return schema


def get_null_counts(
    con: duckdb.DuckDBPyConnection,
    view_name: str = 'battles',
    columns: Optional[list] = None,
    batch_size: int = 20
) -> pd.DataFrame:
    """
    Get null counts for all columns (or specified columns).
    
    Processes columns in batches to avoid buffer overflow on large datasets.

    Args:
        con: DuckDB connection
        view_name: Name of the view
        columns: List of column names to check (None = all columns)
        batch_size: Number of columns to process per batch (default: 20)

    Returns:
        DataFrame with columns: column_name, null_count, null_percentage
    """
    if columns is None:
        # Get all column names
        schema = con.sql(f"DESCRIBE {view_name}").df()
        columns = schema['column_name'].tolist()

    # Get total row count once
    total_rows_result = con.sql(f"SELECT COUNT(*) as total_rows FROM {view_name}").df()
    total_rows = total_rows_result['total_rows'].iloc[0]

    # Process columns in batches to avoid buffer overflow
    null_data = []
    num_batches = (len(columns) + batch_size - 1) // batch_size
    
    for batch_idx in range(num_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(columns))
        batch_columns = columns[start_idx:end_idx]
        
        # Build query to count nulls for this batch of columns
        null_checks = [
            f'SUM(CASE WHEN "{col}" IS NULL THEN 1 ELSE 0 END) as "{col}_nulls"'
            for col in batch_columns
        ]

        query = f"""
            SELECT
                {', '.join(null_checks)}
            FROM {view_name}
        """

        result = con.sql(query).df()
        
        # Process results for this batch
        for col in batch_columns:
            null_count = result[f'{col}_nulls'].iloc[0]
            null_pct = (null_count / total_rows) * 100
            null_data.append({
                'column_name': col,
                'null_count': null_count,
                'null_percentage': null_pct
            })

    null_df = pd.DataFrame(null_data).sort_values('null_percentage', ascending=False)

    return null_df
