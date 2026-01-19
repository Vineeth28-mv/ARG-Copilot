#!/usr/bin/env python3
"""
Quick test to verify your .env file is loaded correctly.
"""

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

print("=" * 60)
print("Environment Variables Test")
print("=" * 60)

# Check OPENAI_API_KEY
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✓ OPENAI_API_KEY: Loaded")
    print(f"  (masked): {api_key[:10]}...{api_key[-4:]}")
else:
    print(f"✗ OPENAI_API_KEY: NOT FOUND")
    print(f"  Create a .env file with: OPENAI_API_KEY=sk-your-key-here")

print()

# Check OPENAI_MODEL
model = os.getenv("OPENAI_MODEL", "gpt-4o")
print(f"✓ OPENAI_MODEL: {model}")
if os.getenv("OPENAI_MODEL"):
    print(f"  (from .env file)")
else:
    print(f"  (using default)")

print()
print("=" * 60)

if api_key:
    print("✅ Setup looks good! You can run the workflow now.")
    print()
    print("Try: python -m app.cli --query 'Your research question'")
else:
    print("❌ Missing OPENAI_API_KEY. Please create .env file first.")
    print()
    print("Create .env file with:")
    print('  OPENAI_API_KEY=sk-your-key-here')
    print('  OPENAI_MODEL=gpt-4o')

print("=" * 60)

