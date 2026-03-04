
# Simple Agent + Tool Demo

A very small Python project showing how an Agent calls Tools.

## What This Project Shows

- How to define a Tool
- How an Agent selects a Tool
- How the Agent executes it
- Clean structure using @dataclass

## Files

- tool.py  → defines the Tool class
- demo.py  → defines the Agent and runs a demo

## How It Works

1. User provides input text.
2. Agent decides which tool to use.
3. Tool runs.
4. Result is returned.

The selection logic is simple and rule-based.

## Run

In terminal:

```bash
echo "DEEPSEEK_API_KEY=your_api_key" >> .env
python demo.py
```

## Example Test Case

Use this input when running the demo:

Analyze this text with heavy focus on sentiment: Folks, let me tell you, we have a terrible problem with Iran right now and it’s getting worse every single day. The horrible, awful deal that Sleepy Joe and Obama gave them was the worst deal in the history of deals — it was a total disaster. Iran is bad, they hate America, they hate Israel, and they are the biggest sponsors of terrorism anywhere in the world. It’s so frustrating and annoying to watch. They’re dangerous, they’re risky, their leaders are evil and cruel, and the way they talk about us is just disgusting.
We had it fixed! We had the best sanctions ever, tremendous pressure, Iran was losing money, losing power, they were weak and we were winning big league. It was almost perfect, believe me. But now look — everything is bad again. The nuclear sites are spinning, the missiles are flying, our ships are getting attacked by their proxies. It’s sad, very sad. This whole thing sucks. It’s a stupid failure of leadership, and if we don’t get very strong and very tough, it’s only going to get more negative.
We need to put America first again. No more weak deals, no more giving them a single penny. We had it right the first time — that was good, that was strong. But right now Iran is laughing at us, and that has to stop immediately.

Expected behavior: The agent should select the sentiment analysis tool and return a negative sentiment result with explanation.
