# add_column.py

import os
from sqlalchemy import create_engine, text


# =========================================================
# DATABASE CONNECTION
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not set")

# Railway fix
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# =========================================================
# SAFE COLUMN ADDER
# =========================================================

def add_column(table, column, column_type):
    """
    Safely adds a column if it doesn't exist.
    """

    try:
        with engine.connect() as conn:

            # Check if column exists
            check_query = text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = :table
                AND column_name = :column
            """)

            result = conn.execute(
                check_query,
                {"table": table, "column": column}
            ).fetchone()

            if result:
                print(f"⚠️ Column '{column}' already exists in '{table}'")
                return

            # Add column
            alter_query = text(
                f"ALTER TABLE {table} ADD COLUMN {column} {column_type}"
            )

            conn.execute(alter_query)
            conn.commit()

            print(f"✅ Added column '{column}' to '{table}'")

    except Exception as e:
        print(f"❌ Failed to add column '{column}':", e)


# =========================================================
# RUN MIGRATIONS HERE
# =========================================================

if __name__ == "__main__":

    print("🚀 Running database migrations...\n")

    # Example upgrades (Level 4 schema evolution)

    add_column("events", "image_url", "TEXT")
    add_column("events", "embedding", "TEXT")
    add_column("events", "source_type", "VARCHAR(50)")
    add_column("events", "tags", "TEXT")

    print("\n✅ Migration complete")