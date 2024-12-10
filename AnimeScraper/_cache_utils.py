import aiosqlite
import sqlite3
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


async def _get_from_cache(db, table: str, key: str)-> str | None:
        async with db.execute(f"SELECT data FROM {table} WHERE id = ?", (key,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]  # Return deserialized JSON
        return None



async def _store_in_cache(db, table: str, key: str, value: str):
        async with db.execute(f"SELECT 1 FROM {table} WHERE id = ?", (key,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return  # Skip if the data already exists
        await db.execute(f"INSERT INTO {table} (id, data) VALUES (?, ?)", (key, value))
        await db.commit()



def _start_database(db_path):
        """
        Initializes the SQLite database with necessary tables.
        """
        with sqlite3.connect(db_path) as db:
            cursor =  db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anime (
                    id TEXT PRIMARY KEY,
                    data TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS character (
                    id TEXT PRIMARY KEY,
                    data TEXT
                )
            """)
            db.commit()


def _from_cache(db, table: str, key: str):
        cursor = db.execute(f"SELECT data FROM {table} WHERE id = ?", (key,))
        row = cursor.fetchone()
        if row:
            print(row[0])
            return row[0]  # Return deserialized JSON
        return None


def _store_cache(db, table: str, key: str, value: str):
        cursor = db.execute(f"SELECT 1 FROM {table} WHERE id = ?", (key,))
        row = cursor.fetchone()
        if row:
            return  # Skip if the data already exists
        db.execute(f"INSERT INTO {table} (id, data) VALUES (?, ?)", (key, value))
        db.commit()

