import duckdb

# Connect to DuckDB
con = duckdb.connect()

# Create view from CSV
con.execute("""
  CREATE VIEW battles AS
  SELECT * FROM read_csv_auto('battles.csv',
    SAMPLE_SIZE=-1,
    IGNORE_ERRORS=true,
    hive_partitioning=0
  )
""")

# Count total matches
result = con.sql("SELECT COUNT(*) as total_matches FROM battles").df()
total = result.iloc[0]['total_matches']

print(f"Total matches: {total:,}")

