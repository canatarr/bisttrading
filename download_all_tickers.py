"""
BIST Trading System - Download All Tickers
Downloads data for all BIST tickers starting from 2025, preserving existing data
"""

import sys
import os
import pandas as pd
from datetime import datetime
import time

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_downloader import BISTDataDownloader
from config.config import BIST_TICKERS, DOWNLOAD_SETTINGS

def get_existing_tickers():
    """Get list of tickers that already have data files"""
    data_dir = "data"
    existing_tickers = set()
    
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.csv'):
                # Extract ticker name from filename (e.g., "THYAO_1y_1d.csv" -> "THYAO.IS")
                ticker_name = file.split('_')[0] + '.IS'
                existing_tickers.add(ticker_name)
    
    return existing_tickers

def get_new_tickers_to_download():
    """Get list of tickers that need to be downloaded"""
    existing_tickers = get_existing_tickers()
    new_tickers = []
    
    for ticker in BIST_TICKERS:
        if ticker not in existing_tickers:
            new_tickers.append(ticker)
    
    return new_tickers

def main():
    """Main function to download data for all new tickers"""
    print("=" * 80)
    print("BIST TRADING SYSTEM - DOWNLOAD ALL TICKERS")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total tickers in config: {len(BIST_TICKERS)}")
    print(f"Download period: {DOWNLOAD_SETTINGS['period']} (from {DOWNLOAD_SETTINGS['start_date']})")
    print(f"Download interval: {DOWNLOAD_SETTINGS['interval']}")
    print("=" * 80)
    
    try:
        # Check existing data
        existing_tickers = get_existing_tickers()
        new_tickers = get_new_tickers_to_download()
        
        print(f"\n📊 EXISTING DATA ANALYSIS:")
        print(f"   Existing tickers: {len(existing_tickers)}")
        print(f"   New tickers to download: {len(new_tickers)}")
        
        if existing_tickers:
            print(f"\n   Existing tickers found:")
            for ticker in sorted(existing_tickers):
                print(f"      ✓ {ticker}")
        
        if not new_tickers:
            print(f"\n🎉 All tickers already have data! No new downloads needed.")
            return True
        
        print(f"\n📥 DOWNLOADING NEW TICKERS:")
        print(f"   Will download data for {len(new_tickers)} new tickers")
        print(f"   This may take a while due to the large number of tickers...")
        
        # Initialize downloader
        downloader = BISTDataDownloader()
        
        # Download data for new tickers
        print(f"\n🚀 Starting download process...")
        results = downloader.download_multiple_tickers(
            tickers=new_tickers,
            period=DOWNLOAD_SETTINGS['period'],
            interval=DOWNLOAD_SETTINGS['interval'],
            delay=DOWNLOAD_SETTINGS.get('delay_between_requests', 1.0)
        )
        
        # Display results
        print(f"\n📈 DOWNLOAD RESULTS:")
        print("-" * 60)
        successful_downloads = 0
        failed_downloads = 0
        
        for ticker in new_tickers:
            if ticker in results and results[ticker] is not None:
                data = results[ticker]
                print(f"   ✓ {ticker}: {len(data)} records")
                print(f"      Date range: {data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}")
                print(f"      Price range: {data['Close'].min():.2f} - {data['Close'].max():.2f} TL")
                print(f"      Avg Volume: {data['Volume'].mean():,.0f}")
                successful_downloads += 1
            else:
                print(f"   ✗ {ticker}: Download failed")
                failed_downloads += 1
        
        print(f"\n📊 FINAL SUMMARY:")
        print(f"   Total tickers in system: {len(BIST_TICKERS)}")
        print(f"   Existing tickers: {len(existing_tickers)}")
        print(f"   New successful downloads: {successful_downloads}")
        print(f"   Failed downloads: {failed_downloads}")
        print(f"   Overall success rate: {((len(existing_tickers) + successful_downloads)/len(BIST_TICKERS)*100):.1f}%")
        
        # Generate summary report for new downloads
        if results:
            print(f"\n📋 Generating summary report for new downloads...")
            summary_df = downloader.generate_summary_report(results)
            print("\nSummary Report for New Downloads:")
            print(summary_df.to_string(index=False))
        
        # Final file count
        print(f"\n💾 FINAL FILE COUNT:")
        print("-" * 60)
        data_files = [f for f in os.listdir("data") if f.endswith('.csv')]
        print(f"   Total CSV files in data directory: {len(data_files)}")
        
        # Group files by type
        existing_files = [f for f in data_files if any(ticker.replace('.IS', '') in f for ticker in existing_tickers)]
        new_files = [f for f in data_files if f not in existing_files]
        
        print(f"   Existing files (preserved): {len(existing_files)}")
        print(f"   New files (downloaded): {len(new_files)}")
        
        print(f"\n" + "=" * 80)
        print("🎉 DOWNLOAD PROCESS COMPLETED!")
        print("=" * 80)
        print(f"📁 Check the 'data' folder for all CSV files")
        print(f"📊 Run visualization scripts to analyze the expanded dataset")
        print(f"🔧 The system is now ready for analysis of {len(BIST_TICKERS)} BIST tickers!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Download process failed. Check the logs for more details.")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
