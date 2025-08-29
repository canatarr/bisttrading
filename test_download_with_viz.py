"""
BIST Trading System - Enhanced Download Test with Visualization
Downloads BIST ticker data and creates comprehensive visualizations
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_downloader import BISTDataDownloader
from data_visualizer import BISTDataVisualizer
from config.config import BIST_TICKERS, DOWNLOAD_SETTINGS

def main():
    """Main function to test BIST data download and visualization"""
    print("=" * 70)
    print("BIST TRADING SYSTEM - ENHANCED DOWNLOAD & VISUALIZATION TEST")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(BIST_TICKERS)} tickers: {', '.join(BIST_TICKERS)}")
    print(f"Period: {DOWNLOAD_SETTINGS['period']}")
    print(f"Interval: {DOWNLOAD_SETTINGS['interval']}")
    print("=" * 70)
    
    try:
        # Initialize downloader and visualizer
        downloader = BISTDataDownloader()
        visualizer = BISTDataVisualizer()
        
        # Step 1: Get ticker information
        print("\n📊 STEP 1: Getting ticker information...")
        print("-" * 50)
        ticker_info_list = []
        for ticker in BIST_TICKERS:
            info = downloader.get_ticker_info(ticker)
            if info:
                ticker_info_list.append(info)
                print(f"   ✓ {ticker}: {info.get('name', 'N/A')}")
                print(f"      Sector: {info.get('sector', 'N/A')}")
                print(f"      Industry: {info.get('industry', 'N/A')}")
                print(f"      Currency: {info.get('currency', 'N/A')}")
            else:
                print(f"   ✗ {ticker}: Failed to get info")
        
        # Step 2: Download data
        print(f"\n📥 STEP 2: Downloading data for {len(BIST_TICKERS)} tickers...")
        print("-" * 50)
        results = downloader.download_multiple_tickers(
            tickers=BIST_TICKERS,
            period=DOWNLOAD_SETTINGS['period'],
            interval=DOWNLOAD_SETTINGS['interval'],
            delay=DOWNLOAD_SETTINGS.get('delay_between_requests', 1.0)
        )
        
        # Step 3: Display download results
        print(f"\n📈 STEP 3: Download Results Summary")
        print("-" * 50)
        successful_downloads = 0
        
        for ticker in BIST_TICKERS:
            if ticker in results and results[ticker] is not None:
                data = results[ticker]
                print(f"   ✓ {ticker}: {len(data)} records")
                print(f"      Date range: {data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}")
                print(f"      Price range: {data['Close'].min():.2f} - {data['Close'].max():.2f} TL")
                print(f"      Avg Volume: {data['Volume'].mean():,.0f}")
                print(f"      Last Close: {data['Close'].iloc[-1]:.2f} TL")
                successful_downloads += 1
            else:
                print(f"   ✗ {ticker}: Download failed")
        
        print(f"\n📊 Download Summary:")
        print(f"   Successful downloads: {successful_downloads}/{len(BIST_TICKERS)}")
        print(f"   Success rate: {(successful_downloads/len(BIST_TICKERS)*100):.1f}%")
        
        # Step 4: Data validation
        print(f"\n🔍 STEP 4: Data Quality Validation")
        print("-" * 50)
        valid_data = {}
        for ticker, data in results.items():
            if data is not None:
                is_valid = downloader.validate_data(data, ticker)
                status = "✓ Valid" if is_valid else "✗ Issues"
                print(f"   {ticker}: {status}")
                if is_valid:
                    valid_data[ticker] = data
        
        # Step 5: Generate summary report
        if results:
            print(f"\n📋 STEP 5: Generating Summary Report")
            print("-" * 50)
            summary_df = downloader.generate_summary_report(results)
            print("\nSummary Report:")
            print(summary_df.to_string(index=False))
        
        # Step 6: Create visualizations
        if valid_data:
            print(f"\n🎨 STEP 6: Creating Data Visualizations")
            print("-" * 50)
            print("   Generating price comparison chart...")
            visualizer.plot_price_comparison(valid_data)
            
            print("   Generating volume analysis charts...")
            visualizer.plot_volume_analysis(valid_data)
            
            print("   Generating correlation matrix...")
            visualizer.plot_correlation_matrix(valid_data)
            
            print("   Creating interactive dashboard...")
            visualizer.create_interactive_dashboard(valid_data)
            
            print("   All visualizations completed!")
        
        # Step 7: File summary
        print(f"\n💾 STEP 7: Files Generated")
        print("-" * 50)
        
        # Data files
        data_files = [f for f in os.listdir("data") if f.endswith('.csv')]
        print(f"   Data files ({len(data_files)}):")
        for file in data_files:
            file_path = os.path.join("data", file)
            file_size = os.path.getsize(file_path)
            print(f"      {file} ({file_size:,} bytes)")
        
        # Output files
        output_files = [f for f in os.listdir("output") if f.endswith(('.png', '.html', '.csv'))]
        print(f"   Output files ({len(output_files)}):")
        for file in output_files:
            file_path = os.path.join("output", file)
            file_size = os.path.getsize(file_path)
            print(f"      {file} ({file_size:,} bytes)")
        
        # Log files
        if os.path.exists("logs"):
            log_files = [f for f in os.listdir("logs") if f.endswith('.log')]
            print(f"   Log files ({len(log_files)}):")
            for file in log_files:
                file_path = os.path.join("logs", file)
                file_size = os.path.getsize(file_path)
                print(f"      {file} ({file_size:,} bytes)")
        
        print(f"\n" + "=" * 70)
        print("🎉 ENHANCED DOWNLOAD & VISUALIZATION TEST COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"📁 Check the 'data', 'output', and 'logs' folders for generated files")
        print(f"🌐 Open the HTML dashboard file in your browser for interactive charts")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Enhanced test failed. Check the logs for more details.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
