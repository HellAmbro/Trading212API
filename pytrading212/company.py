class Company:
    """Company Wrapper"""

    def __init__(self, instrument_code: str, isin: str):
        self.instrument_code = instrument_code
        self.isin = isin
