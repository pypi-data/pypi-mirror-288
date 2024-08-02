import re
from collections.abc import Mapping

from .driver import (
    H2_DRIVER,
    IBM_DB2_DRIVER,
    MARIADB_DRIVER,
    MSSQL_DRIVER,
    MYSQL_DRIVER,
    ORACLE_DRIVER,
    POSTGRESQL_DRIVER,
)

_DRIVER_FROM_PATH: Mapping[str, str] = {
    "db2": IBM_DB2_DRIVER,
    "h2": H2_DRIVER,
    "mariadb": MARIADB_DRIVER,
    "mysql": MYSQL_DRIVER,
    "oracle": ORACLE_DRIVER,
    "postgresql": POSTGRESQL_DRIVER,
    "sqlserver": MSSQL_DRIVER,
}


def infer_driver(url: str, /) -> str:
    match = re.match(r"jdbc:(?P<driver_path>[^:]+):", url)
    driver_path = match.group("driver_path") if match else None
    driver = _DRIVER_FROM_PATH.get(driver_path) if driver_path else None

    if not driver:
        raise ValueError(
            f"Cannot infer driver from URL: `{url}`.",
        )

    return driver
