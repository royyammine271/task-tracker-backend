# Module 4 Task Tracker

## Final Project

Branch reviewed: final-project

### What this submission demonstrates
- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- Docker image builds and runs with /health returning 200.
- AI review, security, and ownership evidence is in docs/.

### How to run locally
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Health check:
```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health
```

### How to run tests
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Verified result in this environment: `35 passed, 3 warnings in 0.51s`.

### How to run with Docker
```powershell
docker build -t task-tracker:release .
docker run --rm -d --name task-tracker-verify -p 8010:8000 task-tracker:release
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8010/health
```

Verified result: HTTP 200 OK from the containerized app.

### Evidence files
- docs/release-evidence.md
- docs/final-ai-review.md
- docs/ai-playbook.md

### AI assistance summary
AI helped draft or review: CI / Docker / docs / security / debugging.
I verified the work by: tests / diff review / Docker / /health / manual scan.
One AI suggestion I rejected or corrected: I rejected the idea of claiming Docker success without a real runtime check and corrected the wording to state only the verified HTTP 200 result.

---

