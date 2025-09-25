from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

open_ai_key = os.getenv("OPENAI_API_KEY", None)
if not open_ai_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

def prepare_podcast_outline(raw_input: str, name: str) -> str:
    with open(Path(__file__).parent.parent / "prompts" / "sys_prompt.txt", "r", encoding="UTF-8") as f:
        raw_prompt = f.read()
    raw_prompt = raw_prompt.replace("{{SALES_DOCUMENT_NAME}}", name)
    raw_prompt = raw_prompt.replace("{{CONTENT}}", raw_input)

    client = OpenAI(
        api_key=os.getenv("API_KEY")
    )
    response = client.responses.create(
        model="gpt-5",
        input=raw_prompt,
        reasoning={ "effort": "high" },
        text={ "verbosity": "medium" },
    )
    return response.output_text