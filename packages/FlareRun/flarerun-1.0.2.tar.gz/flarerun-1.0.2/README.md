# OpenAlgo - Python API Client for Automated Trading

## About OpenAlgo

OpenAlgo is a self-hosted, Python-based platform designed to automate trading orders efficiently and effortlessly. Developed using the Flask framework and Tailwind CSS, OpenAlgo offers a user-friendly interface and leverages a robust SQLite database for local data management. Whether running on a personal desktop, laptop, or deployed on a server, OpenAlgo provides the flexibility required for various trading setups.

Download OpenAlgo from GitHub to get started with automating your trading strategies today.

## Key Features

- **Smart Order Placement:** Execute trades swiftly and efficiently with advanced order placement capabilities.
- **Automated Square-off:** Utilize one-click and time-based auto square-off functionalities to optimize trading outcomes.
- **Local Data Storage:** Ensure maximum privacy and control with your data securely stored on your local device.
- **Interactive UI Interface:** Enjoy a seamless trading experience with a clean and intuitive user interface.
- **Comprehensive API Log Management:** Analyze and refine your trading strategies with detailed log management.
- **Versatile API Access:** Supports local API access, Ngrok based internet access, and hosted API access for flexible connectivity.
- **Data Ownership:** Maintain complete ownership of your data, affirming OpenAlgo's commitment to privacy and control.
- **Rapid Execution:** Minimize slippage and maximize potential with faster trade execution.
- **Custom Webhook URL:** Customize and integrate with your preferred trading applications through webhook URLs.

## License

OpenAlgo is licensed under the MIT License. See the LICENSE file for more details.

## Documentation

For a detailed understanding of each API's behavior and capabilities, refer to the [OpenAlgo REST API Documentation](https://docs.openalgo.in/api-documentation/v1).

## Installation

### Install from PyPI

```bash
pip install openalgo
```

## Getting Started

After installation, import OpenAlgo and initialize the API client with your credentials:

```python
from openalgo.orders import api

# Initialize the API client
my_api = api(api_key="your_api_key")
```

## Creating an API Object

To create an API object, provide your API key, and optionally, the host URL and API version:

```python
my_api = api(api_key="your_api_key_here", host="http://127.0.0.1:5000", version="v1")
```

## Using Object Methods

Utilize the methods by calling them with the necessary parameters. Here are some examples:

### Place an Order

```python
response = my_api.placeorder(symbol="RELIANCE-EQ", action="BUY", exchange="NSE", quantity=1)
print(response)
```

### Modify an Order

```python
response = my_api.modifyorder(order_id="12345678", symbol="INFY-EQ", action="SELL", exchange="NSE", product="CNC", quantity=2, price=1500)
print(response)
```

### Cancel an Order

```python
response = my_api.cancelorder(order_id="12345678")
print(response)
```

### Close a Position

```python
response = my_api.closeposition(strategy="MyStrategy")
print(response)
```

### Cancel All Orders

```python
response = my_api.cancelallorder(strategy="MyStrategy")
print(response)
```

For more detailed usage and additional methods, refer to the [OpenAlgo REST API Documentation](https://docs.openalgo.in/api-documentation/v1)
