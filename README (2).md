# CI/CD Pipeline

![CI/CD Status](https://github.com/YOUR_USERNAME/cicd-pipeline/actions/workflows/cicd.yml/badge.svg)
![Coverage](https://codecov.io/gh/YOUR_USERNAME/cicd-pipeline/branch/main/graph/badge.svg)
![Docker](https://img.shields.io/badge/docker-ghcr.io-blue)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue)

A production-grade CI/CD pipeline for a FastAPI microservice — featuring multi-stage GitHub Actions workflows, Docker containerisation, security scanning, automated deployment, and Slack notifications.

---

## Pipeline Stages

```
 Push / PR
     │
     ▼
┌─────────┐    ┌──────────────┐    ┌────────────────┐    ┌──────────────┐
│  LINT   │───▶│  TEST        │───▶│  BUILD         │───▶│  SECURITY    │
│         │    │              │    │                │    │              │
│ flake8  │    │ pytest       │    │ Docker image   │    │ Trivy scan   │
│ style   │    │ 3.10 + 3.11  │    │ Push to GHCR   │    │ SARIF report │
│ checks  │    │ + coverage   │    │ Layer cache    │    │ to Sec tab   │
└─────────┘    └──────────────┘    └────────────────┘    └──────────────┘
                                                                │
                                                                ▼
                                                       ┌──────────────┐    ┌──────────┐
                                                       │  DEPLOY      │───▶│  NOTIFY  │
                                                       │              │    │          │
                                                       │ Render hook  │    │ Slack    │
                                                       │ Health check │    │ webhook  │
                                                       │ Auto-rollback│    │ pass/fail│
                                                       └──────────────┘    └──────────┘
```

---

## Branch Strategy

| Branch | Purpose | Auto-deploy |
|--------|---------|-------------|
| `dev` | Feature development | No |
| `staging` | Pre-production testing | Build + scan only |
| `main` | Production | Full pipeline → Render |

PRs from `dev` → `staging` → `main` are required. Direct pushes to `main` are blocked via branch protection rules.

---

## Project Structure

```
cicd-pipeline/
├── app/
│   └── main.py                  # FastAPI application
├── tests/
│   └── test_app.py              # API test suite
├── .github/
│   └── workflows/
│       └── cicd.yml             # 6-stage CI/CD pipeline
├── Dockerfile                   # Multi-stage container build
└── requirements.txt
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root / welcome |
| GET | `/health` | Health check (used by deploy smoke test) |
| GET | `/metrics` | Runtime metrics |
| GET | `/coins` | List tracked coins |
| GET | `/coins/{coin_id}` | Coin detail |

---

## Pipeline Features

### Matrix Testing
Tests run in parallel across Python 3.10 and 3.11. A failure on either version blocks the build.

### Docker Layer Caching
GitHub Actions cache is used for Docker layer caching — subsequent builds complete significantly faster.

### Security Scanning
[Trivy](https://github.com/aquasecurity/trivy) scans the built Docker image for CVEs. Results are uploaded to the GitHub Security tab as SARIF — visible in the repo's **Security → Code scanning** section.

### Automated Rollback
The deploy job runs a health check against `/health` after deployment. If the response is not HTTP 200, the workflow exits with a failure, halting any further runs and surfacing the failure in Slack.

### GitHub Container Registry
Every successful build pushes to GHCR with three tags:
- `latest` — current main branch
- `main` / `staging` — branch tag
- `sha-<commit>` — immutable per-commit tag

---

## Setup

### 1. Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/cicd-pipeline
cd cicd-pipeline
```

### 2. Set repository secrets

In **Settings → Secrets and variables → Actions**, add:

| Secret | Value |
|--------|-------|
| `RENDER_DEPLOY_HOOK` | From Render dashboard → your service → Deploy Hook |
| `SLACK_WEBHOOK` | From Slack → Incoming Webhooks app |

### 3. Enable branch protection

In **Settings → Branches**, add a rule for `main`:
- ✅ Require status checks before merging
- ✅ Require branches to be up to date
- ✅ Required checks: `lint`, `test (3.10)`, `test (3.11)`, `build`, `security`

### 4. Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# API at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 5. Run tests

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

### 6. Build Docker image

```bash
docker build -t cicd-pipeline .
docker run -p 8000:8000 cicd-pipeline
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Application | FastAPI + uvicorn |
| Testing | pytest + pytest-cov |
| Linting | flake8 |
| Containerisation | Docker + GitHub Container Registry |
| Security scanning | Trivy |
| CI/CD | GitHub Actions |
| Deployment | Render |
| Notifications | Slack webhooks |
