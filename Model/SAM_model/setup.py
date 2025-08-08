"""
Setup script for Legal Query RAG system.
Helps with installation and initial configuration.
"""
import os
import subprocess
import sys
from pathlib import Path

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Setup environment configuration."""
    print("⚙️ Setting up environment...")
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("🔑 OpenAI API key not found in environment variables.")
        print("\nPlease set your OpenAI API key:")
        print("For Windows PowerShell:")
        print('$env:OPENAI_API_KEY="your-api-key-here"')
        print("\nFor Windows Command Prompt:")
        print('set OPENAI_API_KEY=your-api-key-here')
        print("\nFor Linux/Mac:")
        print('export OPENAI_API_KEY="your-api-key-here"')
        
        return False
    else:
        print("✅ OpenAI API key found")
        return True

def create_sample_documents():
    """Create sample legal documents for testing."""
    print("📄 Creating sample documents...")
    
    sample_docs_dir = Path("sample_documents")
    sample_docs_dir.mkdir(exist_ok=True)
    
    # Sample legal document content
    contract_sample = """
    SAMPLE CONTRACT LAW DOCUMENT
    
    Elements of a Valid Contract:
    1. Offer: A clear proposal made by one party to another
    2. Acceptance: Unconditional agreement to the terms of the offer
    3. Consideration: Something of value exchanged between parties
    4. Capacity: Legal ability of parties to enter into contract
    5. Legality: The contract purpose must be legal
    
    Breach of Contract:
    A breach occurs when one party fails to perform any duty specified in the contract.
    Types of breach include:
    - Material breach: Substantial failure that defeats the contract's purpose
    - Minor breach: Partial failure that doesn't defeat the contract's purpose
    
    Remedies for Breach:
    - Damages: Monetary compensation
    - Specific performance: Court order to fulfill contract terms
    - Rescission: Cancellation of the contract
    """
    
    tort_sample = """
    SAMPLE TORT LAW DOCUMENT
    
    Negligence Elements:
    1. Duty: Legal obligation to conform to a standard of conduct
    2. Breach: Failure to meet the required standard of care
    3. Causation: Connection between breach and harm (factual and legal)
    4. Damages: Actual harm or injury suffered
    
    Types of Negligence:
    - Ordinary negligence: Failure to exercise reasonable care
    - Gross negligence: Extreme departure from ordinary care
    - Professional negligence: Failure to meet professional standards
    
    Defenses to Negligence:
    - Comparative negligence: Plaintiff's own negligence reduces recovery
    - Assumption of risk: Plaintiff voluntarily assumed known risk
    - Statute of limitations: Time limit for filing claims
    """
    
    property_sample = """
    SAMPLE PROPERTY LAW DOCUMENT
    
    Adverse Possession Requirements:
    1. Actual possession: Physical occupation of the property
    2. Open and notorious: Possession must be visible and obvious
    3. Exclusive: Possessor excludes others, including true owner
    4. Hostile: Possession without permission of true owner
    5. Continuous: Uninterrupted for statutory period (varies by state)
    
    Real Property Interests:
    - Fee simple absolute: Complete ownership with full rights
    - Life estate: Ownership for duration of person's life
    - Leasehold: Right to possess for specified time period
    
    Easements:
    - Easement appurtenant: Benefits adjacent property
    - Easement in gross: Benefits individual rather than property
    - Express easement: Created by written agreement
    - Implied easement: Arising from circumstances
    """
    
    # Write sample documents
    samples = [
        ("contract_law.txt", contract_sample),
        ("tort_law.txt", tort_sample),
        ("property_law.txt", property_sample)
    ]
    
    for filename, content in samples:
        file_path = sample_docs_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created {file_path}")
    
    print(f"📁 Sample documents created in: {sample_docs_dir.absolute()}")
    return sample_docs_dir

def main():
    """Main setup function."""
    print("🏛️ Legal Query RAG System Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Setup environment
    env_ok = setup_environment()
    
    # Create sample documents
    sample_docs_dir = create_sample_documents()
    
    # Run basic tests
    print("\n🧪 Running basic tests...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_installation.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Basic tests passed")
        else:
            print("⚠️ Some tests failed, but setup continues")
            print(result.stdout)
    
    except Exception as e:
        print(f"⚠️ Could not run tests: {e}")
    
    # Final instructions
    print("\n" + "=" * 40)
    print("🎉 Setup Complete!")
    print("\nNext steps:")
    
    if not env_ok:
        print("1. ❗ Set your OpenAI API key (see instructions above)")
    else:
        print("1. ✅ OpenAI API key is configured")
    
    print("2. 📖 Read the README.md for detailed usage instructions")
    print("3. 🚀 Run the example: python example_usage.py")
    print(f"4. 📄 Sample documents are available in: {sample_docs_dir}")
    
    print("\nQuick test:")
    print("python test_installation.py")
    
    print("\nFor help and documentation:")
    print("python -c \"from infrance import LegalRAGInference; help(LegalRAGInference)\"")

if __name__ == "__main__":
    main()
