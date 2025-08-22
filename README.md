# Infra Microservice Demo

A demo microservices project showcasing a **central backend service** managing multiple services with centralized configuration, CLI deployment, and repository patterns.  

---

## Overview

This project runs **3 microservices**:

1. **Backend Service** – The main service that:
   - Manages configurations in MongoDB  
   - Provides REST aggregator endpoints  
   - Implements repository layer and protocol abstractions  
   - Includes CLI tools for environment management and deployment  

2. **Users Service** – Handles user data and profiles.  

3. **Orders Service** – Manages order data for users.  

---

## Features

- Centralized **configuration management** via MongoDB  
- CLI tools (`create-env`, `edit-env`, `list-envs`, `deploy`)  
- Environment-aware deployments (`dev`, `demo`, `staging`, `prod`)  
- Dockerized setup for local demo  
- Repository and protocol pattern for clean code separation  

---

## Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/) installed  
- Python 3.12+ (for running CLI tools)  
- MongoDB is containerized via Docker (no local installation required)  

---

## Installation

1. Clone the repository:

```bash
git clone <repo_url>
cd FastApi_BE/backend
```

## Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate  # Windows

**or**

source .venv/bin/activate  # Linux/macOS

## Running the Project (Docker Only)
docker compose up -d

> This starts:
- Backend service
- Users service
- Orders service
- MongoDB

# Project Structure
```bash
FastApi_BE/
├── backend/                 # FastAPI backend service
│   ├── config_loader.py     # Loads configuration from MongoDB or .env
│   ├── models.py            # Pydantic models for Config & FeatureFlags
│   ├── repository/          # Mongo repository layer
│   ├── protocols.py         # Protocol definitions for repo
│   ├── Dockerfile           # Backend Dockerfile
│   └── main.py              # FastAPI routes
├── docs                     # Documents Folder
├── docker-compose.yml       # Docker Compose for all services
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```