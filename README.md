# URL Shortener & Analytics

A full-stack URL shortening application built using FastAPI, Streamlit, SQLAlchemy, and SQLite.

## Features

- Generate unique shortened URLs
- Redirect users to original websites
- Track URL clicks
- Store URL records in a database
- Interactive analytics dashboard
- Click performance visualizations
- Export analytics as CSV
- REST API with interactive documentation

## Technologies

- Python
- FastAPI
- Streamlit
- SQLAlchemy
- SQLite
- Pandas
- Plotly

## Architecture

Streamlit Dashboard → FastAPI REST API → SQLite Database

## Installation

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend:

```bash
python -m uvicorn main:app --reload
```

In a second terminal, start the dashboard:

```bash
python -m streamlit run dashboard.py
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | API health check |
| POST | /shorten | Create shortened URL |
| GET | /analytics | Retrieve URL statistics |
| GET | /{short_code} | Redirect to original URL |

## Future Improvements

- Custom short URLs
- QR code generation
- URL expiration
- Authentication
- Persistent cloud database
- Advanced visitor analytics