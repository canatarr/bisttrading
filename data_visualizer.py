"""
BIST Trading System - Data Visualization Module
Creates charts and visualizations for downloaded BIST data
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Windows
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import os
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class BISTDataVisualizer:
    """Creates visualizations for BIST ticker data"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style for matplotlib
        try:
            plt.style.use('seaborn-v0_8')
        except:
            plt.style.use('default')
        sns.set_palette("husl")
    
    def plot_price_comparison(self, data_dict: Dict[str, pd.DataFrame], 
                            save_path: str = None) -> None:
        """
        Create a price comparison chart for multiple tickers
        
        Args:
            data_dict: Dictionary of ticker data
            save_path: Path to save the plot (optional)
        """
        try:
            plt.figure(figsize=(15, 8))
            
            for ticker, data in data_dict.items():
                if data is not None and not data.empty:
                    # Normalize prices to start at 100 for comparison
                    normalized_prices = (data['Close'] / data['Close'].iloc[0]) * 100
                    plt.plot(data.index, normalized_prices, label=ticker, linewidth=2)
            
            plt.title('BIST Tickers - Normalized Price Comparison (Base=100)', 
                     fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Normalized Price (Base=100)', fontsize=12)
            plt.legend(fontsize=10)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Price comparison chart saved to {save_path}")
            
            # Don't show plots in non-interactive mode
            plt.close()
            
        except Exception as e:
            logger.error(f"Error creating price comparison chart: {str(e)}")
    
    def plot_volume_analysis(self, data_dict: Dict[str, pd.DataFrame], 
                           save_path: str = None) -> None:
        """
        Create volume analysis charts for all tickers
        
        Args:
            data_dict: Dictionary of ticker data
            save_path: Path to save the plot (optional)
        """
        try:
            num_tickers = len(data_dict)
            fig, axes = plt.subplots(num_tickers, 1, figsize=(15, 4*num_tickers))
            
            if num_tickers == 1:
                axes = [axes]
            
            for i, (ticker, data) in enumerate(data_dict.items()):
                if data is not None and not data.empty:
                    ax = axes[i]
                    
                    # Plot volume bars
                    ax.bar(data.index, data['Volume'], alpha=0.7, color='skyblue')
                    ax.set_title(f'{ticker} - Trading Volume', fontweight='bold')
                    ax.set_ylabel('Volume')
                    ax.grid(True, alpha=0.3)
                    ax.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Volume analysis chart saved to {save_path}")
            
            # Don't show plots in non-interactive mode
            plt.close()
            
        except Exception as e:
            logger.error(f"Error creating volume analysis chart: {str(e)}")
    
    def create_interactive_dashboard(self, data_dict: Dict[str, pd.DataFrame], 
                                   save_path: str = None) -> None:
        """
        Create an interactive Plotly dashboard
        
        Args:
            data_dict: Dictionary of ticker data
            save_path: Path to save the HTML file (optional)
        """
        try:
            # Create subplots
            fig = make_subplots(
                rows=len(data_dict), cols=2,
                subplot_titles=[f"{ticker} - Price & Volume" for ticker in data_dict.keys()],
                specs=[[{"secondary_y": True}] * 2] * len(data_dict)
            )
            
            row = 1
            for ticker, data in data_dict.items():
                if data is not None and not data.empty:
                    # Price chart (left subplot)
                    fig.add_trace(
                        go.Scatter(
                            x=data.index,
                            y=data['Close'],
                            name=f"{ticker} Price",
                            line=dict(color='blue')
                        ),
                        row=row, col=1
                    )
                    
                    # Volume chart (right subplot)
                    fig.add_trace(
                        go.Bar(
                            x=data.index,
                            y=data['Volume'],
                            name=f"{ticker} Volume",
                            marker_color='lightblue'
                        ),
                        row=row, col=2
                    )
                    
                    row += 1
            
            # Update layout
            fig.update_layout(
                title="BIST Trading System - Interactive Dashboard",
                height=300 * len(data_dict),
                showlegend=True
            )
            
            # Update axes labels
            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Price (TL)", secondary_y=False)
            fig.update_yaxes(title_text="Volume", secondary_y=True)
            
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Interactive dashboard saved to {save_path}")
            
            # Don't show plots in non-interactive mode
            # fig.show()
            
        except Exception as e:
            logger.error(f"Error creating interactive dashboard: {str(e)}")
    
    def plot_correlation_matrix(self, data_dict: Dict[str, pd.DataFrame], 
                              save_path: str = None) -> None:
        """
        Create a correlation matrix heatmap for ticker returns
        
        Args:
            data_dict: Dictionary of ticker data
            save_path: Path to save the plot (optional)
        """
        try:
            # Calculate returns for each ticker
            returns_data = {}
            for ticker, data in data_dict.items():
                if data is not None and not data.empty:
                    returns_data[ticker] = data['Close'].pct_change().dropna()
            
            # Create returns DataFrame
            returns_df = pd.DataFrame(returns_data)
            
            # Calculate correlation matrix
            correlation_matrix = returns_df.corr()
            
            # Create heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, 
                       annot=True, 
                       cmap='coolwarm', 
                       center=0,
                       square=True,
                       fmt='.3f')
            
            plt.title('BIST Tickers - Returns Correlation Matrix', 
                     fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Correlation matrix saved to {save_path}")
            
            # Don't show plots in non-interactive mode
            plt.close()
            
        except Exception as e:
            logger.error(f"Error creating correlation matrix: {str(e)}")
    
    def generate_all_visualizations(self, data_dict: Dict[str, pd.DataFrame]) -> None:
        """
        Generate all available visualizations for the data
        
        Args:
            data_dict: Dictionary of ticker data
        """
        try:
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            
            # Price comparison chart
            price_chart_path = os.path.join(self.output_dir, f"price_comparison_{timestamp}.png")
            self.plot_price_comparison(data_dict, price_chart_path)
            
            # Volume analysis
            volume_chart_path = os.path.join(self.output_dir, f"volume_analysis_{timestamp}.png")
            self.plot_volume_analysis(data_dict, volume_chart_path)
            
            # Interactive dashboard
            dashboard_path = os.path.join(self.output_dir, f"interactive_dashboard_{timestamp}.html")
            self.create_interactive_dashboard(data_dict, dashboard_path)
            
            # Correlation matrix
            correlation_path = os.path.join(self.output_dir, f"correlation_matrix_{timestamp}.png")
            self.plot_correlation_matrix(data_dict, correlation_path)
            
            logger.info("All visualizations generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {str(e)}")
