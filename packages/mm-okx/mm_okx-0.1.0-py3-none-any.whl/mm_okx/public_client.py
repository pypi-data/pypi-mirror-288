from mm_std import hr


class PublicClient:
    """
    Public data client, no auth required
    """

    def __init__(self, proxy: str | None = None):
        self.base_url = "https://www.okx.com"
        self.proxy = proxy

    def get_instruments_raw(self, inst_type: str = "SPOT") -> object:
        return hr(f"{self.base_url}/api/v5/public/instruments?instType={inst_type}").json

    def get_instrument_raw(self, inst_id: str, inst_type: str = "SPOT") -> object:
        return hr(f"{self.base_url}/api/v5/public/instruments?instId={inst_id}&instType={inst_type}").json

    def get_tickers_raw(self, inst_type: str = "SPOT") -> object:
        return hr(f"{self.base_url}/api/v5/market/tickers?instType={inst_type}").json

    def get_ticker_raw(self, inst_id: str) -> object:
        return hr(f"{self.base_url}/api/v5/market/ticker?instId={inst_id}").json
