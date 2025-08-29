"""
Quick test script to verify BIST Trading System setup
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test basic imports
        import pandas as pd
        print("✓ pandas imported successfully")
        
        import numpy as np
        print("✓ numpy imported successfully")
        
        import yfinance as yf
        print("✓ yfinance imported successfully")
        
        # Test custom modules
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from data_downloader import BISTDataDownloader
        print("✓ BISTDataDownloader imported successfully")
        
        from data_visualizer import BISTDataVisualizer
        print("✓ BISTDataVisualizer imported successfully")
        
        from config.config import BIST_TICKERS, DOWNLOAD_SETTINGS
        print("✓ Configuration imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_configuration():
    """Test configuration values"""
    print("\nTesting configuration...")
    
    try:
        from config.config import BIST_TICKERS, DOWNLOAD_SETTINGS
        
        print(f"✓ Found {len(BIST_TICKERS)} tickers: {', '.join(BIST_TICKERS)}")
        print(f"✓ Download period: {DOWNLOAD_SETTINGS['period']}")
        print(f"✓ Download interval: {DOWNLOAD_SETTINGS['interval']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_directories():
    """Test if required directories exist or can be created"""
    print("\nTesting directories...")
    
    required_dirs = ['data', 'output', 'logs', 'src', 'config']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ Directory '{dir_name}' exists")
        else:
            print(f"✗ Directory '{dir_name}' missing")
            return False
    
    return True

def test_yfinance_connection():
    """Test basic yfinance connectivity"""
    print("\nTesting yfinance connection...")
    
    try:
        import yfinance as yf
        
        # Test with a simple ticker
        ticker = yf.Ticker("THYAO.IS")
        info = ticker.info
        
        if info and 'longName' in info:
            print(f"✓ Successfully connected to yfinance")
            print(f"  Test ticker: THYAO.IS - {info.get('longName', 'N/A')}")
            return True
        else:
            print("✗ No data received from yfinance")
            return False
            
    except Exception as e:
        print(f"✗ yfinance connection error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("BIST TRADING SYSTEM - QUICK TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Directory Test", test_directories),
        ("YFinance Connection Test", test_yfinance_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run: python test_download.py")
        print("2. Or run: python test_download_with_viz.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check internet connection for yfinance test")
        print("3. Ensure all files are in the correct locations")
    
    print("=" * 50)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
