"""
BIST Trading System - Mega Visualization Creator
Creates comprehensive visualizations for the expanded BIST dataset
"""

import sys
import os
import pandas as pd
from datetime import datetime
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_visualizer import BISTDataVisualizer

def load_all_bist_data():
    """Load all available BIST data files"""
    data_dir = "data"
    data_dict = {}
    
    if not os.path.exists(data_dir):
        print("Data directory not found!")
        return {}
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    print(f"Found {len(csv_files)} CSV files to process...")
    
    for file in csv_files:
        try:
            # Extract ticker name from filename
            ticker_name = file.split('_')[0] + '.IS'
            file_path = os.path.join(data_dir, file)
            
            # Load data
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)
            
            # Basic validation
            if not data.empty and 'Close' in data.columns and 'Volume' in data.columns:
                data_dict[ticker_name] = data
                print(f"  ✓ Loaded {ticker_name}: {len(data)} records")
            else:
                print(f"  ✗ Skipped {ticker_name}: Invalid data format")
                
        except Exception as e:
            print(f"  ✗ Error loading {file}: {e}")
    
    return data_dict

def create_sector_analysis(data_dict):
    """Create sector-based analysis and visualizations"""
    print("\n🏭 Creating sector analysis...")
    
    # Group tickers by sector (you can expand this mapping)
    sector_mapping = {
        'Banks': ['GARAN', 'AKBNK', 'YKBNK', 'SKBNK', 'QNBTR', 'VAKBN'],
        'Airlines': ['THYAO', 'TUKAS', 'PGSUS'],
        'Steel': ['KRDMD', 'KRDMA', 'KRDMB', 'EREGL'],
        'Technology': ['ASELS', 'LOGO', 'NETAS', 'KAREL'],
        'Energy': ['TUPRS', 'TATEN', 'AYGAZ', 'NTGAZ'],
        'Food': ['ULKER', 'SASA', 'BIMAS', 'MGROS'],
        'Automotive': ['TOASO', 'FROTO', 'TMSN', 'OTKAR'],
        'Real Estate': ['AGYO', 'ASGYO', 'KRGYO', 'VKGYO']
    }
    
    # Create sector performance analysis
    sector_performance = {}
    
    for sector, tickers in sector_mapping.items():
        sector_data = []
        for ticker in tickers:
            ticker_full = ticker + '.IS'
            if ticker_full in data_dict:
                data = data_dict[ticker_full]
                if not data.empty and 'Close' in data.columns:
                    # Calculate normalized performance
                    normalized = (data['Close'] / data['Close'].iloc[0]) * 100
                    sector_data.append(normalized)
        
        if sector_data:
            # Average sector performance
            sector_df = pd.concat(sector_data, axis=1).mean(axis=1)
            sector_performance[sector] = sector_df
    
    return sector_performance

def create_market_overview(data_dict):
    """Create market overview visualizations"""
    print("\n📊 Creating market overview...")
    
    # Calculate market statistics
    market_stats = []
    
    for ticker, data in data_dict.items():
        if not data.empty and 'Close' in data.columns:
            try:
                stats = {
                    'Ticker': ticker,
                    'Records': len(data),
                    'Start_Date': data.index.min().strftime('%Y-%m-%d'),
                    'End_Date': data.index.max().strftime('%Y-%m-%d'),
                    'Min_Close': data['Close'].min(),
                    'Max_Close': data['Close'].max(),
                    'Last_Close': data['Close'].iloc[-1],
                    'Total_Return': ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100,
                    'Avg_Volume': data['Volume'].mean() if 'Volume' in data.columns else 0,
                    'Volatility': data['Close'].pct_change().std() * np.sqrt(252) * 100
                }
                market_stats.append(stats)
            except Exception as e:
                print(f"  Error calculating stats for {ticker}: {e}")
    
    return pd.DataFrame(market_stats)

def main():
    """Main function to create comprehensive BIST visualizations"""
    print("=" * 80)
    print("BIST TRADING SYSTEM - MEGA VISUALIZATION CREATOR")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    try:
        # Load all BIST data
        print("📂 Loading BIST data files...")
        data_dict = load_all_bist_data()
        
        if not data_dict:
            print("❌ No data found. Please run the download script first.")
            return False
        
        print(f"\n✅ Successfully loaded {len(data_dict)} tickers")
        
        # Initialize visualizer
        visualizer = BISTDataVisualizer()
        
        # Create timestamp for file naming
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        print(f"\n🎨 Creating comprehensive visualizations...")
        
        # 1. Market Overview Dashboard
        print("  1. Creating market overview dashboard...")
        market_stats = create_market_overview(data_dict)
        
        # Save market statistics
        stats_file = os.path.join("output", f"market_overview_{timestamp}.csv")
        market_stats.to_csv(stats_file, index=False)
        print(f"     Market statistics saved to {stats_file}")
        
        # 2. Sector Analysis
        print("  2. Creating sector analysis...")
        sector_performance = create_sector_analysis(data_dict)
        
        # 3. Top Performers Visualization
        print("  3. Creating top performers analysis...")
        if not market_stats.empty:
            # Top 20 performers by total return
            top_performers = market_stats.nlargest(20, 'Total_Return')
            top_tickers = top_performers['Ticker'].tolist()
            
            # Create visualization for top performers
            top_data = {ticker: data_dict[ticker] for ticker in top_tickers if ticker in data_dict}
            if top_data:
                top_viz_path = os.path.join("output", f"top_performers_{timestamp}.png")
                visualizer.plot_price_comparison(top_data, top_viz_path)
                print(f"     Top performers chart saved to {top_viz_path}")
        
        # 4. Market Breadth Analysis
        print("  4. Creating market breadth analysis...")
        if not market_stats.empty:
            # Calculate market breadth (advancing vs declining)
            advancing = len(market_stats[market_stats['Total_Return'] > 0])
            declining = len(market_stats[market_stats['Total_Return'] < 0])
            flat = len(market_stats[market_stats['Total_Return'] == 0])
            
            print(f"     Market Breadth: {advancing} advancing, {declining} declining, {flat} flat")
        
        # 5. Volatility Analysis
        print("  5. Creating volatility analysis...")
        if not market_stats.empty:
            # Top 20 most volatile stocks
            volatile_stocks = market_stats.nlargest(20, 'Volatility')
            volatile_file = os.path.join("output", f"most_volatile_{timestamp}.csv")
            volatile_stocks.to_csv(volatile_file, index=False)
            print(f"     Volatility analysis saved to {volatile_file}")
        
        # 6. Volume Leaders
        print("  6. Creating volume analysis...")
        if not market_stats.empty:
            # Top 20 by average volume
            volume_leaders = market_stats.nlargest(20, 'Avg_Volume')
            volume_file = os.path.join("output", f"volume_leaders_{timestamp}.csv")
            volume_leaders.to_csv(volume_file, index=False)
            print(f"     Volume leaders saved to {volume_file}")
        
        # 7. Correlation Matrix for Major Stocks
        print("  7. Creating correlation matrix...")
        # Select major stocks (top 50 by market cap or volume)
        major_stocks = market_stats.nlargest(50, 'Avg_Volume')
        major_tickers = major_stocks['Ticker'].tolist()
        major_data = {ticker: data_dict[ticker] for ticker in major_tickers if ticker in data_dict}
        
        if len(major_data) > 1:
            correlation_path = os.path.join("output", f"major_stocks_correlation_{timestamp}.png")
            visualizer.plot_correlation_matrix(major_data, correlation_path)
            print(f"     Correlation matrix saved to {correlation_path}")
        
        # 8. Interactive Dashboard
        print("  8. Creating interactive dashboard...")
        # Use a subset for the dashboard (top 30 stocks)
        dashboard_tickers = market_stats.nlargest(30, 'Avg_Volume')['Ticker'].tolist()
        dashboard_data = {ticker: data_dict[ticker] for ticker in dashboard_tickers if ticker in data_dict}
        
        if dashboard_data:
            dashboard_path = os.path.join("output", f"mega_dashboard_{timestamp}.html")
            visualizer.create_interactive_dashboard(dashboard_data, dashboard_path)
            print(f"     Interactive dashboard saved to {dashboard_path}")
        
        # Final summary
        print(f"\n📊 VISUALIZATION SUMMARY:")
        print("-" * 60)
        output_files = [f for f in os.listdir("output") if f.startswith(('market_', 'top_', 'most_', 'volume_', 'major_', 'mega_'))]
        print(f"   Generated analysis files: {len(output_files)}")
        
        for file in output_files:
            file_path = os.path.join("output", file)
            file_size = os.path.getsize(file_path)
            print(f"     {file} ({file_size:,} bytes)")
        
        print(f"\n" + "=" * 80)
        print("🎉 MEGA VISUALIZATION CREATION COMPLETED!")
        print("=" * 80)
        print(f"📊 Analyzed {len(data_dict)} BIST tickers")
        print(f"📁 Check the 'output' folder for all analysis files")
        print(f"🌐 Open the HTML dashboard for interactive analysis")
        print(f"📈 The system now provides comprehensive BIST market analysis!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Visualization creation failed. Check the logs for more details.")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
