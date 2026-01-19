# Setup Checklist

Use this checklist to ensure everything is configured correctly.

## ✅ Phase 1: Environment Setup

- [ ] Python 3.8+ installed
  ```bash
  python --version
  ```

- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

- [ ] OpenAI API key set
  ```bash
  export OPENAI_API_KEY='sk-...'
  # OR create .env file with OPENAI_API_KEY=...
  ```

- [ ] Test OpenAI connection
  ```bash
  python -c "import openai; print('OK')"
  ```

## ✅ Phase 2: Prompts (CRITICAL)

**You MUST replace all 8 placeholder prompts before the system will work properly.**

### A1: Sampling Design Agent
- [ ] `app/prompts/a1_sampling_system_prompt.py`
  - Source: `Sampling Design Agent_System Prompt.md`
  - Paste entire Markdown content into `TEXT = """..."""`

- [ ] `app/prompts/a1_sampling_user_prompt.py`
  - Source: `Sampling Design Agent_User_Prompt.md`
  - Paste entire Markdown content into `TEXT = """..."""`

### A2: Wet-Lab Protocol Agent
- [ ] `app/prompts/a2_wetlab_system_prompt.py`
  - Source: `Wet-Lab Protocol Agent_System_Prompt.md`

- [ ] `app/prompts/a2_wetlab_user_prompt.py`
  - Source: `Wet-Lab Protocol Agent_User_Prompt.md`

### A3: Bioinformatics Pipeline Agent
- [ ] `app/prompts/a3_bioinfo_system_prompt.py`
  - Source: `bioinformatics_Agent_System_Prompt.md`

- [ ] `app/prompts/a3_bioinfo_user_prompt.py`
  - Source: `bioinformatics_Agent_User_Prompt.md`

### A4: Statistical Analysis Agent
- [ ] `app/prompts/a4_analysis_system_prompt.py`
  - Source: `Statistical Analysis & Visualization Agent_System_Prompt.md`

- [ ] `app/prompts/a4_analysis_user_prompt.py`
  - Source: `Statistical Analysis & Visualization Agent_User_Prompt.md`

## ✅ Phase 3: Test Run

- [ ] Test CLI (dry run)
  ```bash
  python -m app.cli --query "Test query" --no-save
  ```

- [ ] Test full workflow
  ```bash
  python -m app.cli --query "Design ARG surveillance in wastewater"
  ```

- [ ] Check results directory
  ```bash
  ls -la runs/
  ```

- [ ] Verify outputs exist
  - [ ] `A1.md` and `A1.json`
  - [ ] `A2.md` and `A2.json`
  - [ ] `A3.md` and `A3.json`
  - [ ] `A4.md` and `A4.json`
  - [ ] `SUMMARY.md`

## ✅ Phase 4: API Testing (Optional)

- [ ] Start API server
  ```bash
  python -m app.api
  # Should see: "Application startup complete"
  ```

- [ ] Test health endpoint
  ```bash
  curl http://localhost:8000/health
  # Should return: {"status":"healthy","openai_key_set":true}
  ```

- [ ] Test workflow endpoint
  ```bash
  curl -X POST http://localhost:8000/workflow/run \
    -H "Content-Type: application/json" \
    -d '{"query":"Test query","save_results":false}'
  ```

## ✅ Phase 5: Validation

- [ ] Review A1 output
  - Is the sampling design appropriate?
  - Is the JSON structure correct?

- [ ] Review A2 output
  - Are protocols non-actionable (no specific temps/volumes)?
  - Check `A2_guardrails.json` for violations

- [ ] Review A3 output
  - Is the bash script generated?
  - Is the YAML config present?
  - Check `A3_guardrails.json` for execution commands

- [ ] Review A4 output
  - Is the R Markdown script generated?
  - Are helper functions present?
  - Check `A4_guardrails.json` for system calls

## 🔧 Troubleshooting

### Issue: "OPENAI_API_KEY not set"
```bash
# Check if key is set
echo $OPENAI_API_KEY

# Set it
export OPENAI_API_KEY='sk-...'

# Or create .env file
echo "OPENAI_API_KEY=sk-..." > .env
```

### Issue: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Issue: Workflow hangs
- Check OpenAI API quota/rate limits
- Reduce `max_tokens` in agent files
- Use a faster model (gpt-4o-mini)

### Issue: Outputs are placeholders
- You forgot to replace the prompts!
- Open `app/prompts/*_prompt.py` and paste your actual prompts

### Issue: JSON parsing fails
- Check that your prompts instruct the LLM to output JSON
- Review the raw output in `A*.md` files
- Adjust prompt formatting

### Issue: Guardrail violations
- Review `*_guardrails.json` files
- Adjust prompts to be less specific (A2) or avoid execution commands (A3/A4)
- Modify guardrail patterns in `app/guards.py` if needed

## 📊 Success Criteria

Your setup is complete when:

1. ✅ CLI runs without errors
2. ✅ All 4 agents complete successfully
3. ✅ Outputs are saved to `runs/<timestamp>/`
4. ✅ JSON outputs are valid and structured
5. ✅ Guardrail violations are minimal or zero
6. ✅ API endpoints respond correctly (if using API)

## 🚀 Next Steps

Once setup is complete:

1. **Run real workflows**: Use your actual research questions
2. **Customize agents**: Adjust validation, parsing, temperature
3. **Integrate with tools**: Connect to databases, version control, etc.
4. **Deploy**: Containerize with Docker, deploy to cloud
5. **Monitor**: Add logging, metrics, error tracking

## 📝 Notes

- First run may take 2-5 minutes depending on prompt length
- Costs: ~$0.10-0.50 per full workflow (4 agents with gpt-4o)
- Results are timestamped and never overwritten
- Failed runs still save partial results

## 🆘 Support

If you encounter issues not covered here:

1. Check `README.md` for full documentation
2. Review `STRUCTURE.md` to understand the architecture
3. Read agent code in `app/agents/` to debug specific issues
4. Check OpenAI API status: https://status.openai.com

---

**Last Updated:** 2025-01-09

