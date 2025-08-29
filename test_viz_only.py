"""
Simple visualization test for BIST Trading System
"""

import sys
import os
import pandas as pd

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_visualizer import BISTDataVisualizer

def main():
    """Test visualization functionality with sample data"""
    print("Testing BIST Data Visualizer...")
    
    try:
        # Create sample data for testing
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        sample_data = {
            'THYAO.IS': pd.DataFrame({
                'Close': [100 + i * 0.1 for i in range(len(dates))],
                'Volume': [1000000 + i * 1000 for i in range(len(dates))]
            }, index=dates),
            'GARAN.IS': pd.DataFrame({
                'Close': [50 + i * 0.05 for i in range(len(dates))],
                'Volume': [800000 + i * 800 for i in range(len(dates))]
            }, index=dates)
        }
        
        # Initialize visualizer
        visualizer = BISTDataVisualizer()
        
        print("Creating test visualizations...")
        
        # Test price comparison
        print("  - Price comparison chart...")
        visualizer.plot_price_comparison(sample_data, "output/test_price_comparison.png")
        
        # Test volume analysis
        print("  - Volume analysis...")
        visualizer.plot_volume_analysis(sample_data, "output/test_volume_analysis.png")
        
        # Test correlation matrix
        print("  - Correlation matrix...")
        visualizer.plot_correlation_matrix(sample_data, "output/test_correlation.png")
        
        # Test interactive dashboard
        print("  - Interactive dashboard...")
        visualizer.create_interactive_dashboard(sample_data, "output/test_dashboard.html")
        
        print("All visualizations completed successfully!")
        
        # Check output files
        output_files = [f for f in os.listdir("output") if f.startswith("test_")]
        print(f"\nGenerated test files: {len(output_files)}")
        for file in output_files:
            file_path = os.path.join("output", file)
            file_size = os.path.getsize(file_path)
            print(f"  {file} ({file_size:,} bytes)")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
