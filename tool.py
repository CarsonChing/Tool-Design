class Tool:
    """
    Base tool definition.

    This class can be extended by concrete tools that implement
    a `run` method (or other custom interface) to perform work.
    """

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description

    def run(self, *args, **kwargs):
        """
        Execute the tool.

        Subclasses should override this method.
        """
        raise NotImplementedError("Subclasses must implement `run`.")


def sentiment_analyzer(text: str) -> dict:
    """
    Analyze the sentiment of the given text.

    This is a simple, fully local rule-based analyzer that counts
    occurrences of positive and negative words and derives a sentiment
    score from their difference.

    Args:
        text (str): Arbitrary input text to analyze. Must be a non-empty
            string; otherwise a structured error is returned.

    Returns:
        dict: JSON-serializable object. On success:
            {
                "label": str,   # one of "positive", "negative", "neutral"
                "score": float, # normalized score in the range [-1.0, 1.0]
            }
        On validation error (e.g., too few recognized tokens or wrong type):
            {
                "error": {
                    "code": str,    # short machine-readable error code
                    "message": str, # human-readable description
                }
            }
    """
    import re

    if not isinstance(text, str):
        return {
            "error": {
                "code": "invalid_type",
                "message": "Input `text` must be a string.",
            }
        }

    positive_words = {
        "good", "great", "excellent", "awesome", "amazing", "fantastic", "nice",
        "love", "like", "wonderful", "happy", "pleased", "positive", "enjoy",
        "best", "perfect", "super", "brilliant", "outstanding", "terrific",
        "fabulous", "incredible", "stellar", "impressive", "delightful",
        "lovely", "beautiful", "adorable", "cute", "fun", "funny", "cool",
        "rad", "epic", "legendary", "satisfying", "thrilled", "excited",
        "cheerful", "joyful", "blessed", "grateful", "appreciate", "thankful",
        "inspiring", "motivating", "refreshing", "relaxing", "comfortable",
        "smooth", "easy", "helpful", "supportive", "kind", "friendly",
        "generous", "talented", "smart", "clever", "brave", "strong",
        "healthy", "energetic", "vibrant", "beautiful", "stunning", "gorgeous",
        "magnificent", "spectacular", "breathtaking", "top", "elite", "premium",
        "flawless", "ideal", "dream", "heavenly", "paradise", "win", "victory",
        "success", "win-win", "yes", "yay", "woohoo", "haha"  # common positive laughter
    }

    negative_words = {
        "bad", "terrible", "awful", "horrible", "hate", "dislike", "worst",
        "sad", "angry", "upset", "disappointed", "poor", "negative", "terrifying",
        "annoying", "frustrating", "shitty", "crap", "sucks", "stupid", "dumb",
        "idiotic", "pathetic", "useless", "trash", "garbage", "junk", "broken",
        "disgusting", "gross", "nasty", "filthy", "dirty", "painful", "hurt",
        "pain", "suffering", "miserable", "depressed", "lonely", "boring",
        "dull", "tedious", "tiring", "exhausting", "stressful", "anxious",
        "nervous", "scary", "frightening", "dangerous", "risky", "deadly",
        "toxic", "evil", "cruel", "mean", "rude", "arrogant", "selfish",
        "greedy", "lazy", "weak", "slow", "expensive", "overpriced", "cheap",
        "fake", "scam", "fraud", "lie", "lying", "wrong", "fail", "failure",
        "lost", "defeat", "no", "nah", "ugh", "ew", "yuck", "damn", "hell",
        "shit", "fuck", "wtf", "boo"
    }

    tokens = re.split(r"[^a-zA-Z]+", text.lower())
    tokens = [t for t in tokens if t]

    if len(tokens) < 50:
        return {
            "error": {
                "code": "insufficient_tokens",
                "message": "Not enough recognizable tokens (minimum 50 required) "
                "to perform a reliable sentiment analysis.",
            }
        }

    raw_score = 0
    for token in tokens:
        if token in positive_words:
            raw_score += 1
        elif token in negative_words:
            raw_score -= 1

    total = len(tokens) if tokens else 1
    normalized_score = max(-1.0, min(1.0, raw_score / total))

    # Use a wider neutral band around zero, so small fluctuations
    # in sentiment are treated as neutral.
    if normalized_score > 0.1:
        label = "positive"
    elif normalized_score < -0.1:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "score": normalized_score,
    }


sentiment_analyzer_tool = Tool(
    name="sentiment_analyzer",
    description="Analyze sentiment of a text string locally and return a JSON object.",
)

