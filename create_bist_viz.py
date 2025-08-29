"""
Create BIST data visualizations from downloaded data
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_visualizer import BISTDataVisualizer

def load_downloaded_data():
    """Load the downloaded BIST data"""
    data_dir = "data"
    data_dict = {}
    
    # Load each CSV file
    for file in os.listdir(data_dir):
        if file.endswith('.csv') and not file.startswith('test_'):
            ticker = file.split('_')[0] + '.IS'
            file_path = os.path.join(data_dir, file)
            
            try:
                data = pd.read_csv(file_path, index_col=0, parse_dates=True)
                data_dict[ticker] = data
                print(f"Loaded {ticker}: {len(data)} records")
            except Exception as e:
                print(f"Error loading {file}: {e}")
    
    return data_dict

def main():
    """Main function to create BIST visualizations"""
    print("=" * 60)
    print("BIST TRADING SYSTEM - CREATING VISUALIZATIONS")
    print("=" * 60)
    
    try:
        # Load downloaded data
        print("Loading downloaded BIST data...")
        data_dict = load_downloaded_data()
        
        if not data_dict:
            print("No data found. Please run the download test first.")
            return False
        
        print(f"Loaded {len(data_dict)} tickers: {', '.join(data_dict.keys())}")
        
        # Initialize visualizer
        visualizer = BISTDataVisualizer()
        
        # Create visualizations
        print("\nCreating BIST data visualizations...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Price comparison chart
        print("  - Price comparison chart...")
        price_chart_path = os.path.join("output", f"bist_price_comparison_{timestamp}.png")
        visualizer.plot_price_comparison(data_dict, price_chart_path)
        
        # Volume analysis
        print("  - Volume analysis charts...")
        volume_chart_path = os.path.join("output", f"bist_volume_analysis_{timestamp}.png")
        visualizer.plot_volume_analysis(data_dict, volume_chart_path)
        
        # Correlation matrix
        print("  - Correlation matrix...")
        correlation_path = os.path.join("output", f"bist_correlation_matrix_{timestamp}.png")
        visualizer.plot_correlation_matrix(data_dict, correlation_path)
        
        # Interactive dashboard
        print("  - Interactive dashboard...")
        dashboard_path = os.path.join("output", f"bist_interactive_dashboard_{timestamp}.html")
        visualizer.create_interactive_dashboard(data_dict, dashboard_path)
        
        print("\nAll BIST visualizations completed successfully!")
        
        # Check output files
        output_files = [f for f in os.listdir("output") if f.startswith("bist_")]
        print(f"\nGenerated BIST visualization files: {len(output_files)}")
        for file in output_files:
            file_path = os.path.join("output", file)
            file_size = os.path.getsize(file_path)
            print(f"  {file} ({file_size:,} bytes)")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
