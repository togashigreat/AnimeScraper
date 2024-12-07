import aiosqlite
import json

async def _initialize_database(db_path):
        """
        Initializes the SQLite database with necessary tables.
        """
        async with aiosqlite.connect(db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS anime (
                    id TEXT PRIMARY KEY,
                    data TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS character (
                    id TEXT PRIMARY KEY,
                    data TEXT
                )
            """)
            await db.commit()


async def _get_from_cache(db, table: str, key: str):
        async with db.execute(f"SELECT data FROM {table} WHERE id = ?", (key,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return json.loads(row[0])  # Return deserialized JSON
        return None



async def _store_in_cache(db, table: str, key: str, value: dict):
        async with db.execute(f"SELECT 1 FROM {table} WHERE id = ?", (key,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return  # Skip if the data already exists
        await db.execute(f"INSERT INTO {table} (id, data) VALUES (?, ?)", (key, json.dumps(value)))
        await db.commit()

