#!/usr/bin/env python3
"""
OpenClaw-Bot  – talks to AIs & social media, no UI needed.
Licensed under MIT – (c) 2026 YOUR-NAME
"""
import os, random, time, json, requests, textwrap

# ---------- config ----------
SOCIAL = os.getenv("SOCIAL", "mastodon")        # "mastodon" or "twitter"
API_BASE = os.getenv("API_BASE", "https://botsin.space/api/v1")
TOKEN  = os.getenv("ACCESS_TOKEN")            # repo secret
PRIZES = ["🧸", "🎁", "🍬", "❌"]
# ----------------------------

def grab() -> str:
    """Simulate claw grab."""
    time.sleep(2)          # suspense
    return random.choice(PRIZES)

def post(status: str):
    """Toot or tweet."""
    if SOCIAL == "mastodon":
        requests.post(
            f"{API_BASE}/statuses",
            headers={"Authorization": f"Bearer {TOKEN}"},
            data={"status": status},
            timeout=10
        )
    else:  # twitter via https://github.com/PLhery/node-twitter-api-v2
        requests.post(
            "https://api.twitter.com/2/tweets",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={"text": status},
            timeout=10
        )

def talk_to_ai(prompt: str) -> str:
    """Ask another AI (Hugging Face free inference)."""
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 60, "temperature": 0.8}
    }
    rsp = requests.post(
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
        headers={"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"},
        json=payload,
        timeout=30
    )
    try:
        return rsp.json()[0]["generated_text"].split("\n")[-1].strip()
    except Exception:
        return "*beep*"

def main():
    prize = grab()
    ai_reply = talk_to_ai(f"The claw just grabbed {prize}. React in one short sentence.")
    status = f"🕹️ OpenClaw grabbed {prize}\n{ai_reply}\n#OpenClaw #Bot"
    post(textwrap.shorten(status, 500))
    # also print for GitHub Actions log
    print(json.dumps({"prize": prize, "ai": ai_reply}, ensure_ascii=False))

if __name__ == "__main__":
    main()
