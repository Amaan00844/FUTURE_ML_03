"""
Quick Start Configuration

Setup instructions and initialization script.
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is 3.7+."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")


def install_dependencies():
    """Install required packages."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'
        ])
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def download_spacy_model():
    """Download spaCy English model."""
    print("\n📥 Downloading spaCy model...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'
        ])
        print("✅ spaCy model downloaded")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to download spaCy model: {e}")
        print("   Try: python -m spacy download en_core_web_sm")


def setup():
    """Run complete setup."""
    print("=" * 80)
    print("RESUME SCREENING SYSTEM - SETUP")
    print("=" * 80)
    
    check_python_version()
    install_dependencies()
    download_spacy_model()
    
    print("\n" + "=" * 80)
    print("✅ SETUP COMPLETE!")
    print("=" * 80)
    print("\n🚀 Next Steps:")
    print("   1. Prepare your resume CSV file with columns: ID, Resume_str, Category")
    print("   2. Run: python main.py --csv your_file.csv --role 'Data Scientist'")
    print("   3. Or: python main.py --list  (to see all available roles)")
    print("\n📚 Examples:")
    print("   python examples/basic_usage.py")
    print("   python examples/full_pipeline.py")


if __name__ == '__main__':
    setup()
