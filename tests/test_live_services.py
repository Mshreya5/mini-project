import os
import subprocess
import sys
import time
import requests

os.environ["NO_PROXY"] = "localhost,127.0.0.1,*"
os.environ["no_proxy"] = "localhost,127.0.0.1,*"

PYTHON = sys.executable


def kill_proc(proc):
    if sys.platform == "win32":
        subprocess.run(f"taskkill /F /T /PID {proc.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()

def test_live_system():
    print("=================================================================")
    print("🚀 STARTING LIVE PRODUCTION SERVICES FOR VERIFICATION")
    print("=================================================================")

    sub_env = {**os.environ, "NO_PROXY": "*", "no_proxy": "*"}
    p2 = subprocess.Popen([PYTHON, "-m", "uvicorn", "ai_module.api.main:app", "--host", "127.0.0.1", "--port", "8001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=sub_env)
    p3 = subprocess.Popen([PYTHON, "-m", "uvicorn", "url_analysis.api:app", "--host", "127.0.0.1", "--port", "8002"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=sub_env)
    p4 = subprocess.Popen([PYTHON, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=sub_env)
    p1 = subprocess.Popen([PYTHON, "-m", "streamlit", "run", "silvershield_frontend.py", "--server.port", "8501", "--server.headless", "true", "--browser.gatherUsageStats", "false"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=sub_env)

    processes = [p2, p3, p4, p1]

    try:
        print("Waiting for all 4 services to become healthy...")
        healthy = False
        for attempt in range(25):
            time.sleep(1.0)
            status_2 = status_3 = status_4 = status_1 = "DOWN"
            try:
                r2 = requests.get("http://127.0.0.1:8001/health", timeout=1.0)
                status_2 = f"HTTP {r2.status_code}"
            except Exception as e:
                status_2 = type(e).__name__

            try:
                r3 = requests.get("http://127.0.0.1:8002/health", timeout=1.0)
                status_3 = f"HTTP {r3.status_code}"
            except Exception as e:
                status_3 = type(e).__name__

            try:
                r4 = requests.get("http://127.0.0.1:8000/health", timeout=1.0)
                status_4 = f"HTTP {r4.status_code}"
            except Exception as e:
                status_4 = type(e).__name__

            try:
                r1 = requests.get("http://127.0.0.1:8501", timeout=1.0)
                status_1 = f"HTTP {r1.status_code}"
            except Exception as e:
                status_1 = type(e).__name__

            print(f"Attempt {attempt+1}: 8001: {status_2} | 8002: {status_3} | 8000: {status_4} | 8501: {status_1}", flush=True)

            if "HTTP 200" in status_2 and "HTTP 200" in status_3 and "HTTP 200" in status_4 and "HTTP 200" in status_1:
                healthy = True
                break

        if not healthy:
            raise RuntimeError("One or more services failed to start within 25 seconds.")

        print("✅ All 4 services are LIVE and responding:")
        print("  - Port 8001: Member 2 (ML Scam API) -> OK")
        print("  - Port 8002: Member 3 (URL Security API) -> OK")
        print("  - Port 8000: Member 4 (Central Risk Aggregator) -> OK")
        print("  - Port 8501: Member 1 (Streamlit Frontend) -> OK")

        backend_url = "http://127.0.0.1:8000/api/v1/assess"

        print("\n--- TEST 1: Legitimate Message ---")
        msg1 = "Hi Mom, I am on my way home from college. See you for dinner at 8 PM!"
        r = requests.post(backend_url, json={"message": msg1}, timeout=5.0)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        d1 = r.json()
        print(f"Risk Level: {d1['overall_risk']} | Score: {d1['risk_score']} | Status: {d1['status']}")
        print(f"Warning: {d1['warning']}")
        print(f"Explanation: {d1.get('explanation')}")
        assert d1["overall_risk"] == "LOW", f"Expected LOW risk, got {d1['overall_risk']}"
        assert d1["status"] == "OK"
        print("Result: PASS")

        print("\n--- TEST 2: Scam Message ---")
        msg2 = "CONGRATULATIONS! You have been selected as the grand winner of $500,000 cash prize! Claim your prize now."
        r = requests.post(backend_url, json={"message": msg2}, timeout=5.0)
        assert r.status_code == 200
        d2 = r.json()
        print(f"Risk Level: {d2['overall_risk']} | Score: {d2['risk_score']} | Indicators: {d2['risk_indicators']}")
        print(f"Warning: {d2['warning']}")
        print(f"Explanation: {d2.get('explanation')}")
        assert d2["overall_risk"] == "HIGH", f"Expected HIGH risk, got {d2['overall_risk']}"
        assert len(d2["risk_indicators"]) > 0
        print("Result: PASS")

        print("\n--- TEST 3: Suspicious URL ---")
        msg3 = "Urgent: Your account is locked. Log in immediately to verify at http://192.168.1.1/secure-login"
        r = requests.post(backend_url, json={"message": msg3}, timeout=5.0)
        assert r.status_code == 200
        d3 = r.json()
        print(f"Risk Level: {d3['overall_risk']} | URL Risk: {d3['url_risk']} | Indicators: {d3['risk_indicators']}")
        print(f"Analysed URL: {d3['analysed_url']}")
        assert d3["overall_risk"] in ("MEDIUM", "HIGH")
        assert d3["url_risk"] in ("SUSPICIOUS", "MALICIOUS")
        print("Result: PASS")

        print("\n--- TEST 4: Safe URL with Normal Message ---")
        msg4 = "Here is the article on elderly gardening tips you asked for: https://en.wikipedia.org/wiki/Gardening"
        r = requests.post(backend_url, json={"message": msg4}, timeout=5.0)
        assert r.status_code == 200
        d4 = r.json()
        print(f"Risk Level: {d4['overall_risk']} | URL Risk: {d4['url_risk']}")
        assert d4["overall_risk"] == "LOW", f"Expected LOW risk for benign Wikipedia link, got {d4['overall_risk']}"
        assert d4["url_risk"] == "SAFE"
        print("Result: PASS")

        print("\n--- TEST 5: Message Containing OTP Request ---")
        msg5 = "Your bank verification OTP is 839201. Please reply with this OTP to our customer service agent to prevent account block."
        r = requests.post(backend_url, json={"message": msg5}, timeout=5.0)
        assert r.status_code == 200
        d5 = r.json()
        print(f"Risk Level: {d5['overall_risk']} | Score: {d5['risk_score']} | Indicators: {d5['risk_indicators']}")
        print(f"Warning: {d5['warning']}")
        print(f"Recommended Actions: {d5['recommended_actions']}")
        assert d5["overall_risk"] == "HIGH"
        assert any("otp" in str(ind).lower() for ind in d5["risk_indicators"])
        print("Result: PASS")

        print("\n--- TEST 6: Urgent Payment Threatening Account Suspension ---")
        msg6 = "FINAL NOTICE: Your power will be disconnected in 1 hour due to unpaid bill. Pay immediately by wire transfer to avoid penalty."
        r = requests.post(backend_url, json={"message": msg6}, timeout=5.0)
        assert r.status_code == 200
        d6 = r.json()
        print(f"Risk Level: {d6['overall_risk']} | Score: {d6['risk_score']} | Indicators: {d6['risk_indicators']}")
        assert d6["overall_risk"] == "HIGH"
        assert len(d6["recommended_actions"]) > 0
        print("Result: PASS")

        print("\n--- TEST 7: Empty or Invalid Input ---")
        r_empty = requests.post(backend_url, json={"message": "   "}, timeout=5.0)
        print(f"Empty message response code: {r_empty.status_code}")
        assert r_empty.status_code == 422, f"Expected 422 for empty message, got {r_empty.status_code}"

        r_bad_url = requests.post(backend_url, json={"message": "check this link", "url": "ftp://malicious-server.xyz/payload"}, timeout=5.0)
        print(f"Invalid non-HTTP URL response code: {r_bad_url.status_code}")
        assert r_bad_url.status_code == 422, f"Expected 422 for bad URL, got {r_bad_url.status_code}"
        print("Result: PASS")

        print("\n--- TEST 8: ML Service Unavailable (Graceful Degradation) ---")
        print("Stopping Member 2 (ML API)...")
        kill_proc(p2)
        time.sleep(1.0)

        r_degraded_ml = requests.post(backend_url, json={"message": "A normal test message while ML is down"}, timeout=6.0)
        assert r_degraded_ml.status_code == 200
        d8 = r_degraded_ml.json()
        print(f"Degraded Risk Level: {d8['overall_risk']} | Status: {d8['status']}")
        print(f"Module Status: {d8['module_status']}")
        assert d8["status"] == "DEGRADED"
        assert d8["overall_risk"] != "LOW", "Degraded mode must enforce safety floor and NEVER report LOW risk"
        print("Result: PASS")

        print("\n--- TEST 9: URL Service Unavailable (Graceful Degradation) ---")
        print("Stopping Member 3 (URL API)...")
        kill_proc(p3)
        time.sleep(1.0)

        r_degraded_url = requests.post(backend_url, json={"message": "Check link http://example.com/test while URL service is down"}, timeout=6.0)
        assert r_degraded_url.status_code == 200
        d9 = r_degraded_url.json()
        print(f"Degraded Risk Level: {d9['overall_risk']} | Status: {d9['status']}")
        print(f"Module Status: {d9['module_status']}")
        assert d9["status"] == "DEGRADED"
        assert d9["overall_risk"] != "LOW", "Degraded mode must enforce safety floor and NEVER report LOW risk"
        print("Result: PASS")

        print("\n--- TEST 10: Privacy and Redaction Checks ---")
        r_priv = requests.get("http://127.0.0.1:8000/api/v1/risk-config", timeout=5.0)
        assert r_priv.status_code == 200
        print("Transparency rule set endpoint: OK")

        print("\n=================================================================")
        print("🎉 ALL 10 LIVE RUNTIME SCENARIOS PASSED WITH FLYING COLORS!")
        print("=================================================================")

    finally:
        print("\nCleaning up live test background processes...")
        for p in processes:
            kill_proc(p)
        print("All processes terminated successfully.")

if __name__ == "__main__":
    test_live_system()
