from _typeshed import Incomplete
from enum import Enum

WEBSOCKET_BASE_URI = str
VERSION = str
ARGS_LIMIT = int
MAX_SUBSCRIPTIONS_PER_STREAM_SPOT = int
MAX_SUBSCRIPTIONS_PER_STREAM_LINEAR = int
MAX_SUBSCRIPTIONS_PER_STREAM_INVERSE = int
MAX_SUBSCRIPTIONS_PER_STREAM_OPTION = int

class Exchanges(str, Enum):
    BYBIT: str
    BYBIT_TESTNET: str

CONNECTION_SETTINGS: Incomplete
