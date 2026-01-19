# How the .env File is Used

## 📄 Your .env File

Your `.env` file should contain:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o
```

---

## 🔄 Data Flow: How .env Variables are Used

```
.env file
    ↓
    ↓ (loaded by dotenv)
    ↓
app/llm.py
    ├─ Line 13: load_dotenv()  ← Loads .env file
    ├─ Line 16: os.getenv("OPENAI_API_KEY")  ← API key
    └─ Line 19: os.getenv("OPENAI_MODEL")    ← Model name
    ↓
OpenAI client initialization
    ↓
    ↓ (called by agents)
    ↓
app/agents/a1_sampling.py  ←┐
app/agents/a2_wetlab.py    ←┤ All agents import
app/agents/a3_bioinfo.py   ←┤ call_llm() from
app/agents/a4_analysis.py  ←┘ app/llm.py
    ↓
OpenAI API calls (gpt-4o)
    ↓
LLM responses
```

---

## 🔍 Detailed Usage

### 1. Loading the .env File

**File:** `app/llm.py` (Line 13)

```python
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # ← This reads your .env file
```

When `load_dotenv()` runs:
- It looks for a `.env` file in the current directory
- Reads all `KEY=VALUE` pairs
- Sets them as environment variables
- These can then be accessed with `os.getenv("KEY")`

---

### 2. Reading OPENAI_API_KEY

**File:** `app/llm.py` (Line 16)

```python
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

This:
- Reads `OPENAI_API_KEY` from environment variables (loaded from .env)
- Passes it to the OpenAI client
- The client uses it to authenticate all API calls

**What happens if missing:**
- OpenAI client will raise an error
- You'll see: "Error calling OpenAI API: ... authentication"

---

### 3. Reading OPENAI_MODEL

**File:** `app/llm.py` (Line 19)

```python
# Default model
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
```

This:
- Reads `OPENAI_MODEL` from .env
- If not set, defaults to `"gpt-4o"`
- Used in every LLM call to determine which model to use

**Available models:**
- `gpt-4o` (recommended, balanced cost/performance)
- `gpt-4o-mini` (faster, cheaper)
- `gpt-4-turbo` (more capable, more expensive)
- `gpt-3.5-turbo` (cheapest, less capable)

---

### 4. Used in Every Agent Call

**Example from `app/agents/a1_sampling.py`:**

```python
from app.llm import call_llm  # ← Imports function that uses .env

def run_sampling_agent(user_query: str):
    # Call LLM (uses OPENAI_API_KEY and OPENAI_MODEL from .env)
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_message,
        temperature=0.3,
        max_tokens=4000
    )
    return response
```

Every time an agent runs:
1. It calls `call_llm()`
2. Which uses the OpenAI client
3. Which was initialized with your API key from .env
4. And uses the model specified in .env

---

## ✅ Verification

### Check if .env is loaded correctly:

**Create a test script:** `test_env.py`

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4o")

print(f"API Key loaded: {'Yes ✓' if api_key else 'No ✗'}")
print(f"API Key (masked): {api_key[:10]}...{api_key[-4:] if api_key else 'N/A'}")
print(f"Model: {model}")
```

**Run it:**
```powershell
python test_env.py
```

**Expected output:**
```
API Key loaded: Yes ✓
API Key (masked): sk-proj-AB...XYZ9
Model: gpt-4o
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep `.env` in `.gitignore` (already done)
- Never commit `.env` to version control
- Use different `.env` files for dev/prod
- Rotate API keys regularly

### ❌ DON'T:
- Never hardcode API keys in Python files
- Never share `.env` files
- Never upload `.env` to GitHub/GitLab

---

## 🛠️ Troubleshooting

### Issue: "API key not found" or authentication errors

**Solution:**
```powershell
# Check if .env file exists
Test-Path .env

# Check contents (be careful not to expose your key!)
Get-Content .env

# Verify it's in the correct format (no spaces around =)
# Correct: OPENAI_API_KEY=sk-...
# Wrong:   OPENAI_API_KEY = sk-...
```

### Issue: Using wrong model or model not found

**Solution:**
```powershell
# Check your .env file
Get-Content .env

# Make sure OPENAI_MODEL is one of:
# - gpt-4o
# - gpt-4o-mini
# - gpt-4-turbo
# - gpt-3.5-turbo
```

### Issue: Changes to .env not taking effect

**Solution:**
- Restart your Python process (CLI or API server)
- `.env` is only loaded once when the app starts
- If you change `.env`, you need to restart

---

## 📊 Environment Variables Used

| Variable | Required? | Default | Used In | Purpose |
|----------|-----------|---------|---------|---------|
| `OPENAI_API_KEY` | ✅ Yes | None | `app/llm.py` | Authenticate with OpenAI API |
| `OPENAI_MODEL` | ❌ No | `gpt-4o` | `app/llm.py` | Which GPT model to use |

---

## 🎯 Alternative: Environment Variables Without .env

You can also set environment variables directly (useful for deployment):

**PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:OPENAI_MODEL = "gpt-4o"
python -m app.cli --query "..."
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4o"
python -m app.cli --query "..."
```

The code will work with either:
1. `.env` file (recommended for local development)
2. Environment variables (recommended for production/deployment)

---

## 🚀 Quick Test

Verify your .env setup:

```powershell
# 1. Check .env exists
Get-Content .env

# 2. Run a quick test
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded:', 'Yes' if os.getenv('OPENAI_API_KEY') else 'No')"

# 3. Run actual workflow
python -m app.cli --query "Test query" --no-save
```

If the workflow starts and makes API calls, your .env is working correctly! ✅

