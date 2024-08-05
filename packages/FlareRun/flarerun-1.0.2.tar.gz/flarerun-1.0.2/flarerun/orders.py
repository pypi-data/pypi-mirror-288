# -*- coding: utf-8 -*-
"""
OpenAlgo REST API Documentation
    https://docs.openalgo.in
"""

import requests


class api:
    """
    A class to handle all the API calls to OpenAlgo.
    """

    def __init__(self, api_key, host="http://127.0.0.1:5000", version="v1"):
        """
        Initialize the api object with an API key and optionally a host URL and API version.

        Attributes:
        - api_key (str): User's API key.
        - host (str): Base URL for the API endpoints. Defaults to localhost.
        - version (str): API version. Defaults to "v1".
        """
        self.api_key = api_key
        self.base_url = f"{host}/api/{version}/"
        self.headers = {
            'Content-Type': 'application/json'
        }

    def placeorder(self, *, strategy="Python", symbol, action, exchange, price_type="MARKET", product="MIS", quantity=1, **kwargs):
        """
        Place an order with the given parameters. All parameters after 'strategy' must be named explicitly.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - symbol (str): Trading symbol. Required.
        - action (str): BUY or SELL. Required.
        - exchange (str): Exchange code. Required.
        - price_type (str, optional): Type of price. Defaults to "MARKET".
        - product (str, optional): Product type. Defaults to "MIS".
        - quantity (int, optional): Quantity to trade. Defaults to 1.
        - **kwargs: Optional parameters like price, trigger_price, disclosed_quantity, etc.

        Returns:
        dict: JSON response from the API.
        """
        url = self.base_url + "placeorder"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,  # Default strategy set to "Python"
            "symbol": symbol,
            "action": action,
            "exchange": exchange,
            "pricetype": price_type,
            "product": product,
            "quantity": str(quantity)
        }
        payload.update(kwargs)
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def placesmartorder(self, *, strategy="Python", symbol, action, exchange, price_type="MARKET", product="MIS", quantity=1, position_size, **kwargs):
        """
        Place a smart order that considers the current position size.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - symbol (str): Trading symbol. Required.
        - action (str): BUY or SELL. Required.
        - exchange (str): Exchange code. Required.
        - price_type (str, optional): Type of price. Defaults to "MARKET".
        - product (str, optional): Product type. Defaults to "MIS".
        - quantity (int, optional): Quantity to trade. Defaults to 1.
        - position_size (int): Required position size.
        - **kwargs: Optional parameters like price, trigger_price, disclosed_quantity, etc.

        Returns:
        dict: JSON response from the API.
        """
        url = self.base_url + "placesmartorder"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "symbol": symbol,
            "action": action,
            "exchange": exchange,
            "pricetype": price_type,
            "product": product,
            "quantity": str(quantity),
            "position_size": str(position_size)
        }
        payload.update(kwargs)
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def modifyorder(self, *, order_id, strategy="Python", symbol, action, exchange, price_type="LIMIT", product, quantity, price, **kwargs):
        """
        Modify an existing order.

        Parameters:
        - order_id (str): The ID of the order to modify. Required.
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - symbol (str): Trading symbol. Required.
        - action (str): BUY or SELL. Required.
        - exchange (str): Exchange code. Required.
        - price_type (str, optional): Type of price. Defaults to "LIMIT".
        - product (str): Product type. Required.
        - quantity (int): Quantity to trade. Required.
        - price (float): New price for the order. Required.
        - **kwargs: Optional parameters like trigger_price, disclosed_quantity, etc.

        Returns:
        dict: JSON response from the API.
        """
        url = self.base_url + "modifyorder"
        payload = {
            "apikey": self.api_key,
            "orderid": order_id,
            "strategy": strategy,
            "symbol": symbol,
            "action": action,
            "exchange": exchange,
            "pricetype": price_type,
            "product": product,
            "quantity": str(quantity),
            "price": str(price)
        }
        payload.update(kwargs)
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def cancelorder(self, *, order_id, strategy="Python"):
        """
        Cancel an existing order.

        Parameters:
        - order_id (str): The ID of the order to cancel. Required.
        - strategy (str, optional): The trading strategy name. Defaults to "Python".

        Returns:
        dict: JSON response from the API.
        """
        url = self.base_url + "cancelorder"
        payload = {
            "apikey": self.api_key,
            "orderid": order_id,
            "strategy": strategy
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    

    def closeposition(self, *, strategy="Python"):
        """
        Close all open positions for a given strategy.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".

        Returns:
        dict: JSON response from the API indicating the result of the close position action.
        """
        url = self.base_url + "closeposition"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def cancelallorder(self, *, strategy="Python"):
        """
        Cancel all orders for a given strategy.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".

        Returns:
        dict: JSON response from the API indicating the result of the cancel all orders action.
        """
        url = self.base_url + "cancelallorder"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()


