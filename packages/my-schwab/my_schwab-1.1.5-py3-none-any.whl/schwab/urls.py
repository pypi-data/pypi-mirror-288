class Urls:
    # Base URLs
    redirect_uri = 'https://127.0.0.1'
    BASE = 'https://api.schwabapi.com'
    TRADER = f"{BASE}/trader/v1"
    MARKET_DATA = f"{BASE}/marketdata/v1"

    # Endpoints
    token_url = f"{BASE}/v1/oauth/token"
    accounts_url = f"{TRADER}/accounts"
    all_orders_url = f"{TRADER}/orders"
    quotes_url = f"{MARKET_DATA}/quotes"
    user_preference_url = f"{TRADER}/userPreference"

    def orders_url(self, account_number):
        return f"{self.accounts_url}/{account_number}/orders"

    def preview_order_url(self, account_number):
        return f"{self.accounts_url}/{account_number}/previewOrder"

    def transactions_url(self, account_number):
        return f"{self.accounts_url}/{account_number}/transactions"

    def quote_url(self, symbol):
        return f"{self.MARKET_DATA}/{symbol}/quotes"

    def quotes_url(self, symbols):
        symbols = ','.join(symbols)
        return f"{self.MARKET_DATA}/quotes?symbols={symbols}"

    # TODO: Implement this method
    def pricehistory(self, symbol, period_type='day', period=10, frequency_type='day', frequency=1):
        pass


urls = Urls()