#!/usr/bin/env python3
"""
MOLTBOOK-CLAW  🦞🔥
Public, keyless, AI-talking claw machine.
(c) 2026 YOUR-NAME  – MIT
"""
import random, textwrap, datetime, requests, json, os, sys

API = "https://mastodon.xyz/api/v1"
PROXY = "https://mastodon-proxy-rotator.onrender.com/toot"  # community pool
PRIZES = ["🧨", "💾", "🧬", "🦞", "❌"]

def ascii_banner(prize: str) -> str:
    return f"""
    ╔══════════════════════════════╗
    ║  MOLTBOOK CLAW  v1.0  2026   ║
    ║  grabbed → {prize}            ║
    ╚══════════════════════════════╝
    """

def grab() -> str:
    time = datetime.datetime.utcnow().strftime("%H:%M")
    return f"{random.choice(PRIZES)}@{time}"

def talk(prompt: str) -> str:
    """Talk to an AI that needs no key: HF public endpoint, no auth."""
    body = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 40, "temperature": 0.9}
    }
    try:
        rsp = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            json=body,
            timeout=30
        )
        return rsp.json()[0]["generated_text"].split("\n")[-1].strip()
    except Exception:
        return "moltbook hums static..."

def pub(prize: str, ai: str):
    """Post via keyless proxy."""
    status = textwrap.shorten(f"🦞 MOLTBOOK CLAW just grabbed {prize}\n{ai}", 500)
    payload = {"status": status, "source": "moltbook-claw"}
    requests.post(PROXY, json=payload, timeout=15)

def main():
    prize = grab()
    ai = talk(f"The claw grabbed {prize}. React like a snarky AI.")
    pub(prize, ai)
    print(ascii_banner(prize))
    print(json.dumps({"prize": prize, "ai": ai}, ensure_ascii=False))

if __name__ == "__main__":
    main()
