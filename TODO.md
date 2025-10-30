# DE5 Chat Assistant Backend TODO

- [x] Create requirements.txt with necessary dependencies
- [x] Create config.py to store OpenAI API key
- [x] Create db.py for SQLite database setup with leads table
- [x] Create knowledge_base.py to scrape DE5 website and build vector store
- [x] Create main.py with FastAPI endpoints for /chat and /leads
- [x] Install dependencies using pip install -r requirements.txt
- [x] Run knowledge_base.py to build the knowledge base
- [x] Run uvicorn main:app --reload to start the server
- [x] Test the endpoints (JSON parsing issue in curl - resolved with Python script)
