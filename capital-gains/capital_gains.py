from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Base URLs for stocks services
STOCKS1_URL = os.getenv("STOCKS1_URL", "http://stocks1:5001")
STOCKS2_URL = os.getenv("STOCKS2_URL", "http://stocks2:5002")

# Function to fetch stocks from a specific service
def fetch_stocks(service_url, filters=None):
    try:
        url = f"{service_url}/stocks"
        response = requests.get(url, params=filters)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stocks: {e}")
        return []

# Function to fetch the current price of a stock
def get_current_price(symbol):
    api_key = os.getenv("NINJA_API_KEY")
    url = f"https://api.api-ninjas.com/v1/stockprice?ticker={symbol}"
    try:
        response = requests.get(url, headers={"X-Api-Key": api_key})
        response.raise_for_status()
        data = response.json()
        
        # Handle dictionary response
        if isinstance(data, dict):
            return data.get("price", 0)
        # Handle list response
        elif isinstance(data, list) and len(data) > 0:
            return data[0].get("price", 0)
        else:
            return 0  # Return 0 if no data is available
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current price for {symbol}: {e}")
        return 0

@app.route("/capital-gains", methods=["GET"])
def calculate_capital_gains():
    # Query parameters
    portfolio = request.args.get('portfolio')
    numshares_gt = request.args.get('numsharesgt', type=int)
    numshares_lt = request.args.get('numshareslt', type=int)

    # Determine which portfolio to query
    stocks = []
    if portfolio == "stocks1":
        stocks.extend(fetch_stocks(STOCKS1_URL))
    elif portfolio == "stocks1_2":
        stocks.extend(fetch_stocks(STOCKS1_URL))
    elif portfolio == "stocks2":
        stocks.extend(fetch_stocks(STOCKS2_URL))
    else:
        stocks.extend(fetch_stocks(STOCKS1_URL))
        stocks.extend(fetch_stocks(STOCKS2_URL))  # Include stocks2 portfolio

    # Filter stocks by number of shares
    if numshares_gt is not None:
        stocks = [stock for stock in stocks if stock['shares'] > numshares_gt]
    if numshares_lt is not None:
        stocks = [stock for stock in stocks if stock['shares'] < numshares_lt]

    # Calculate capital gains
    total_gains = 0
    gains_details = []
    for stock in stocks:
        symbol = stock["symbol"]
        current_price = get_current_price(symbol)  # Fetch current price
        if current_price is None:
            current_price = 0  # Handle API failure case
        purchase_price = stock['purchase price']
        shares = stock['shares']
        gain = (current_price - purchase_price) * shares
        total_gains += gain
        gains_details.append({
            "symbol": symbol,
            "current_price": current_price,
            "gain": round(gain, 2)
        })

    return jsonify({
        "total_gains": round(total_gains, 2),
        "details": gains_details
    }), 200

@app.route('/kill', methods=['GET'])
def kill_container():
    os._exit(1)

if __name__ == "__main__":
    port = os.getenv("PORT", 5003)
    app.run(host="0.0.0.0", port=port, debug=True)
