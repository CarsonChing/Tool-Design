import json
import os
import re
from typing import Any, Dict, List

from openai import OpenAI
import tool
from dotenv import load_dotenv


# JSON schema we ask the LLM to return so we can decide whether to call a tool.
LLM_RESPONSE_SCHEMA = """
You must reply with exactly one JSON object, no other text. Use one of these shapes:

1) When you do NOT need to call a tool (answer directly):
   {"use_tool": false, "response": "your answer to the user"}

2) When you DO need to call the sentiment_analyzer tool (user asks for sentiment/emotion of text):
   {"use_tool": true, "tool_name": "sentiment_analyzer", "arguments": {"text": "the exact text to analyze"}}

Available tool:
- sentiment_analyzer: analyzes sentiment of a string; arguments must be {"text": "<string>"}.
"""


def get_client() -> OpenAI:
    """
    Create a DeepSeek client using the OpenAI-compatible SDK.

    The API key is read from the DEEPSEEK_API_KEY environment variable,
    which is loaded from a local .env file if present.
    """
    # Load variables from .env into the environment (no-op if already loaded).
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError(
            "DEEPSEEK_API_KEY is not set. "
            "Set it in your environment or in a local .env file."
        )

    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def parse_llm_json(content: str) -> Dict[str, Any] | None:
    """
    Extract a JSON object from the LLM response (handles markdown code blocks).
    """
    content = content.strip()
    # Strip optional markdown code block
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
    if match:
        content = match.group(1)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def run_agent(user_input: str) -> str:
    """
    Run a simple single-turn agent. The LLM returns JSON to indicate whether
    to call a tool; we parse that JSON and call the tool locally if needed.
    """
    client = get_client()

    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that analyzes speech. "
                + LLM_RESPONSE_SCHEMA
            ),
        },
        {"role": "user", "content": user_input},
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )
    raw = (response.choices[0].message.content or "").strip()
    parsed = parse_llm_json(raw)

    if parsed is None:
        return f"Could not parse model response as JSON. Raw reply:\n{raw}"

    use_tool = parsed.get("use_tool") is True
    if not use_tool:
        print(f"\n[demo] No tool requested by model. Return direct response.")
        return parsed.get("response", raw)

    tool_name = parsed.get("tool_name")
    arguments = parsed.get("arguments") or {}

    print(f"\n[demo] Tool requested by model: {tool_name}")
    print(f"[demo] Tool arguments from model: {json.dumps(arguments, ensure_ascii=False)}")

    if tool_name == "sentiment_analyzer":
        text_arg = arguments.get("text", "")
        tool_result = tool.sentiment_analyzer(text_arg)
    else:
        tool_result = {
            "error": {
                "code": "unknown_tool",
                "message": f"Unknown tool: {tool_name}",
            }
        }

    print(f"[demo] Tool result: {json.dumps(tool_result, ensure_ascii=False)}")

    # Optional: ask the model to turn the tool result into a natural reply.
    messages.append({"role": "assistant", "content": raw})
    messages.append(
        {
            "role": "user",
            "content": (
                "Tool result (use this to answer the user in a short, natural way):\n"
                + json.dumps(tool_result)
            ),
        }
    )
    followup = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )
    raw = (followup.choices[0].message.content or "").strip()
    parsed = parse_llm_json(raw)

    if parsed is None:
        return f"Could not parse model response as JSON. Raw reply:\n{raw}"

    return parsed.get("response", raw)


if __name__ == "__main__":
    user_text = input("Enter a message for the agent: ")
    try:
        reply = run_agent(user_text)
    except Exception as exc:  # noqa: BLE001 - simple demo script
        print(f"Error running agent: {exc}")
    else:
        print("\nAgent reply:")
        print(reply)

