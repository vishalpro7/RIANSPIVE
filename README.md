# 🛒 RIANSPIVE

> A modular, FastAPI-powered backend for end-to-end e-commerce order management — from product catalog to payments, shipments, and analytics.

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Status](https://img.shields.io/badge/status-in%20progress-yellow?style=flat)]()
[![License](https://img.shields.io/badge/license-MIT-green?style=flat)]()

---

## 📖 Overview

**RIANSPIVE** is a backend system built to simulate how a real-world e-commerce company handles orders at scale — covering everything from authentication and product catalogs to order processing, payments, shipment tracking, admin controls, and analytics.

It's built with **FastAPI** for speed and clean async APIs, **SQLAlchemy 2.0** for the ORM layer, and **Alembic** for versioned database migrations — a stack designed to mirror production-grade backend architecture rather than a single-file prototype.

> 🚧 **Status:** Actively in development as part of an academic Software Development Project (SDP). Core modules are being built out incrementally.

---

## ✨ Features

| Module | Description |
|---|---|
| 🔐 **Auth** | JWT-based authentication and authorization using `python-jose` and `passlib`/`bcrypt` |
| 📦 **Products** | Product catalog management |
| 🧾 **Orders** | Order creation, tracking, and lifecycle management |
| 💳 **Payments** | Payment processing workflows |
| 🛡️ **Admin** | Administrative controls and oversight |
| 🚚 **Shipments** | Shipment creation and tracking |
| 📊 **Analytics** | Reporting and business insights |

Each domain is isolated into its own router, model, and schema — making the codebase easy to extend, test, and reason about.

---

## 🏗️ Architecture

The project follows a clean, layered structure inspired by production FastAPI applications:

```
enterprise-order-management-platform/
├── alembic/          # Database migration scripts
├── auth/             # Authentication & authorization logic
├── database/          # DB session/connection setup
├── dependencies/       # Shared FastAPI dependencies (e.g. auth guards, DB sessions)
├── models/            # SQLAlchemy ORM models
├── routers/            # FastAPI route definitions (auth, products, orders, payments, admin, shipments, analytics)
├── schemas/            # Pydantic request/response schemas
├── services/           # Business logic layer
├── main.py             # Application entry point
├── alembic.ini          # Alembic configuration
└── requirements.txt      # Python dependencies
```

This separation of **routers → services → models** keeps HTTP handling, business logic, and data access decoupled — a pattern that scales well as more domains are added.

---

## 🛠️ Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) `0.116.1`
- **Server:** [Uvicorn](https://www.uvicorn.org/) `0.35.0`
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) `2.0.42`
- **Database:** PostgreSQL (via `psycopg2-binary`)
- **Migrations:** [Alembic](https://alembic.sqlalchemy.org/) `1.19.1`
- **Auth:** `python-jose[cryptography]` (JWT) + `passlib[bcrypt]` + `bcrypt`
- **Validation:** [Pydantic](https://docs.pydantic.dev/) `2.11.7` + `email-validator`
- **Forms/Uploads:** `python-multipart`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL running locally or remotely
- `pip` / a virtual environment tool

### Installation

```bash
# Clone the repository
git clone https://github.com/vishalpro7/enterprise-order-management-platform.git
cd enterprise-order-management-platform

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

1. Create a PostgreSQL database for the project.
2. Configure your database connection (e.g. via environment variables or a `.env` file, depending on `database/` setup).
3. Run migrations:

```bash
alembic upgrade head
```

### Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at **`http://127.0.0.1:8000`**, with interactive docs at:

- Swagger UI → `http://127.0.0.1:8000/docs`
- ReDoc → `http://127.0.0.1:8000/redoc`

---

## 📌 Roadmap

- [ ] Flesh out full CRUD for each router (products, orders, shipments)
- [ ] Add automated test suite (pytest)
- [ ] Add CI pipeline (GitHub Actions)
- [ ] Add Docker/Docker Compose setup for one-command local dev
- [ ] API documentation with example requests/responses
- [ ] Rate limiting & request validation hardening

---

## 🤝 Contributing

This is currently a solo academic project (SDP), but suggestions and issues are welcome. Feel free to open an issue if you spot a bug or have an idea for improvement.

---

## 📄 License

This project is open for educational reference. Add a `LICENSE` file (e.g. MIT) to formalize usage terms.

---

<p align="center">Built with ⚡ FastAPI, 🐘 PostgreSQL, and a lot of debugging.</p>
