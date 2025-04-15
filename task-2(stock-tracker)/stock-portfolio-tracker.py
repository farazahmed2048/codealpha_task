import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
import os
import threading
import time

class StockPortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")
        
        # API key for Alpha Vantage
        # Note: In a real app, you would store this more securely
        self.api_key = " ZKHIYU9Z339WCXAG"
        
        # Portfolio data
        self.portfolio = []
        self.load_portfolio()
        
        # Create UI
        self.create_widgets()
        
        # Start auto-refresh thread
        self.stop_thread = False
        self.refresh_thread = threading.Thread(target=self.auto_refresh)
        self.refresh_thread.daemon = True
        self.refresh_thread.start()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Stock Portfolio Tracker", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)
        
        # Control frame for portfolio management
        control_frame = ttk.LabelFrame(main_frame, text="Portfolio Management")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add stock button
        add_button = ttk.Button(control_frame, text="Add Stock", command=self.add_stock)
        add_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Remove stock button
        remove_button = ttk.Button(control_frame, text="Remove Stock", command=self.remove_stock)
        remove_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Refresh data button
        refresh_button = ttk.Button(control_frame, text="Refresh Data", command=self.refresh_data)
        refresh_button.grid(row=0, column=2, padx=5, pady=5)
        
        # View details button
        details_button = ttk.Button(control_frame, text="View Details", command=self.view_stock_details)
        details_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Portfolio table
        portfolio_frame = ttk.LabelFrame(main_frame, text="Current Portfolio")
        portfolio_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for portfolio display
        columns = ("Symbol", "Name", "Shares", "Buy Price", "Current Price", "Value", "Gain/Loss", "Gain/Loss %")
        self.portfolio_tree = ttk.Treeview(portfolio_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.portfolio_tree.heading(col, text=col)
            width = 100
            if col == "Name":
                width = 200
            self.portfolio_tree.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(portfolio_frame, orient=tk.VERTICAL, command=self.portfolio_tree.yview)
        self.portfolio_tree.configure(yscroll=scrollbar.set)
        
        # Pack portfolio tree and scrollbar
        self.portfolio_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(main_frame, text="Portfolio Summary")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Summary labels
        self.total_value_label = ttk.Label(summary_frame, text="Total Value: $0.00")
        self.total_value_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.total_gain_label = ttk.Label(summary_frame, text="Total Gain/Loss: $0.00 (0.00%)")
        self.total_gain_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        self.last_update_label = ttk.Label(summary_frame, text="Last Updated: Never")
        self.last_update_label.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
        
        # Bottom frame for charts
        chart_frame = ttk.LabelFrame(main_frame, text="Portfolio Visualization")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure for the charts
        self.figure, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Setup canvas
        self.canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial update
        self.update_portfolio_display()
    
    def add_stock(self):
        # Prompt for stock details
        symbol = simpledialog.askstring("Add Stock", "Enter Stock Symbol (e.g., AAPL):")
        if not symbol:
            return
        
        symbol = symbol.upper()
        
        # Check if stock already exists in portfolio
        for stock in self.portfolio:
            if stock['symbol'] == symbol:
                messagebox.showerror("Error", f"Stock {symbol} already exists in portfolio!")
                return
        
        # Validate symbol using API
        try:
            stock_data = self.fetch_stock_data(symbol)
            if not stock_data:
                messagebox.showerror("Error", f"Could not find stock with symbol {symbol}")
                return
            
            name = stock_data.get('name', symbol)
            current_price = stock_data.get('price', 0.0)
            
            # Get shares and buy price
            shares = simpledialog.askfloat("Add Stock", f"Enter number of shares for {symbol}:", minvalue=0.01)
            if not shares:
                return
            
            buy_price = simpledialog.askfloat("Add Stock", f"Enter purchase price per share for {symbol}:", minvalue=0.01)
            if buy_price is None:
                return
            
            # Add stock to portfolio
            stock_info = {
                'symbol': symbol,
                'name': name,
                'shares': shares,
                'buy_price': buy_price,
                'current_price': current_price
            }
            
            self.portfolio.append(stock_info)
            self.save_portfolio()
            self.update_portfolio_display()
            
            messagebox.showinfo("Success", f"Added {shares} shares of {symbol} to portfolio!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add stock: {str(e)}")
    
    def remove_stock(self):
        # Get selected item
        selected_item = self.portfolio_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a stock to remove!")
            return
        
        # Get symbol from the selected item
        item_values = self.portfolio_tree.item(selected_item[0], 'values')
        symbol = item_values[0]
        
        # Confirm removal
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove {symbol} from portfolio?")
        if not confirm:
            return
        
        # Remove from portfolio
        for i, stock in enumerate(self.portfolio):
            if stock['symbol'] == symbol:
                self.portfolio.pop(i)
                break
        
        self.save_portfolio()
        self.update_portfolio_display()
        messagebox.showinfo("Success", f"Removed {symbol} from portfolio!")
    
    def view_stock_details(self):
        # Get selected item
        selected_item = self.portfolio_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a stock to view details!")
            return
        
        # Get symbol from the selected item
        item_values = self.portfolio_tree.item(selected_item[0], 'values')
        symbol = item_values[0]
        
        # Create a new window for details
        details_window = tk.Toplevel(self.root)
        details_window.title(f"{symbol} Details")
        details_window.geometry("800x600")
        
        # Fetch historical data
        try:
            historical_data = self.fetch_historical_data(symbol)
            
            # Create detail view
            ttk.Label(details_window, text=f"{symbol} Historical Performance", font=("Arial", 16, "bold")).pack(pady=10)
            
            # Create figure for historical chart
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Plot data
            if historical_data:
                dates = [d['date'] for d in historical_data]
                prices = [d['close'] for d in historical_data]
                
                ax.plot(dates, prices)
                ax.set_title(f"{symbol} Price History")
                ax.set_xlabel("Date")
                ax.set_ylabel("Price ($)")
                ax.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                # Add chart to window
                canvas = FigureCanvasTkAgg(fig, master=details_window)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            else:
                ttk.Label(details_window, text="No historical data available").pack(pady=20)
            
        except Exception as e:
            ttk.Label(details_window, text=f"Error fetching details: {str(e)}").pack(pady=20)
    
    def fetch_stock_data(self, symbol):
        """Fetch current stock data from Alpha Vantage API"""
        try:
            # Endpoint for current price (Global Quote)
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            # Extract relevant data
            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                price = float(quote.get('05. price', 0))
                
                # Get company name using OVERVIEW endpoint
                overview_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.api_key}"
                overview_response = requests.get(overview_url)
                overview_data = overview_response.json()
                name = overview_data.get('Name', symbol)
                
                return {
                    'symbol': symbol,
                    'name': name,
                    'price': price
                }
            else:
                if 'Note' in data:
                    print(f"API limit reached: {data['Note']}")
                return None
        except Exception as e:
            print(f"Error fetching stock data: {str(e)}")
            return None
    
    def fetch_historical_data(self, symbol, days=30):
        """Fetch historical stock data from Alpha Vantage API"""
        try:
            # Endpoint for historical data (TIME_SERIES_DAILY)
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                historical_data = []
                
                # Convert to list and sort by date
                for date, values in time_series.items():
                    historical_data.append({
                        'date': date,
                        'open': float(values['1. open']),
                        'high': float(values['2. high']),
                        'low': float(values['3. low']),
                        'close': float(values['4. close']),
                        'volume': int(values['5. volume'])
                    })
                
                # Sort by date
                historical_data.sort(key=lambda x: x['date'])
                
                # Limit to last X days
                return historical_data[-days:]
            else:
                if 'Note' in data:
                    print(f"API limit reached: {data['Note']}")
                return []
        except Exception as e:
            print(f"Error fetching historical data: {str(e)}")
            return []
    
    def refresh_data(self):
        """Refresh stock data for all portfolio items"""
        if not self.portfolio:
            messagebox.showinfo("Info", " portfolio is empty!")
            return
        
        try:
            # Update each stock's current price
            for stock in self.portfolio:
                stock_data = self.fetch_stock_data(stock['symbol'])
                if stock_data:
                    stock['current_price'] = stock_data['price']
            
            self.save_portfolio()
            self.update_portfolio_display()
            
            # Update last refresh time
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_update_label.config(text=f"Last Updated: {now}")
            
            messagebox.showinfo("Success", "Portfolio data refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh data: {str(e)}")
    
    def update_portfolio_display(self):
        """Update the portfolio treeview and summary"""
        # Clear existing items
        for item in self.portfolio_tree.get_children():
            self.portfolio_tree.delete(item)
        
        # Reset summary values
        total_value = 0
        total_cost = 0
        
        # Stock distribution data for pie chart
        stock_values = []
        stock_symbols = []
        
        # Add portfolio items to treeview
        for stock in self.portfolio:
            symbol = stock['symbol']
            name = stock['name']
            shares = stock['shares']
            buy_price = stock['buy_price']
            current_price = stock.get('current_price', buy_price)
            
            # Calculate values
            value = shares * current_price
            cost = shares * buy_price
            gain_loss = value - cost
            gain_loss_percent = (gain_loss / cost) * 100 if cost > 0 else 0
            
            # Format values
            value_str = f"${value:.2f}"
            gain_loss_str = f"${gain_loss:.2f}"
            gain_loss_percent_str = f"{gain_loss_percent:.2f}%"
            
            # Color for gain/loss
            tag = "gain" if gain_loss >= 0 else "loss"
            
            # Insert into treeview
            item_id = self.portfolio_tree.insert(
                "", 
                tk.END, 
                values=(
                    symbol, 
                    name, 
                    f"{shares:.2f}", 
                    f"${buy_price:.2f}", 
                    f"${current_price:.2f}", 
                    value_str, 
                    gain_loss_str, 
                    gain_loss_percent_str
                ),
                tags=(tag,)
            )
            
            # Update totals
            total_value += value
            total_cost += cost
            
            # Add to chart data
            stock_values.append(value)
            stock_symbols.append(symbol)
        
        # Configure tag colors
        self.portfolio_tree.tag_configure("gain", foreground="green")
        self.portfolio_tree.tag_configure("loss", foreground="red")
        
        # Update summary labels
        total_gain_loss = total_value - total_cost
        total_gain_loss_percent = (total_gain_loss / total_cost) * 100 if total_cost > 0 else 0
        
        self.total_value_label.config(text=f"Total Value: ${total_value:.2f}")
        
        gain_loss_text = f"Total Gain/Loss: ${total_gain_loss:.2f} ({total_gain_loss_percent:.2f}%)"
        self.total_gain_label.config(text=gain_loss_text)
        
        if total_gain_loss >= 0:
            self.total_gain_label.config(foreground="green")
        else:
            self.total_gain_label.config(foreground="red")
        
        # Update last update time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_update_label.config(text=f"Last Updated: {now}")
        
        # Update charts
        self.update_charts(stock_symbols, stock_values)
    
    def update_charts(self, symbols, values):
        """Update portfolio visualization charts"""
        # Clear previous charts
        self.ax1.clear()
        self.ax2.clear()
        
        if not symbols:
            self.canvas.draw()
            return
        
        # Pie chart for portfolio composition
        if sum(values) > 0:
            self.ax1.pie(
                values, 
                labels=symbols, 
                autopct='%1.1f%%', 
                startangle=90, 
                shadow=True
            )
            self.ax1.set_title('Portfolio Composition')
            
            # Bar chart for stock values
            self.ax2.bar(symbols, values, color='skyblue')
            self.ax2.set_title('Stock Values')
            self.ax2.set_ylabel('Value ($)')
            self.ax2.tick_params(axis='x', rotation=45)
        
        # Adjust layout
        plt.tight_layout()
        
        # Draw the updated charts
        self.canvas.draw()
    
    def load_portfolio(self):
        """Load portfolio data from file"""
        try:
            if os.path.exists('portfolio.json'):
                with open('portfolio.json', 'r') as f:
                    self.portfolio = json.load(f)
        except Exception as e:
            print(f"Error loading portfolio: {str(e)}")
            self.portfolio = []
    
    def save_portfolio(self):
        """Save portfolio data to file"""
        try:
            with open('portfolio.json', 'w') as f:
                json.dump(self.portfolio, f, indent=4)
        except Exception as e:
            print(f"Error saving portfolio: {str(e)}")
    
    def auto_refresh(self):
        """Auto refresh thread function - refreshes data every hour"""
        while not self.stop_thread:
            time.sleep(3600)  # Sleep for 1 hour
            if not self.stop_thread:
                # Run refresh on main thread
                self.root.after(0, self.refresh_data)
    
    def on_close(self):
        """Handle window close event"""
        self.stop_thread = True
        self.save_portfolio()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockPortfolioTracker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
