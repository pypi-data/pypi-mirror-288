from ._connection import ElasticSearchConnection, ElasticSearchSession

connect = connection = Connect = Connection = ElasticSearchConnection
session = Session = ElasticSearchSession

__all__ = [
    "connect",
    "connection",
    "Connect",
    "Connection",
    "ElasticSearchConnection",
    "session",
    "Session",
    "ElasticSearchSession"
]
