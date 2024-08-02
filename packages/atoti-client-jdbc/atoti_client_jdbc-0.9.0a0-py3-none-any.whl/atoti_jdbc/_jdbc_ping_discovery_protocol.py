from dataclasses import KW_ONLY
from typing import final

from atoti._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from atoti.experimental._distributed import DiscoveryProtocol
from pydantic.dataclasses import dataclass
from typing_extensions import override

from ._infer_driver import infer_driver


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class JdbcPingDiscoveryProtocol(DiscoveryProtocol):
    connection_url: str

    _: KW_ONLY

    connection_username: str

    connection_password: str

    connection_driver: str | None = None
    """The :mod:`~atoti.jdbc_driver` to use.

    If ``None``, it is inferred from :attr:`connection_url`.
    """

    delete_single_sql: str | None = None

    initialize_sql: str | None = None

    insert_single_sql: str | None = None

    remove_all_data_on_view_change: bool = True
    """"Defined by the FILE_PING protocol.

    See http://jgroups.org/manual4/index.html#_removal_of_zombie_files.
    """

    remove_old_coords_on_view_change: bool = True
    """"Defined by the FILE_PING protocol.

    See http://jgroups.org/manual4/index.html#_removal_of_zombie_files.
    """

    select_all_pingdata_sql: str | None = None

    write_data_on_find: bool = True
    """"Defined by the FILE_PING protocol.

    See http://jgroups.org/manual4/index.html#_removal_of_zombie_files.
    """

    def __post_init__(self) -> None:
        if self.connection_driver is None:
            self.__dict__["connection_driver"] = infer_driver(self.connection_url)

    @property
    @override
    def _protocol_name(self) -> str:
        return "JDBC_PING"
