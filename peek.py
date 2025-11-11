# peek.py
import duckdb, os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(SCRIPT_DIR, 'battles.csv')

con = duckdb.connect()                         # in-memory SQL engine
# Safe, streaming view over the CSV (no full load into RAM)
con.execute(f"""
CREATE VIEW v AS
SELECT * FROM read_csv_auto('{CSV}',
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
