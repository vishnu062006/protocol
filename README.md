# Sequential Sum API

A secure RESTful API built with Python (Flask) that accepts a list of numbers and returns their sequential sum. Protected by API Key authentication via a custom request header.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Language | Python 3.10+ |
| Framework | Flask 3.x |
| Server (prod) | Gunicorn |
| Auth | API Key via `X-API-KEY` header |
| Testing | pytest |

---

## Project Structure

```
sequential-sum-api/
├── app.py              # Main application — routes, auth, logic
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment config (Render / Railway / Heroku)
├── .env.example        # Template for your secret key
├── .gitignore
├── tests/
│   └── test_app.py     # 10 unit tests covering auth + edge cases
└── README.md
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/sequential-sum-api.git
cd sequential-sum-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

```bash
cp .env.example .env
# Open .env and set:  API_KEY=your-secret-key-here
```

### 5. Run the server

```bash
python app.py
```

Server starts at `http://localhost:5000`.

---

## API Reference

### `GET /health`

Simple liveness check. No authentication required.

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{ "status": "ok" }
```

---

### `POST /sum`

Calculates the sequential sum of a list of numbers.

**Request Headers:**

| Header | Required | Description |
|---|---|---|
| `X-API-KEY` | ✅ Yes | Your secret API key |
| `Content-Type` | ✅ Yes | Must be `application/json` |

**Request Body:**

```json
{
  "numbers": [5, 10, 15]
}
```

**Response (200 OK):**

```json
{
  "input": [5, 10, 15],
  "result": 30,
  "count": 3
}
```

---

## Sample curl Commands

### ✅ Successful request

```bash
curl -X POST http://localhost:5000/sum \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-secret-key-here" \
  -d '{"numbers": [5, 10, 15]}'
```

**Expected response:**
```json
{
  "input": [5, 10, 15],
  "result": 30,
  "count": 3
}
```

---

### ❌ Missing API key (401 Unauthorized)

```bash
curl -X POST http://localhost:5000/sum \
  -H "Content-Type: application/json" \
  -d '{"numbers": [5, 10, 15]}'
```

**Expected response:**
```json
{
  "error": "Unauthorized",
  "message": "Missing X-API-KEY header"
}
```

---

### ❌ Invalid API key (403 Forbidden)

```bash
curl -X POST http://localhost:5000/sum \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: wrong-key" \
  -d '{"numbers": [5, 10, 15]}'
```

**Expected response:**
```json
{
  "error": "Forbidden",
  "message": "Invalid API key"
}
```

---

## Error Responses Summary

| Status | Scenario |
|---|---|
| `200 OK` | Valid request, sum returned |
| `400 Bad Request` | Missing/invalid `numbers` field, non-numeric values |
| `401 Unauthorized` | `X-API-KEY` header not present |
| `403 Forbidden` | `X-API-KEY` header present but incorrect |

---

## Running Tests

```bash
python -m pytest tests/ -v
```

All 10 tests cover: authentication, valid sums, empty lists, floats, negatives, and malformed input.

---

## Deployment

This project is ready to deploy on **Render**, **Railway**, or **Heroku** using the included `Procfile`.

### Steps (Render example):
1. Push code to your public GitHub repository.
2. Create a new **Web Service** on [render.com](https://render.com), linked to the repo.
3. Set the environment variable `API_KEY` in the Render dashboard (never commit `.env`).
4. Deploy — Render auto-detects the `Procfile` and runs `gunicorn app:app`.

---

## Security Notes

- The API key is loaded from an **environment variable**, never hardcoded.
- `.env` is in `.gitignore` — secrets never touch version control.
- Auth is enforced via a **decorator** (`@require_api_key`) so it's impossible to accidentally expose the endpoint without it.
