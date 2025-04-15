# Stock Portfolio Tracker

A comprehensive stock portfolio tracking application that allows users to manage their stock investments and track performance in real-time using financial market data.

## Features

- **Portfolio Management**: Add and remove stocks from personal portfolio
- **Real-time Data**: Get current stock prices from Alpha Vantage API
- **Performance Tracking**: View gain/loss for individual stocks and overall portfolio
- **Data Visualization**: Visual representation of portfolio composition and stock values
- **Historical Data**: View price history charts for individual stocks
- **Automatic Updates**: Portfolio data refreshes automatically every hour
- **Local Storage**: Portfolio data is saved locally for persistence between sessions

## Screenshots



## Requirements

- Python 3.6+
- Required Python packages (see requirements.txt):
  - tkinter
  - requests
  - matplotlib
  - pandas

## Installation

1. Clone this repository:
```
git https://github.com/farazahmed2048/codealpha_task.git
cd task-2(stock-tracker)
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Get an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

4. Replace the placeholder API key in the code:
```python
self.api_key = " ZKHIYU9Z339WCXAG"
```

## Usage

1. Run the application:
```
python stock_portfolio_tracker.py
```

2. Add stocks to portfolio by clicking the "Add Stock" button
   - Enter the stock symbol (e.g., AAPL for Apple Inc.)
   - Enter the number of shares you own
   - Enter purchase price per share

3. Monitor portfolio:
   - View current values, gain/loss calculations
   - Visualize portfolio composition
   - Track performance over time

4. Remove stocks from portfolio when necessary

5. Click "View Details" to see historical price charts for specific stocks

## How It Works

This application uses the Alpha Vantage API to fetch real-time and historical stock data. The main components include:

1. **Data Fetching**: The application connects to the Alpha Vantage API to retrieve current prices and historical data
2. **Portfolio Management**: Users can create and maintain their stock portfolio
3. **Performance Calculation**: The app calculates current value, gain/loss, and percentage changes
4. **Visualization**: Matplotlib is used to create charts and graphs of portfolio data
5. **Data Persistence**: Portfolio information is stored locally in a JSON file

## API Rate Limits

Please note that the free tier of Alpha Vantage API has the following limitations:
- 5 API requests per minute
- 500 API requests per day

The application includes measures to handle these limitations, but you may experience delays if making many requests in quick succession.

## Future Enhancements

- Add support for multiple currencies
- Implement transaction history tracking
- Add dividend tracking
- Create watchlists for potential investments
- Implement alerts for price movements
- Expand visualization options with more chart types
- Add export functionality for reports

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Alpha Vantage](https://www.alphavantage.co/) for providing financial market data
- [Matplotlib](https://matplotlib.org/) for data visualization capabilities
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
