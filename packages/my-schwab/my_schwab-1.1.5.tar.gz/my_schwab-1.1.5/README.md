# Schwab

## About

The `my-schwab` API client is a Python package that provides a convenient way to interact with the Schwab API. It allows you to access your Schwab account information, fetch account details, place orders, and retrieve order history. With this client, you can easily integrate Schwab functionality into your Python applications and automate trading strategies. It provides a simple and intuitive interface, making it easy to get started with the Schwab API. Start using the `my-Schwab` API client today and take control of your Schwab account programmatically.

## Installation

You can install the `my-schwab` package using pip. Open your terminal and type:

```bash
pip install my-schwab
```


```python
from schwab import Client

# fetch will fetch your current account and positions
client = Client(fetch=True)

client.place_order('AAPL', qty=1, order_type='limit', side='buy')
orders = client.get_orders()

transactions = client.get_transactions()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.