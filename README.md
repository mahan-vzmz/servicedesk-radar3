# Enterprise AI Retrieval Infrastructure

AI-powered retrieval platform for enterprise helpdesk systems.

This project provides intelligent ticket search, knowledge retrieval, and incident detection using modern Information Retrieval (IR) and Natural Language Processing (NLP) techniques.

---

## Overview

Traditional helpdesk systems rely heavily on keyword matching, which often fails to capture semantic meaning and user intent.

This project introduces a multi-stage retrieval architecture that combines:

- Semantic Search
- Keyword Search
- Hybrid Retrieval
- Cross-Encoder Reranking
- Knowledge Base Retrieval
- Incident Detection
- Evaluation Metrics

The system is designed to serve as an AI Infrastructure layer for enterprise helpdesk platforms.

---

## Features

### Semantic Ticket Search

Retrieve semantically similar tickets using dense vector embeddings.

### Hybrid Retrieval

Combine:

- Semantic Search (Vector Search)
- Keyword Search (Lexical Search)

for improved retrieval quality.

### Cross-Encoder Reranking

Apply deep relevance ranking on retrieved candidates to improve final result ordering.

### Knowledge Base Search

Retrieve troubleshooting articles and internal documentation relevant to user queries.

### Incident Detection

Identify potential enterprise-wide incidents by analyzing similar historical tickets.

### Retrieval Evaluation

Evaluate retrieval performance using:

- Precision@K
- Recall@K
- Mean Reciprocal Rank (MRR)

### Metadata Filtering

Support filtering by:

- Department
- Tenant

### Dockerized Deployment

Run the entire infrastructure using Docker and Docker Compose.

---

# Architecture

```text
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FastAPI   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│   Hybrid Retrieval      │
├─────────────────────────┤
│ Semantic Search(Qdrant) │
│ Keyword Search          │
│ Score Fusion            │
└──────────┬──────────────┘
           │
           ▼
┌────────────────────┐
│ Cross Encoder Rank │
└─────────┬──────────┘
          │
          ▼
 ┌──────────────────┐
 │ Incident Engine  │
 └────────┬─────────┘
          │
          ▼
 ┌──────────────────┐
 │ Final Response   │
 └──────────────────┘
```

---

# Retrieval Pipeline

```text
Query
  ↓
Embedding Generation
  ↓
Semantic Retrieval (Qdrant)
  ↓
Keyword Retrieval
  ↓
Score Fusion
  ↓
Cross-Encoder Reranking
  ↓
Final Results
```

---

# Tech Stack

| Layer | Technology |
|---------|-------------|
| API | FastAPI |
| Language | Python |
| Embeddings | Sentence Transformers |
| Vector Database | Qdrant |
| Reranking | Cross Encoder |
| Containerization | Docker |
| Evaluation | Precision@K, Recall@K, MRR |

---

# Project Structure

```text
app/
│
├── api/
│   └── routes/
│       ├── tickets.py
│       ├── incidents.py
│       ├── knowledge.py
│       └── evaluation.py
│
├── core/
│   └── startup.py
│
├── services/
│   ├── infrastructure_service.py
│   ├── incident_service.py
│   ├── knowledge_service.py
│   └── evaluation_service.py
│
├── infrastructure/
│
│   ├── data/
│   │   ├── fake_tickets.py
│   │   └── fake_articles.py
│   │
│   ├── embeddings/
│   │   └── embedding_service.py
│   │
│   ├── vector_db/
│   │   ├── qdrant_client.py
│   │   └── qdrant_store.py
│   │
│   ├── retrieval/
│   │   ├── qdrant/
│   │   ├── keyword/
│   │   └── hybrid/
│   │
│   ├── reranking/
│   │   └── cross_encoder_reranker.py
│   │
│   ├── incidents/
│   │   └── incident_detector.py
│   │
│   └── evaluation/
│       ├── metrics.py
│       └── evaluation_dataset.py
│
└── main.py
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-repository.git

cd your-repository
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

```bash
source venv/bin/activate
```

or

```powershell
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running with Docker

```bash
docker compose up --build
```

Services:

| Service | Port |
|----------|--------|
| FastAPI | 8000 |
| Qdrant | 6333 |

---

# API Endpoints

## Similar Tickets

### Request

```http
POST /tickets/similar
```

### Example

```json
{
  "query": "VPN MFA issue"
}
```

---

## Incident Detection

### Request

```http
POST /incidents/detect
```

### Example

```json
{
  "query": "VPN login failed"
}
```

---

## Knowledge Search

### Request

```http
GET /knowledge/search?query=VPN issue
```

---

## Retrieval Evaluation

### Request

```http
GET /evaluation/retrieval
```

---

# Embedding Model

Model:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

Reasons:

- Multilingual support
- Lightweight
- Fast inference
- Suitable for semantic retrieval
- 384-dimensional vectors

---

# Reranking Model

Model:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Purpose:

- Deep relevance estimation
- Final ranking optimization
- Improved retrieval precision

---

# Evaluation Metrics

The retrieval system is evaluated using:

## Precision@K

Measures how many retrieved documents are relevant.

## Recall@K

Measures how many relevant documents are retrieved.

## Mean Reciprocal Rank (MRR)

Measures ranking quality of the first relevant result.

---

# Example Evaluation Output

```json
{
  "mean_precision@5": 0.64,
  "mean_recall@5": 0.91,
  "mean_mrr": 0.88
}
```

---

# Future Improvements

- Reciprocal Rank Fusion (RRF)
- Redis Cache Layer
- LLM-powered Answer Generation
- Real Enterprise Dataset
- Multi-Tenant Security
- Role-Based Access Control
- Retrieval-Augmented Generation (RAG)
- Observability & Monitoring

---

# Educational Goals

This project demonstrates practical implementation of:

- Information Retrieval
- Semantic Search
- Vector Databases
- Retrieval Pipelines
- Ranking Systems
- NLP Infrastructure
- Enterprise AI Architecture

---

# License

MIT License