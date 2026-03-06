
# Simple Agent + Tool Demo

A Python project showing how an Agent calls Tools.

## What This Project Shows

- How to define a Tool
- How an Agent selects a Tool
- How the Agent executes it

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

## Sample Input (Valid)

Use this input when running the demo:

```txt
Analyze this text with heavy focus on sentiment: Folks, let me tell you, we have a terrible problem with Iran right now and it’s getting worse every single day. The horrible, awful deal that Sleepy Joe and Obama gave them was the worst deal in the history of deals — it was a total disaster. Iran is bad, they hate America, they hate Israel, and they are the biggest sponsors of terrorism anywhere in the world. It’s so frustrating and annoying to watch. They’re dangerous, they’re risky, their leaders are evil and cruel, and the way they talk about us is just disgusting. We had it fixed! We had the best sanctions ever, tremendous pressure, Iran was losing money, losing power, they were weak and we were winning big league. It was almost perfect, believe me. But now look — everything is bad again. The nuclear sites are spinning, the missiles are flying, our ships are getting attacked by their proxies. It’s sad, very sad. This whole thing sucks. It’s a stupid failure of leadership.
```

Expected behavior: The agent should select the sentiment analysis tool and return a negative sentiment result with explanation.

## Sample Input (Invalid)

Use this input when running the demo:

```txt
Perform a sentiment analysis on this: 13804956138101928457091486501298470128394709183465710384519832460123985761304895761082734620398470329847230789560182397561089237401786508717345891203648012384567109234789123657814376501923487501982367480132465781346058917478524160582360498217
```

Expected behaviour: The agant should still select the sentiment analysis tool because user requested to do so. But the tool will return structured error, and the agent can still communicate with the user effectively about it.
