# peek.py
import duckdb, os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARQUET = os.path.join(SCRIPT_DIR, 'battles.parquet')
CSV = os.path.join(SCRIPT_DIR, 'battles.csv')  # Fallback

con = duckdb.connect()                         # in-memory SQL engine

# Use Parquet if available (faster), otherwise fall back to CSV
if os.path.exists(PARQUET):
    print("Using battles.parquet (faster queries)...")
    con.execute(f"""
    CREATE VIEW v AS
    SELECT * FROM read_parquet('{PARQUET.replace("\\", "/")}');
    """)
else:
    print("Using battles.csv (Parquet not found, consider converting for faster queries)...")
    con.execute(f"""
    CREATE VIEW v AS
    SELECT * FROM read_csv_auto('{CSV.replace("\\", "/")}',
      SAMPLE_SIZE=-1,            -- robust type inference
      IGNORE_ERRORS=true,
      hive_partitioning=0
    );
    """)

print("Head:")
print(con.sql("SELECT * FROM v LIMIT 50").df())  # first 50 rows

print("\nSchema:")
print(con.sql("DESCRIBE v").df())                # column names + inferred types

print("\nRow count estimate (fast approximate):")
print(con.sql("SELECT COUNT(*) AS rows FROM v").df())
