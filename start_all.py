"""
SilverShield AI - Master Multi-Service Launcher
Launches all integrated components with a single command:
- Member 1: Streamlit Accessibility Frontend (Port 8501)
- Member 2: ML Scam Prediction API (Port 8001)
- Member 3: URL Security & Privacy API (Port 8002)
- Member 4: Central Risk Aggregator & Integration API (Port 8000)
"""
import sys
import time
import subprocess
import argparse
from pathlib import Path

ROOT = Path(__file__).parent


def run_service(cmd, name):
    print(f"🚀 Starting {name}...")
    proc = subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        shell=True
    )
    return proc


def main():
    parser = argparse.ArgumentParser(description="SilverShield AI Launcher")
    parser.add_argument("--backend-only", action="store_true", help="Launch only Member 4 FastAPI Backend")
    parser.add_argument("--frontend-only", action="store_true", help="Launch only Member 1 Streamlit Frontend")
    parser.add_argument("--mocks-only", action="store_true", help="Launch only Member 2 & 3 Mock APIs")
    args = parser.parse_args()

    python_bin = sys.executable
    processes = []

    try:
        if args.backend_only:
            proc = run_service(f'"{python_bin}" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload', "Member 4 FastAPI Backend")
            processes.append(proc)
        elif args.frontend_only:
            proc = run_service(f'"{python_bin}" -m streamlit run silvershield_frontend.py', "Member 1 Streamlit Frontend")
            processes.append(proc)
        elif args.mocks_only:
            p2 = run_service(f'"{python_bin}" -m uvicorn mocks.mock_member2_ml:app --host 127.0.0.1 --port 8001', "Member 2 ML Scam Service")
            p3 = run_service(f'"{python_bin}" -m uvicorn mocks.mock_member3_url:app --host 127.0.0.1 --port 8002', "Member 3 URL Security Service")
            processes.extend([p2, p3])
        else:
            # Default: Launch Everything!
            print("================================================================")
            print("🛡️  SilverShield AI: Launching Full Integrated System")
            print("================================================================")
            p2 = run_service(f'"{python_bin}" -m uvicorn mocks.mock_member2_ml:app --host 127.0.0.1 --port 8001', "Member 2 ML Service (Port 8001)")
            p3 = run_service(f'"{python_bin}" -m uvicorn mocks.mock_member3_url:app --host 127.0.0.1 --port 8002', "Member 3 URL Service (Port 8002)")
            time.sleep(1.5)

            p4 = run_service(f'"{python_bin}" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000', "Member 4 Central Integration API (Port 8000)")
            time.sleep(1.5)

            p1 = run_service(f'"{python_bin}" -m streamlit run silvershield_frontend.py --server.port 8501', "Member 1 Streamlit Frontend (Port 8501)")
            processes.extend([p2, p3, p4, p1])

            print("\n✅ All services running!")
            print("👉 Open your browser at: http://localhost:8501")
            print("👉 Backend API Swagger docs: http://localhost:8000/docs")
            print("Press Ctrl+C to stop all services.\n")

        for p in processes:
            p.wait()

    except KeyboardInterrupt:
        print("\n🛑 Shutting down all services...")
        for p in processes:
            p.terminate()
        print("Done.")


if __name__ == "__main__":
    main()
