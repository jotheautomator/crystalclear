"""Neo4j driver connection management."""

from neo4j import AsyncDriver, AsyncGraphDatabase

from app.core.config import settings

_driver: AsyncDriver | None = None


async def init_neo4j() -> None:
    """Initialize Neo4j driver on startup."""
    global _driver
    _driver = AsyncGraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
    )
    # Verify connectivity
    await _driver.verify_connectivity()


async def close_neo4j() -> None:
    """Close Neo4j driver on shutdown."""
    global _driver
    if _driver:
        await _driver.close()
        _driver = None


def get_neo4j_driver() -> AsyncDriver:
    """Dependency that returns the Neo4j driver."""
    if _driver is None:
        raise RuntimeError("Neo4j driver not initialized. Call init_neo4j() first.")
    return _driver
