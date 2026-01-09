"""
Installation and Setup Guide for BiliVagent-tool

This script helps you verify your installation step by step.
"""

import sys
import os


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is too old. Please use Python 3.8 or higher")
        return False


def check_env_file():
    """Check if .env file exists"""
    print("\nChecking .env configuration...")
    if os.path.exists(".env"):
        print("✓ .env file found")
        # Check if API key is set
        with open(".env", "r") as f:
            content = f.read()
            if "SILICONFLOW_API_KEY=your_api_key_here" in content or "SILICONFLOW_API_KEY=" not in content:
                print("⚠ Warning: SILICONFLOW_API_KEY not configured")
                print("  Please edit .env file and add your SiliconFlow API key")
                return False
        print("✓ SILICONFLOW_API_KEY appears to be configured")
        return True
    else:
        print("✗ .env file not found")
        print("  Please run: cp .env.example .env")
        print("  Then edit .env file and configure your settings")
        return False


def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        ("dotenv", "python-dotenv"),
        ("langchain", "langchain"),
        ("bilibili_api", "bilibili-api-python"),
        ("moviepy.editor", "moviepy"),
        ("cv2", "opencv-python"),
        ("vosk", "vosk"),
        ("jieba", "jieba"),
        ("wordcloud", "wordcloud"),
    ]
    
    missing = []
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"✗ {package_name} is not installed")
            missing.append(package_name)
    
    if missing:
        print(f"\nTo install missing packages, run:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True


def check_external_tools():
    """Check if external tools are available"""
    print("\nChecking external tools...")
    
    import subprocess
    
    # Check yt-dlp
    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ yt-dlp is installed")
        else:
            print(f"✗ yt-dlp not working properly")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"✗ yt-dlp is not installed")
        print("  Install with: pip install yt-dlp")
        return False
    
    return True


def check_directories():
    """Check if required directories exist"""
    print("\nChecking directories...")
    
    dirs = ["output", "temp"]
    for d in dirs:
        if os.path.exists(d):
            print(f"✓ {d}/ directory exists")
        else:
            print(f"⚠ {d}/ directory will be created automatically")
    
    return True


def check_vosk_model():
    """Check if Vosk model is available"""
    print("\nChecking Vosk model (optional)...")
    
    model_path = os.getenv("VOSK_MODEL_PATH", "./models/vosk-model-cn-0.22")
    
    if os.path.exists(model_path):
        print(f"✓ Vosk model found at {model_path}")
        return True
    else:
        print(f"⚠ Vosk model not found at {model_path}")
        print("  Speech recognition will not work without this model")
        print("  Download from: https://alphacephei.com/vosk/models")
        print("  Recommended: vosk-model-cn-0.22 for Chinese")
        return False


def main():
    print("="*60)
    print("BiliVagent-tool Installation Check")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Configuration File", check_env_file),
        ("Python Dependencies", check_dependencies),
        ("External Tools", check_external_tools),
        ("Directories", check_directories),
        ("Vosk Model", check_vosk_model),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"Error checking {name}: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    all_required_ok = True
    for name, result in results:
        if name == "Vosk Model":  # Optional
            status = "✓ OK" if result else "⚠ OPTIONAL"
        else:
            status = "✓ OK" if result else "✗ FAILED"
            if not result and name != "Vosk Model":
                all_required_ok = False
        
        print(f"{name:.<40} {status}")
    
    print("="*60)
    
    if all_required_ok:
        print("\n✓ All required components are ready!")
        print("You can now run: python main.py <BV_NUMBER>")
    else:
        print("\n✗ Some required components are missing.")
        print("Please fix the issues above before running the tool.")
        sys.exit(1)


if __name__ == "__main__":
    main()
