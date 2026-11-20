web: streamlit run silvershield_frontend.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false
api: uvicorn app.main:app --host 0.0.0.0 --port $PORT
