import aiosqlite

from src.token_manager.cache_interface import AccessTokenCacheInterface


class SQLiteCacheAdapter(AccessTokenCacheInterface):
    def __init__(self, db_path: str = "pydk_token_cache.db"):
        self._db_path = db_path
        self._initialized = False

    async def _init_db(self) -> None:
        if self._initialized:
            return
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS token_cache (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    token TEXT,
                    expires_at INTEGER
                );
            """
            )
            await db.commit()
        self._initialized = True

    async def get_token(self) -> tuple[str, int]:
        await self._init_db()
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute("SELECT token, expires_at FROM token_cache WHERE id = 1;")
            row = await cursor.fetchone()

            if row is None:
                raise ValueError("Token cache is empty. No token found.")

            token, expires_at = row

            if token is None:
                raise ValueError("Token cache returned None unexpectedly.")

            return token, expires_at

    async def save_token(self, token: str, expires_at: int) -> None:
        await self._init_db()
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT INTO token_cache (id, token, expires_at) VALUES (1, ?, ?) ON CONFLICT(id) DO UPDATE SET token = excluded.token, expires_at = excluded.expires_at;",
                (token, expires_at),
            )
            await db.commit()
