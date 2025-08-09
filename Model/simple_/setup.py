"""
Setup script for RAG System
"""
import os
import subprocess
import sys


def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = ["documents", "logs"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")


def create_env_file():
    """Create .env file template"""
    env_content = """# RAG System Environment Variables
# Copy this file to .env and fill in your actual values

OPENAI_API_KEY=your-openai-api-key-here
PDF_SAVE_DIR=./documents
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
BATCH_SIZE=8
MAX_THREADS=4
SIMILARITY_THRESHOLD=0.7
"""
    
    if not os.path.exists(".env.template"):
        with open(".env.template", "w") as f:
            f.write(env_content)
        print("✅ Created .env.template file")
        print("📝 Please copy .env.template to .env and update with your API keys")
    else:
        print("📄 .env.template already exists")


def main():
    """Main setup function"""
    print("🚀 RAG System Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed - could not install requirements")
        return
    
    # Create directories
    create_directories()
    
    # Create environment file template
    create_env_file()
    
    print("\n" + "=" * 40)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy .env.template to .env")
    print("2. Update .env with your OpenAI API key")
    print("3. Run: python main.py")
    print("=" * 40)


if __name__ == "__main__":
    main()