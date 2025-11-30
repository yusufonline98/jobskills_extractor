import os
import json
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI  # Swap with Gemini if needed

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

TEMPLATE = """
You are an expert recruiter and resume writer.

Input: A job description.

Tasks:
1. Extract required skills into categories: Technical, Tools, Soft, Certifications
2. Generate 6 achievement-focused resume bullets
3. Return JSON with keys: technical, tools, soft, certifications, bullets

Job Description:
{job_description}
"""

prompt = PromptTemplate(input_variables=["job_description"], template=TEMPLATE)

def run_extraction(job_description: str):
    llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0)
    chain = LLMChain(llm=llm, prompt=prompt)
    raw = chain.run(job_description)
    try:
        parsed = json.loads(raw.strip())
    except Exception:
        import re
        m = re.search(r"(\{.*\})", raw, re.S)
        if m:
            parsed = json.loads(m.group(1))
        else:
            parsed = {"error": "Could not parse JSON", "raw": raw}
    for key in ["technical", "tools", "soft", "certifications", "bullets"]:
        parsed.setdefault(key, [] if key=="bullets" else "")
    if isinstance(parsed.get("bullets"), str):
        lines = [b.strip("-•0123456789. ") for b in parsed["bullets"].splitlines() if b.strip()]
        parsed["bullets"] = lines if lines else [parsed["bullets"]]
    return parsed

