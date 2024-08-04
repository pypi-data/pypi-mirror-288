import logging
from _typeshed import Incomplete

__logger__: logging.getLogger
logger = __logger__

class BybitWebSocketApiRestclient:
    threading_lock: Incomplete
    debug: Incomplete
    disable_colorama: Incomplete
    exchange: Incomplete
    lucit_api_secret: Incomplete
    lucit_license_ini: Incomplete
    lucit_license_profile: Incomplete
    lucit_license_token: Incomplete
    restful_base_uri: Incomplete
    show_secrets_in_logs: Incomplete
    socks5_proxy_server: Incomplete
    socks5_proxy_user: Incomplete
    socks5_proxy_pass: Incomplete
    socks5_proxy_ssl_verification: Incomplete
    stream_list: Incomplete
    warn_on_update: Incomplete
    sigterm: bool
    def __init__(self, debug: bool | None = False, disable_colorama: bool | None = False, exchange: str | None = 'bybit.com', lucit_api_secret: str | None = None, lucit_license_ini: str = None, lucit_license_profile: str | None = None, lucit_license_token: str | None = None, restful_base_uri: str | None = None, show_secrets_in_logs: bool | None = False, socks5_proxy_server: str | None = None, socks5_proxy_user: str | None = None, socks5_proxy_pass: str | None = None, socks5_proxy_ssl_verification: bool | None = True, stream_list: dict = None, warn_on_update: bool | None = True) -> None: ...
    def get_symbols(self): ...
