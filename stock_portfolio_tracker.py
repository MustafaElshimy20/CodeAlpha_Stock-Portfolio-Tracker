import requests
import pandas as pd

API_KEY = 'QMQ9V1Y1Q0RVUQI2'  # Replace with your Alpha Vantage API key

class StockPortfolio:
    def __init__(self):
        self.portfolio = pd.DataFrame(columns=['Symbol', 'Quantity', 'Price'])

    def add_stock(self, symbol, quantity):
        price = self.get_stock_price(symbol)
        if price:
            new_stock = pd.DataFrame({'Symbol': [symbol], 'Quantity': [quantity], 'Price': [price]})
            if not self.portfolio.empty:
                self.portfolio = pd.concat([self.portfolio, new_stock], ignore_index=True)
            else:
                self.portfolio = new_stock
            print(f"Added {quantity} shares of {symbol} at ${price:.2f} each to the portfolio.")

    def remove_stock(self, symbol):
        if symbol in self.portfolio['Symbol'].values:
            self.portfolio = self.portfolio[self.portfolio.Symbol != symbol]
            print(f"Removed {symbol} from the portfolio.")
        else:
            print(f"{symbol} not found in the portfolio.")

    def get_stock_price(self, symbol):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        try:
            price = float(data['Global Quote']['05. price'])
            return price
        except KeyError:
            print(f"Error fetching data for {symbol}. Please check the stock symbol.")
            return None

    def track_portfolio(self):
        self.portfolio['Current Price'] = self.portfolio['Symbol'].apply(self.get_stock_price)
        self.portfolio['Value'] = self.portfolio['Quantity'] * self.portfolio['Current Price']
        total_value = self.portfolio['Value'].sum()
        print("\nCurrent Portfolio:")
        print(self.portfolio)
        print(f"\nTotal portfolio value: ${total_value:.2f}")

    def show_menu(self):
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Portfolio")
        print("4. Exit")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Choose an option: ")
            if choice == '1':
                symbol = input("Enter stock symbol: ").upper()
                quantity = int(input("Enter quantity: "))
                self.add_stock(symbol, quantity)
            elif choice == '2':
                symbol = input("Enter stock symbol to remove: ").upper()
                self.remove_stock(symbol)
            elif choice == '3':
                self.track_portfolio()
            elif choice == '4':
                print("Exiting the tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    portfolio = StockPortfolio()
    portfolio.run()
