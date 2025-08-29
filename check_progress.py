"""
BIST Trading System - Progress Checker
Check the progress of ticker downloads and data status
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config.config import BIST_TICKERS

def check_download_progress():
    """Check the current download progress"""
    data_dir = "data"
    
    print("=" * 80)
    print("BIST TRADING SYSTEM - DOWNLOAD PROGRESS CHECKER")
    print("=" * 80)
    print(f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Get existing files
    existing_files = []
    if os.path.exists(data_dir):
        existing_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    # Extract ticker names from filenames
    downloaded_tickers = set()
    for file in existing_files:
        ticker_name = file.split('_')[0] + '.IS'
        downloaded_tickers.add(ticker_name)
    
    # Find missing tickers
    missing_tickers = set(BIST_TICKERS) - downloaded_tickers
    
    # Calculate progress
    total_tickers = len(BIST_TICKERS)
    downloaded_count = len(downloaded_tickers)
    missing_count = len(missing_tickers)
    progress_percentage = (downloaded_count / total_tickers) * 100
    
    print(f"\n📊 PROGRESS SUMMARY:")
    print(f"   Total tickers configured: {total_tickers}")
    print(f"   Downloaded tickers: {downloaded_count}")
    print(f"   Missing tickers: {missing_count}")
    print(f"   Progress: {progress_percentage:.1f}%")
    
    # Progress bar
    progress_bar_length = 50
    filled_length = int(progress_bar_length * progress_percentage / 100)
    progress_bar = "█" * filled_length + "░" * (progress_bar_length - filled_length)
    print(f"   Progress: [{progress_bar}] {progress_percentage:.1f}%")
    
    # Show existing tickers
    if downloaded_tickers:
        print(f"\n✅ DOWNLOADED TICKERS ({len(downloaded_tickers)}):")
        print("-" * 60)
        for ticker in sorted(downloaded_tickers):
            # Find corresponding file
            file = next((f for f in existing_files if ticker.replace('.IS', '') in f), None)
            if file:
                file_path = os.path.join(data_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"   ✓ {ticker} - {file} ({file_size:,} bytes)")
    
    # Show missing tickers (first 20)
    if missing_tickers:
        print(f"\n❌ MISSING TICKERS ({len(missing_tickers)}):")
        print("-" * 60)
        missing_list = sorted(list(missing_tickers))
        for i, ticker in enumerate(missing_list[:20]):
            print(f"   ✗ {ticker}")
        
        if len(missing_tickers) > 20:
            print(f"   ... and {len(missing_tickers) - 20} more")
    
    # File size analysis
    if existing_files:
        print(f"\n💾 FILE SIZE ANALYSIS:")
        print("-" * 60)
        total_size = 0
        for file in existing_files:
            file_path = os.path.join(data_dir, file)
            file_size = os.path.getsize(file_path)
            total_size += file_size
        
        print(f"   Total files: {len(existing_files)}")
        print(f"   Total size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        print(f"   Average file size: {total_size/len(existing_files):,.0f} bytes")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print("-" * 60)
    
    if progress_percentage == 100:
        print("   🎉 All tickers downloaded! Run 'python create_mega_viz.py' for analysis.")
    elif progress_percentage > 50:
        print("   🚀 Good progress! Continue with 'python download_all_tickers.py'")
        print("   📊 You can start analysis with existing data using 'python create_mega_viz.py'")
    elif progress_percentage > 0:
        print("   📥 Some tickers downloaded. Continue with 'python download_all_tickers.py'")
        print("   ⏰ Downloading 500+ tickers may take 1-2 hours")
    else:
        print("   🚀 No tickers downloaded yet. Start with 'python download_all_tickers.py'")
        print("   ⏰ This will download data for all 500+ BIST tickers")
    
    print(f"\n" + "=" * 80)
    
    return {
        'total': total_tickers,
        'downloaded': downloaded_count,
        'missing': missing_count,
        'progress': progress_percentage
    }

def main():
    """Main function"""
    try:
        progress = check_download_progress()
        return True
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
