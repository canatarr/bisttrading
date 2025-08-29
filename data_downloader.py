"""
BIST Trading System - Data Downloader Module
Downloads historical data for BIST tickers using yfinance
"""

import yfinance as yf
import pandas as pd
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
import time

# Setup logging
def setup_logging():
    """Setup logging with proper error handling"""
    try:
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/download.log'),
                logging.StreamHandler()
            ]
        )
    except Exception:
        # Fallback to console-only logging if file logging fails
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )

setup_logging()
logger = logging.getLogger(__name__)

class BISTDataDownloader:
    """Downloads and manages BIST ticker data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("output", exist_ok=True)
    
    def download_ticker_data(self, ticker: str, period: str = "1y", 
                           interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Download data for a single ticker
        
        Args:
            ticker: Ticker symbol (e.g., 'THYAO.IS')
            period: Data period (e.g., '1y', '6mo', '1mo')
            interval: Data interval (e.g., '1d', '1h', '5m')
        
        Returns:
            DataFrame with ticker data or None if failed
        """
        try:
            logger.info(f"Downloading data for {ticker}")
            
            # Create ticker object
            tick = yf.Ticker(ticker)
            
            # Download data
            data = tick.history(period=period, interval=interval)
            
            if data.empty:
                logger.warning(f"No data received for {ticker}")
                return None
            
            # Add ticker symbol column
            data['Ticker'] = ticker
            
            # Save to file
            filename = f"{ticker.replace('.IS', '')}_{period}_{interval}.csv"
            filepath = os.path.join(self.data_dir, filename)
            data.to_csv(filepath)
            
            logger.info(f"Successfully downloaded {len(data)} records for {ticker}")
            logger.info(f"Data saved to {filepath}")
            
            return data
            
        except Exception as e:
            logger.error(f"Error downloading data for {ticker}: {str(e)}")
            return None
    
    def download_multiple_tickers(self, tickers: List[str], 
                                period: str = "1y", 
                                interval: str = "1d",
                                delay: float = 1.0) -> Dict[str, pd.DataFrame]:
        """
        Download data for multiple tickers with delay between requests
        
        Args:
            tickers: List of ticker symbols
            period: Data period
            interval: Data interval
            delay: Delay between requests in seconds
        
        Returns:
            Dictionary mapping ticker symbols to their data
        """
        results = {}
        
        for i, ticker in enumerate(tickers):
            logger.info(f"Processing ticker {i+1}/{len(tickers)}: {ticker}")
            
            data = self.download_ticker_data(ticker, period, interval)
            if data is not None:
                results[ticker] = data
            
            # Add delay between requests to avoid rate limiting
            if i < len(tickers) - 1:  # Don't delay after the last request
                time.sleep(delay)
        
        return results
    
    def get_ticker_info(self, ticker: str) -> Optional[Dict]:
        """Get basic information about a ticker"""
        try:
            tick = yf.Ticker(ticker)
            info = tick.info
            
            # Extract relevant information
            ticker_info = {
                'symbol': ticker,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'currency': info.get('currency', 'N/A')
            }
            
            return ticker_info
            
        except Exception as e:
            logger.error(f"Error getting info for {ticker}: {str(e)}")
            return None
    
    def validate_data(self, data: pd.DataFrame, ticker: str) -> bool:
        """
        Validate downloaded data quality
        
        Args:
            data: Downloaded data DataFrame
            ticker: Ticker symbol for logging
        
        Returns:
            True if data is valid, False otherwise
        """
        if data.empty:
            logger.warning(f"Data for {ticker} is empty")
            return False
        
        # Check for required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            logger.warning(f"Missing columns for {ticker}: {missing_columns}")
            return False
        
        # Check for reasonable data ranges
        if (data['Close'] <= 0).any():
            logger.warning(f"Invalid close prices found for {ticker}")
            return False
        
        # Check for missing values
        missing_count = data.isnull().sum().sum()
        if missing_count > 0:
            logger.warning(f"Found {missing_count} missing values for {ticker}")
        
        logger.info(f"Data validation passed for {ticker}")
        return True
    
    def generate_summary_report(self, results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Generate a summary report of downloaded data"""
        summary_data = []
        
        for ticker, data in results.items():
            if data is not None and not data.empty:
                summary_data.append({
                    'Ticker': ticker,
                    'Records': len(data),
                    'Start_Date': data.index.min().strftime('%Y-%m-%d'),
                    'End_Date': data.index.max().strftime('%Y-%m-%d'),
                    'Min_Close': data['Close'].min(),
                    'Max_Close': data['Close'].max(),
                    'Avg_Volume': data['Volume'].mean(),
                    'Data_Quality': 'Valid' if self.validate_data(data, ticker) else 'Issues'
                })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Save summary report
        summary_file = os.path.join("output", f"download_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        summary_df.to_csv(summary_file, index=False)
        logger.info(f"Summary report saved to {summary_file}")
        
        return summary_df
