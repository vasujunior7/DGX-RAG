"""
Fix installation script for RAG System
Handles common dependency issues
"""
import subprocess
import sys
import os


def run_command(command):
    """Run a command and return success status"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main fix function"""
    print("🔧 RAG System Installation Fix")
    print("=" * 50)
    
    # Uninstall problematic packages first
    print("\n1. Uninstalling potentially problematic packages...")
    packages_to_uninstall = [
        "langchain",
        "langchain-openai", 
        "langchain-community",
        "openai"
    ]
    
    for package in packages_to_uninstall:
        run_command(f"pip uninstall {package} -y")
    
    # Install packages in correct order
    print("\n2. Installing packages in correct order...")
    
    # Install core packages first
    core_packages = [
        "openai==1.23.6",
        "pydantic==2.7.1",
        "numpy==1.24.3",
        "requests==2.31.0"
    ]
    
    for package in core_packages:
        if not run_command(f"pip install {package}"):
            print(f"Failed to install {package}")
            return False
    
    # Install LangChain packages
    langchain_packages = [
        "langchain-core==0.1.52",
        "langchain-openai==0.1.7", 
        "langchain-community==0.0.38",
        "langchain==0.1.20"
    ]
    
    for package in langchain_packages:
        if not run_command(f"pip install {package}"):
            print(f"Failed to install {package}")
            return False
    
    # Install remaining packages
    other_packages = [
        "pymupdf==1.23.8",
        "faiss-cpu==1.8.0",
        "python-dotenv==1.0.0"
    ]
    
    for package in other_packages:
        if not run_command(f"pip install {package}"):
            print(f"Failed to install {package}")
            return False
    
    print("\n✅ Installation completed!")
    print("\n3. Testing imports...")
    
    # Test imports
    test_imports = [
        "import openai",
        "from langchain_openai import OpenAIEmbeddings, ChatOpenAI",
        "from langchain_community.vectorstores import FAISS",
        "import fitz",
        "import faiss"
    ]
    
    for import_test in test_imports:
        try:
            exec(import_test)
            print(f"✅ {import_test}")
        except Exception as e:
            print(f"❌ {import_test} - Error: {e}")
            return False
    
    print("\n🎉 All installations and imports successful!")
    print("You can now run: python main.py")
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Installation failed. Please check the errors above.")
        sys.exit(1)