# BIST Trading System - Extended Edition

A comprehensive Python-based system for downloading, analyzing, and visualizing BIST (Borsa Istanbul) stock market data for **ALL major BIST tickers**.

## 🚀 Features

- **Complete Coverage**: Downloads data for **500+ BIST tickers** starting from 2025
- **Data Preservation**: Keeps existing data for original 5 tickers, adds new ones
- **Advanced Analysis**: Sector analysis, market breadth, volatility analysis
- **Comprehensive Visualizations**: Multiple chart types, interactive dashboards
- **Data Validation**: Comprehensive data quality checks and validation
- **Professional Charts**: Matplotlib and Plotly visualizations
- **Logging**: Detailed logging for debugging and monitoring
- **Configurable**: Easy-to-modify configuration for tickers and download parameters

## 📊 Supported Tickers

The system now covers **ALL major BIST tickers** including:

### **Original 5 Tickers** (Data preserved from previous runs)
- **THYAO.IS** - Turkish Airlines
- **GARAN.IS** - Garanti Bank
- **AKBNK.IS** - Akbank
- **ASELS.IS** - Aselsan
- **KRDMD.IS** - KARDEMIR

### **New Tickers Added** (500+ additional tickers)
- **Banks**: YKBNK, SKBNK, QNBTR, VAKBN, and more
- **Technology**: LOGO, NETAS, KAREL, and more
- **Energy**: TUPRS, TATEN, AYGAZ, NTGAZ, and more
- **Food & Retail**: ULKER, SASA, BIMAS, MGROS, and more
- **Automotive**: TOASO, FROTO, TMSN, OTKAR, and more
- **Real Estate**: AGYO, ASGYO, KRGYO, VKGYO, and more
- **And many more sectors...**

## 🛠️ Installation

1. **Navigate to the project directory:**
   ```bash
   cd C:\Users\havva\bist-trading-system
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Project Structure

```
bist-trading-system/
├── config/
│   └── config.py              # Configuration with ALL tickers
├── src/
│   ├── data_downloader.py     # Data download functionality
│   └── data_visualizer.py     # Data visualization tools
├── data/                      # All CSV files (500+ tickers)
├── output/                    # Generated charts and reports
├── logs/                      # Log files
├── tests/                     # Test files
├── download_all_tickers.py    # Download ALL new tickers
├── create_mega_viz.py        # Create comprehensive visualizations
├── test_download.py           # Basic download test (original 5)
├── test_download_with_viz.py  # Enhanced test with visualization
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🚀 Usage

### **Phase 1: Download All Tickers** (New!)

Download data for all 500+ BIST tickers starting from 2025:

```bash
python download_all_tickers.py
```

This will:
- ✅ **Preserve existing data** for the first 5 tickers
- 📥 **Download new data** for all additional tickers
- 📊 **Generate summary reports** for new downloads
- 🔍 **Validate data quality** for all tickers

### **Phase 2: Create Mega Visualizations** (New!)

Generate comprehensive analysis for the entire BIST market:

```bash
python create_mega_viz.py
```

This will create:
- 📊 **Market Overview Dashboard** with statistics for all tickers
- 🏭 **Sector Analysis** by industry groups
- 🏆 **Top Performers Analysis** (best performing stocks)
- 📈 **Market Breadth Analysis** (advancing vs declining)
- ⚡ **Volatility Analysis** (most volatile stocks)
- 📊 **Volume Leaders Analysis** (highest volume stocks)
- 🔗 **Correlation Matrix** for major stocks
- 🌐 **Interactive Mega Dashboard** with top 30 stocks

### **Original Functions** (Still Available)

- **Basic Download Test**: `python test_download.py`
- **Enhanced Test**: `python test_download_with_viz.py`
- **Quick Test**: `python quick_test.py`

## ⚙️ Configuration

Edit `config/config.py` to modify:

- **Ticker symbols**: All 500+ BIST tickers are configured
- **Download period**: Set to "ytd" (year-to-date from 2025)
- **Data interval**: Daily data (1d)
- **API settings**: Adjust timeouts and retry attempts

## 📊 Output Files

### **Data Files**
- CSV files with historical data for **500+ tickers**
- Located in the `data/` folder
- Naming format: `{TICKER}_{PERIOD}_{INTERVAL}.csv`

### **Analysis Files** (New!)
- **Market Overview**: Complete statistics for all tickers
- **Sector Analysis**: Performance by industry sectors
- **Top Performers**: Best performing stocks analysis
- **Volatility Analysis**: Most volatile stocks
- **Volume Leaders**: Highest volume stocks
- **Correlation Matrix**: Relationships between major stocks

### **Visualization Files**
- **PNG charts**: Static charts for various analyses
- **HTML dashboards**: Interactive Plotly dashboards
- **Summary reports**: CSV files with comprehensive statistics
- Located in the `output/` folder

## 🔍 Data Validation

The system automatically validates downloaded data for:

- **Completeness**: Required columns (Open, High, Low, Close, Volume)
- **Data quality**: Reasonable price ranges and volume values
- **Missing values**: Identification of gaps in data
- **Format consistency**: Proper data types and structure

## 📈 Advanced Analysis Features

### **Market Overview**
- Total return calculations for all tickers
- Volatility analysis (annualized)
- Volume analysis and rankings
- Date range validation

### **Sector Analysis**
- Grouped by industry sectors
- Sector performance comparisons
- Normalized price analysis

### **Market Breadth**
- Advancing vs declining stocks
- Market sentiment indicators
- Performance distribution analysis

### **Risk Analysis**
- Volatility rankings
- Correlation analysis
- Sector diversification insights

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Data Download Failures**: Check internet connection and ticker symbols

3. **Memory Issues**: With 500+ tickers, ensure sufficient RAM

4. **Time Considerations**: Downloading 500+ tickers may take 1-2 hours

### Log Files
Check the `logs/` folder for detailed error information and debugging details.

## 🔧 Customization

### Adding New Tickers
1. Edit `config/config.py`
2. Add new ticker symbols to `BIST_TICKERS` list
3. Ensure ticker symbols end with `.IS` for BIST

### Modifying Analysis Parameters
1. Edit the analysis scripts to change:
   - Number of top performers displayed
   - Sector groupings
   - Correlation matrix size
   - Dashboard ticker selection

## 📝 License

This project is for educational and research purposes. Please ensure compliance with data usage terms and regulations.

## 🤝 Contributing

Feel free to extend the system with:
- Additional technical indicators
- Backtesting capabilities
- Real-time data feeds
- Portfolio management tools
- Risk analysis features
- Machine learning models
- Alternative data sources

## 📞 Support

For issues or questions:
1. Check the log files in the `logs/` folder
2. Review the configuration in `config/config.py`
3. Ensure all dependencies are properly installed
4. Check available memory for large datasets

---

## 🎯 **System Capabilities Summary**

- **📊 Coverage**: 500+ BIST tickers
- **📅 Time Range**: From January 2025 onwards
- **📈 Analysis**: Comprehensive market analysis
- **🎨 Visualizations**: Professional charts and dashboards
- **🔍 Validation**: Data quality assurance
- **📁 Storage**: Efficient CSV file management
- **⚡ Performance**: Optimized for large datasets

**Happy Trading with the Complete BIST Market! 📈🚀**
