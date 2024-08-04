from _typeshed import Incomplete
from enum import Enum

WEBSOCKET_BASE_URI: type[str]
VERSION: type[str]
ARGS_LIMIT: type[int]
MAX_SUBSCRIPTIONS_PER_STREAM_SPOT: type[int]
MAX_SUBSCRIPTIONS_PER_STREAM_LINEAR: type[int]
MAX_SUBSCRIPTIONS_PER_STREAM_INVERSE: type[int]
MAX_SUBSCRIPTIONS_PER_STREAM_OPTION: type[int]

class Exchanges(str, Enum):
    BYBIT = 'bybit.com'
    BYBIT_TESTNET = 'bybit.com-testnet'

CONNECTION_SETTINGS: Incomplete
