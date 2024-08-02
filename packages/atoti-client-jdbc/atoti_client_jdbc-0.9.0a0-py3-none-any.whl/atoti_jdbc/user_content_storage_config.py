from dataclasses import KW_ONLY
from typing import Annotated, final

from atoti._collections import FrozenMapping, frozendict
from atoti._jdbc import normalize_jdbc_url
from atoti._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from pydantic import AfterValidator
from pydantic.dataclasses import dataclass

from ._infer_driver import infer_driver


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class UserContentStorageConfig:
    """The config for storing user content in a separate database.

    Example:
        >>> from atoti_jdbc import UserContentStorageConfig
        >>> config = UserContentStorageConfig(
        ...     "mysql://localhost:7777/example?user=username&password=passwd"
        ... )

    """

    url: Annotated[str, AfterValidator(normalize_jdbc_url)]
    """The JDBC connection string of the database.

    The ``jdbc`` scheme is optional but the database specific scheme (such as ``h2`` or ``mysql``) is mandatory.
    For instance:

    * ``"h2:file:/home/user/database/file/path;USER=username;PASSWORD=passwd"``
    * ``"mysql://localhost:7777/example?user=username&password=passwd"``
    * ``"postgresql://postgresql.db.server:5430/example?user=username&password=passwd"``

    More examples can be found `here <https://www.baeldung.com/java-jdbc-url-format>`__.

    This defines Hibernate's `URL <https://javadoc.io/static/org.hibernate/hibernate-core/5.6.15.Final/org/hibernate/cfg/AvailableSettings.html#URL>`__ option.
    """

    _: KW_ONLY

    driver: str | None = None
    """The :mod:`~atoti_jdbc.driver` used to load the data.

    This defines Hibernate's `DRIVER <https://javadoc.io/static/org.hibernate/hibernate-core/5.6.15.Final/org/hibernate/cfg/AvailableSettings.html#DRIVER>`__ option.

    Inferred from :attr:`url` if ``None``.
    """

    hibernate_options: FrozenMapping[str, str] = frozendict()
    """Extra options to pass to Hibernate.

    See `AvailableSettings <https://javadoc.io/static/org.hibernate/hibernate-core/5.6.15.Final/org/hibernate/cfg/AvailableSettings.html>`__.
    """

    def __post_init__(self) -> None:
        if self.driver is None:
            self.__dict__["driver"] = infer_driver(self.url)
