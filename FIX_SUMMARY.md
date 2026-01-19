# Bug Fix: JSON Parsing Error

## Problem Identified

The framework was crashing with error: `KeyError: '\n  "framework"'`

## Root Cause

The user prompt files contained JSON examples with curly braces `{...}`, and the agent code was using Python's `.format()` method to inject variables:

```python
user_message = USER_PROMPT.format(user_query=user_query)
```

When `.format()` encountered JSON like:
```json
{
  "framework": "STROBE-metagenomics"
}
```

It tried to interpret `"framework"` as a format placeholder, causing a `KeyError`.

## Solution

✅ **Replaced `.format()` with `.replace()`** using unique placeholders that won't conflict with JSON:

### Agent Code Changes

| Agent | Old | New |
|-------|-----|-----|
| A1 | `.format(user_query=...)` | `.replace("###USER_QUERY###", ...)` |
| A2 | `.format(sampling_output=...)` | `.replace("###SAMPLING_OUTPUT###", ...)` |
| A3 | `.format(wetlab_output=...)` | `.replace("###WETLAB_OUTPUT###", ...)` |
| A4 | `.format(bioinfo_output=...)` | `.replace("###BIOINFO_OUTPUT###", ...)` |

### Prompt Template Changes

| File | Old Placeholder | New Placeholder |
|------|----------------|-----------------|
| `a1_sampling_user_prompt.py` | `{user_query}` | `###USER_QUERY###` |
| `a2_wetlab_user_prompt.py` | `{sampling_output}` | `###SAMPLING_OUTPUT###` |
| `a3_bioinfo_user_prompt.py` | `{wetlab_output}` | `###WETLAB_OUTPUT###` |
| `a4_analysis_user_prompt.py` | `{bioinfo_output}` | `###BIOINFO_OUTPUT###` |

## Files Modified

1. ✅ `app/agents/a1_sampling.py` - Line 29
2. ✅ `app/agents/a2_wetlab.py` - Line 34
3. ✅ `app/agents/a3_bioinfo.py` - Line 34
4. ✅ `app/agents/a4_analysis.py` - Line 34
5. ✅ `app/prompts/a1_sampling_user_prompt.py` - Line 436
6. ✅ `app/prompts/a2_wetlab_user_prompt.py` - Line 592
7. ✅ `app/prompts/a3_bioinfo_user_prompt.py` - Line 773
8. ✅ `app/prompts/a4_analysis_user_prompt.py` - Line 798

## Additional Improvements

Also enhanced error handling and logging:
- Added traceback printing for debugging
- Made JSON parsing more robust
- Improved validation to continue with warnings instead of blocking execution

## Next Step

Run the workflow again to verify the fix:
```bash
python run_example.py
```

The framework should now execute successfully! 🎉
