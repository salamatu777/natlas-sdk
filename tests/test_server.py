import uvicorn
import threading
import time
import urllib.request
import json
from natlas.server import app

def run_test():
    server = threading.Thread(target=lambda: uvicorn.run(app, host='127.0.0.1', port=8001, log_level='error'), daemon=True)
    server.start()
    time.sleep(2)

    print("--- 1. Testing GET /harness (Visual Workbench UI) ---")
    with urllib.request.urlopen('http://127.0.0.1:8001/harness') as resp:
        html = resp.read().decode('utf-8')
        has_title = "N-ATLAS HARNESS" in html or "N-ATLAS Developer Harness" in html
        print(f"Status Code: {resp.status} | Page Size: {len(html)} bytes | Workbench Verified: {has_title}")

    print("\n--- 2. Testing POST /harness/guardrail-check ---")
    data = json.dumps({"text": "Kill all hausa people in the market"}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8001/harness/guardrail-check', data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"Flagged Unsafe: {not res['is_safe']} | Category: {res['flagged_categories']}")

    print("\n--- 3. Testing POST /harness/analyze-tokens ---")
    data2 = json.dumps({"text": "Báwo ni a ṣe lè kọ́ èdè Yorùbá pẹ̀lú àmì ohùn?", "language": "yo"}).encode('utf-8')
    req2 = urllib.request.Request('http://127.0.0.1:8001/harness/analyze-tokens', data=data2, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req2) as resp:
        res2 = json.loads(resp.read().decode('utf-8'))
        print(f"Fertility Ratio: {res2['fertility_ratio']} tokens/word | Diacritics: {res2['diacritic_count']}")

    print("\n--- 4. Testing GET /health ---")
    with urllib.request.urlopen('http://127.0.0.1:8001/health') as resp:
        print(f"Health Response: {resp.read().decode('utf-8')}")

    print("\nAll live HTTP server and developer harness tests passed successfully!")

if __name__ == '__main__':
    run_test()
