import urllib.request
import ssl
import json
import time
import sys

# Ensure UTF-8 output
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl._create_unverified_context()
LIVE_API_URL = "https://d9fd-34-186-47-214.ngrok-free.app/v1/chat/completions"

def query_natlas(prompt, lang_name):
    payload = {
        "model": "NCAIR1/N-ATLaS",
        "messages": [
            {"role": "system", "content": "you are a large language model trained by Awarri AI technologies. You are a friendly assistant and you are here to help."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 220,
        "temperature": 0.1
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        LIVE_API_URL, 
        data=data, 
        headers={
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "1", 
            "User-Agent": "NAtlasClient/0.2.0"
        }
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            duration = round(time.time() - t0, 2)
            res_json = json.loads(resp.read().decode("utf-8"))
            print(f"\n{'='*70}")
            print(f"[{lang_name}] Query: \"{prompt}\" (Latency: {duration}s)")
            print(f"{'='*70}")
            print(res_json["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"Error querying {lang_name}: {e}")

if __name__ == '__main__':
    print("Connecting to live N-ATLAS GPU server at https://d9fd-34-186-47-214.ngrok-free.app ...")
    
    # Hausa query
    query_natlas("Wane irin taki ne ya fi dacewa da noman masara a Arewacin Najeriya?", "HAUSA")
    
    # English query
    query_natlas("What are the best practices for controlling fall armyworm on maize in Nigeria?", "ENGLISH")
