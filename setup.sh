#!/bin/bash
# Setup script for ARG Surveillance Multi-Agent Framework

echo "🚀 Setting up ARG Surveillance Framework..."

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
fi

# Create runs directory
if [ ! -d "runs" ]; then
    echo "Creating runs directory..."
    mkdir runs
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Replace placeholder prompts in app/prompts/*_prompt.py with your actual prompts"
echo "3. Run the CLI: python -m app.cli --query 'Your research question'"
echo "4. Or start the API: python -m app.api"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate   (Linux/Mac)"
echo "  venv\\Scripts\\activate      (Windows)"



