"""
BIST Trading System - Download Test Script
Tests the data download functionality for multiple BIST tickers
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_downloader import BISTDataDownloader
from config.config import BIST_TICKERS, DOWNLOAD_SETTINGS

def main():
    """Main function to test BIST data download"""
    print("=" * 60)
    print("BIST TRADING SYSTEM - DATA DOWNLOAD TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(BIST_TICKERS)} tickers: {', '.join(BIST_TICKERS)}")
    print(f"Period: {DOWNLOAD_SETTINGS['period']}")
    print(f"Interval: {DOWNLOAD_SETTINGS['interval']}")
    print("=" * 60)
    
    try:
        # Initialize downloader
        downloader = BISTDataDownloader()
        
        # Get ticker information first
        print("\n1. Getting ticker information...")
        ticker_info_list = []
        for ticker in BIST_TICKERS:
            info = downloader.get_ticker_info(ticker)
            if info:
                ticker_info_list.append(info)
                print(f"   ✓ {ticker}: {info.get('name', 'N/A')} - {info.get('sector', 'N/A')}")
            else:
                print(f"   ✗ {ticker}: Failed to get info")
        
        # Download data for all tickers
        print(f"\n2. Downloading data for {len(BIST_TICKERS)} tickers...")
        results = downloader.download_multiple_tickers(
            tickers=BIST_TICKERS,
            period=DOWNLOAD_SETTINGS['period'],
            interval=DOWNLOAD_SETTINGS['interval'],
            delay=DOWNLOAD_SETTINGS.get('delay_between_requests', 1.0)
        )
        
        # Display results
        print(f"\n3. Download Results:")
        print("-" * 40)
        successful_downloads = 0
        
        for ticker in BIST_TICKERS:
            if ticker in results and results[ticker] is not None:
                data = results[ticker]
                print(f"   ✓ {ticker}: {len(data)} records")
                print(f"      Date range: {data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}")
                print(f"      Price range: {data['Close'].min():.2f} - {data['Close'].max():.2f}")
                print(f"      Avg Volume: {data['Volume'].mean():,.0f}")
                successful_downloads += 1
            else:
                print(f"   ✗ {ticker}: Download failed")
        
        print(f"\n4. Summary:")
        print(f"   Successful downloads: {successful_downloads}/{len(BIST_TICKERS)}")
        print(f"   Success rate: {(successful_downloads/len(BIST_TICKERS)*100):.1f}%")
        
        # Generate and display summary report
        if results:
            print(f"\n5. Generating summary report...")
            summary_df = downloader.generate_summary_report(results)
            print("\nSummary Report:")
            print(summary_df.to_string(index=False))
        
        # Data quality check
        print(f"\n6. Data Quality Check:")
        print("-" * 40)
        for ticker, data in results.items():
            if data is not None:
                is_valid = downloader.validate_data(data, ticker)
                status = "✓ Valid" if is_valid else "✗ Issues"
                print(f"   {ticker}: {status}")
        
        print(f"\n7. Files saved:")
        print("-" * 40)
        data_files = [f for f in os.listdir("data") if f.endswith('.csv')]
        for file in data_files:
            file_path = os.path.join("data", file)
            file_size = os.path.getsize(file_path)
            print(f"   {file} ({file_size:,} bytes)")
        
        print(f"\n" + "=" * 60)
        print("DOWNLOAD TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Download test failed. Check the logs for more details.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
