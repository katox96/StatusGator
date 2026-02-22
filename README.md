# 1. Go to root dir(StatusGator) of the project
cd <path>/StatusGator

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start the FastAPI server
uvicorn app.main:app --reload --port 10000

---
API docs - Swagger UI
http://localhost:10000/docs

---
API Endpoints
Get all incidents
curl http://localhost:10000/incidents

Get incidents for a specific date
curl "http://localhost:10000/incidents?incident_date=2026-02-20"

Filter incidents by feed
curl "http://localhost:10000/incidents?feed=openai"

Register a new feed
curl -X POST http://localhost:10000/feeds \
     -H "Content-Type: application/json" \
     -d '{
           "name": "stripe",
           "url": "https://status.stripe.com/rss"
         }'