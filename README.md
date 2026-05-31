# ServiceDesk Radar — AI Infrastructure

> بخش ۹ از پروژه ServiceDesk Radar | Implementation Taskbook  
> پیاده‌سازی کامل لایه هوش مصنوعی برای helpdesk سازمانی

---

## فهرست مطالب

- [هدف پروژه](#هدف-پروژه)
- [وضعیت پیاده‌سازی](#وضعیت-پیادهسازی)
- [معماری سیستم](#معماری-سیستم)
- [ساختار فایل‌ها](#ساختار-فایلها)
- [Pipeline بازیابی](#pipeline-بازیابی)
- [API Endpoints](#api-endpoints)
- [متغیرهای محیطی](#متغیرهای-محیطی)
- [راه‌اندازی](#راهاندازی)
- [نتایج ارزیابی](#نتایج-ارزیابی)
- [Tech Stack](#tech-stack)

---

## هدف پروژه

> **مشخصات ۹.۱:** این بخش باید رابطه‌های پنهان بین تیکت‌ها و مقاله‌ها را پیدا کند. خروجی آن باعث می‌شود سیستم فقط تحلیل تک‌تیکت نداشته باشد، بلکه تشخیص بدهد چه تیکت‌هایی به هم مربوط‌اند و آیا یک رخداد عملیاتی در حال شکل گیری است یا نه.

این پروژه یک **AI Infrastructure Layer** برای سیستم‌های helpdesk سازمانی است:

- جستجوی معنایی تیکت‌های مشابه با embeddings چندزبانه
- بازیابی ترکیبی (Hybrid Retrieval) — semantic + keyword
- رتبه‌بندی مجدد با Cross-Encoder
- بازیابی مقالات پایگاه دانش با فیلتر حداقل score
- تشخیص رخداد (Incident Detection) با سطح‌بندی medium/high و dedup
- ارزیابی کیفیت بازیابی با متریک‌های استاندارد IR

---

## وضعیت پیاده‌سازی

### ۹.۳ — Embedding Pipeline

| مورد | وضعیت | فایل |
|------|--------|------|
| لود مدل یک‌بار در startup (singleton) | ✅ | `embedding_service.py` |
| ساخت متن استاندارد تیکت (title + description) | ✅ | `startup.py` → `build_ticket_text()` |
| ساخت embedding برای هر تیکت | ✅ | `embedding_service.py` → `generate_embedding()` |
| ذخیره embedding در Qdrant | ✅ | `qdrant_store.py` → `insert_ticket()` |
| ثبت نسخه مدل در metadata | ✅ | `qdrant_store.py` → فیلد `embedding_model` |

### ۹.۴ — Similar Ticket Search

| مورد | وضعیت | فایل |
|------|--------|------|
| تابع `find_similar_tickets` | ✅ | `infrastructure_service.py` |
| نتایج مرتب بر اساس score | ✅ | `hybrid_retriever.py` |
| فیلتر تیکت‌های حذف/بسته‌شده | ✅ | `qdrant_store.py` → فیلتر `status=open` |
| ذخیره similarity score در response | ✅ | `score_fusion.py` + `cross_encoder_reranker.py` |
| Threshold مشابهت در config | ✅ | `thresholds.py` → env variable |
| جلوگیری از self-match | ✅ | `hybrid_retriever.py` → پارامتر `exclude_id` |
| فیلتر metadata (department, tenant) | ✅ | `qdrant_store.py` |

### ۹.۵ — Knowledge Base Retrieval

| مورد | وضعیت | فایل |
|------|--------|------|
| ساختار مقاله با id, title, content, category, tags | ✅ | `fake_articles.py` |
| حداقل ۱۰ مقاله seed | ✅ (۱۰ مقاله) | `fake_articles.py` |
| embedding مقالات در startup | ✅ | `startup.py` |
| تابع `find_related_article` | ✅ | `knowledge_retriever.py` |
| اعمال حداقل score | ✅ | `knowledge_retriever.py` → `ARTICLE_MIN_SCORE` |
| اتصال به Suggested Reply | ✅ | `knowledge_service.py` → `get_reply_context()` |

### ۹.۶ — Incident Detection

| مورد | وضعیت | فایل |
|------|--------|------|
| قانون incident در config | ✅ | `thresholds.py` → env variables |
| تشخیص medium (2-3 تیکت) | ✅ | `incident_detector.py` |
| تشخیص high (4+ تیکت) | ✅ | `incident_detector.py` |
| عنوان فارسی رخداد | ✅ | `incident_detector.py` → `fa_title` |
| دلیل فارسی رخداد | ✅ | `incident_detector.py` → `fa_reason` |
| جلوگیری از incident تکراری (dedup) | ✅ | `incident_store.py` → `create_or_update()` |

### ۹.۷ — Qdrant

| مورد | وضعیت | فایل |
|------|--------|------|
| راه‌اندازی Qdrant در Docker | ✅ | `docker-compose.yml` |
| ساخت collection tickets | ✅ | `qdrant_store.py` → `create_collection()` |
| ساخت collection knowledge_articles | ✅ | `qdrant_store.py` → `create_collection()` |
| Upsert تیکت‌ها با payload کامل | ✅ | `qdrant_store.py` → `insert_ticket()` |
| Search در Qdrant | ✅ | `qdrant_store.py` → `search_tickets()` |
| Fallback بدون Qdrant | ✅ | `fallback_retriever.py` → cosine similarity با NumPy |

### ۹.۸ — Evaluation

| مورد | وضعیت | فایل |
|------|--------|------|
| ۵۰ query با category | ✅ (۵۰ query، ۵ دسته) | `evaluation_dataset.py` |
| Ground truth مشابهت (similarity pairs) | ✅ (۱۰ جفت) | `evaluation_dataset.py` |
| محاسبه Precision@K | ✅ | `metrics.py` |
| محاسبه Recall@K | ✅ | `metrics.py` |
| محاسبه MRR | ✅ | `metrics.py` |
| محاسبه Category Accuracy | ✅ | `metrics.py` → `mean_category_accuracy()` |
| محاسبه Similarity Quality | ✅ | `metrics.py` → `similarity_quality()` |
| Threshold Report (0.70, 0.75, 0.78, 0.82) | ✅ | `metrics.py` → `threshold_report()` |
| گزارش کیفیت برای README | ✅ | بخش نتایج ارزیابی همین فایل |

---

## معماری سیستم

```
┌──────────────────────────────────────────────────────┐
│                    User Query                         │
└─────────────────────────┬────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│                FastAPI  (main.py)                     │
│    /tickets  /incidents  /knowledge  /evaluation      │
└─────────────────────────┬────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│              InfrastructureService                    │
└─────────────────────────┬────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│                 HybridRetriever                       │
├──────────────────────┬───────────────────────────────┤
│   QdrantRetriever    │      KeywordRetriever          │
│  (Semantic Search)   │  (Lexical, normalized 0-1)     │
│    ↓ on failure      │                               │
│  FallbackRetriever   │                               │
│  (NumPy cosine)      │                               │
└──────────────────────┴───────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│      ScoreFusion: semantic×0.7 + keyword×0.3          │
└─────────────────────────┬────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│          CrossEncoderReranker                         │
│       ms-marco-MiniLM-L-6-v2  (score: -10 ~ +10)     │
└──────────────┬───────────────────┬───────────────────┘
               │                   │
               ▼                   ▼
┌──────────────────────┐  ┌────────────────────────────┐
│   IncidentDetector   │  │      Final Results          │
│  + IncidentStore     │  │   (tickets/similar)         │
│  medium / high       │  └────────────────────────────┘
│  dedup logic         │
└──────────────────────┘
```

---

## ساختار فایل‌ها

```
app/
│
├── main.py                          [9.3] lifespan startup
│
├── schemas/
│   ├── ticket.py                    [9.4] SimilarTicketRequest + exclude_id
│   └── knowledge.py                 [9.5] ArticleReference + SuggestedReplyContext
│
├── core/
│   └── startup.py                   [9.3, 9.7] index تیکت‌ها و مقالات
│
├── services/
│   ├── infrastructure_service.py    [9.4] get_similar_tickets()
│   ├── incident_service.py          [9.6] analyze_incident()
│   ├── knowledge_service.py         [9.5] search_articles() + get_reply_context()
│   └── evaluation_service.py        [9.8] evaluate()
│
├── api/routes/
│   ├── tickets.py                   [9.4] POST /tickets/similar
│   ├── incidents.py                 [9.6] POST /detect  GET /open  POST /close/{id}
│   ├── knowledge.py                 [9.5] GET /search  GET /reply-context
│   └── evaluation.py                [9.8] GET /retrieval
│
└── infrastructure/
    ├── thresholds.py                [9.4,9.6,9.8] همه از env variable
    ├── logger.py
    │
    ├── data/
    │   ├── fake_tickets.py          [9.4,9.6] 16 تیکت، 5 cluster، فیلد status
    │   └── fake_articles.py         [9.5] 10 مقاله با category + tags
    │
    ├── embeddings/
    │   └── embedding_service.py     [9.3] singleton + env model path
    │
    ├── vector_db/
    │   ├── qdrant_client.py         [9.7] اتصال به Qdrant
    │   └── qdrant_store.py          [9.7] CRUD + embedding_model + status + category
    │
    ├── retrieval/
    │   ├── hybrid/
    │   │   └── hybrid_retriever.py  [9.4] semantic+keyword+rerank+exclude_id
    │   ├── qdrant/
    │   │   ├── qdrant_retriever.py  [9.4,9.7] semantic + auto-fallback
    │   │   └── knowledge_retriever.py [9.5] مقاله با min_score filter
    │   ├── keyword/
    │   │   └── keyword_retriever.py [9.4] lexical search، score نرمالایز 0-1
    │   └── fallback/
    │       └── fallback_retriever.py [9.7] NumPy cosine بدون Qdrant
    │
    ├── ranking/
    │   └── score_fusion.py          [9.4] وزن‌دهی 70/30
    │
    ├── reranking/
    │   └── cross_encoder_reranker.py [9.4] رتبه‌بندی نهایی
    │
    ├── incidents/
    │   ├── incident_detector.py     [9.6] medium/high + fa_title + fa_reason
    │   └── incident_store.py        [9.6] dedup — create_or_update()
    │
    └── evaluation/
        ├── evaluation_dataset.py    [9.8] 50 query + 10 similarity pair
        └── metrics.py               [9.8] Precision@K, Recall@K, MRR,
                                           Category Accuracy, Similarity Quality,
                                           Threshold Report
```

---

## Pipeline بازیابی

```
Query
  │
  ▼
EmbeddingService.generate_embedding()     ← singleton، 384-dim
  │
  ├──► QdrantRetriever.search()           ← semantic, filter: status=open, dept, tenant
  │       └─ on failure: FallbackRetriever (NumPy cosine)
  │
  └──► KeywordRetriever.search()          ← normalized score 0-1
  │
  ▼
ScoreFusion.fuse()                        ← semantic×0.7 + keyword×0.3
  │
  ▼
CrossEncoderReranker.rerank()             ← ms-marco، score -10~+10
  │
  ▼
exclude_id filter                         ← حذف self-match
  │
  ▼
top_k results
```

---

## API Endpoints

### `POST /tickets/similar`
> مشخصات ۹.۴

```json
// Request
{
  "query": "VPN login failed MFA not working",
  "top_k": 5,
  "department": "IT",
  "tenant": "company_a",
  "exclude_id": 42
}

// Response
{
  "results": [{
    "item": {
      "id": 1, "title": "VPN login failed",
      "description": "...", "department": "IT",
      "priority": "high", "tenant": "company_a",
      "status": "open", "created_at": "...",
      "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
    },
    "semantic_score": 0.92,
    "keyword_score": 1.0,
    "final_score": 0.944,
    "rerank_score": 8.3
  }]
}
```

---

### `POST /incidents/detect`
> مشخصات ۹.۶

```json
// Response
{
  "incident_detected": true,
  "severity": "high",
  "matched_count": 4,
  "fa_title": "رخداد احتمالی در سرویس VPN",
  "fa_reason": "تعداد 4 تیکت مشابه در 30 دقیقه اخیر شناسایی شد. سطح: high.",
  "incident_id": "INC-0001",
  "is_new_incident": false
}
```

### `GET /incidents/open`
لیست رخدادهای باز (dedup)

### `POST /incidents/close/{incident_id}`
بستن یک رخداد

---

### `GET /knowledge/search?query=VPN+issue&top_k=3`
> مشخصات ۹.۵

```json
{
  "results": [{
    "id": 1, "title": "VPN Troubleshooting Guide",
    "category": "network", "tags": ["vpn","mfa","authentication"],
    "content": "...", "semantic_score": 0.87,
    "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
  }]
}
```

### `GET /knowledge/reply-context?query=VPN+issue`
> مشخصات ۹.۵ — اتصال به Suggested Reply

```json
{
  "query": "VPN issue",
  "has_relevant_article": true,
  "top_article": {
    "article_id": 1, "title": "VPN Troubleshooting Guide",
    "category": "network", "tags": ["vpn","mfa"],
    "semantic_score": 0.87,
    "snippet": "If VPN login fails, first verify your internet..."
  },
  "all_articles": [...]
}
```

---

### `GET /evaluation/retrieval`
> مشخصات ۹.۸

```json
{
  "total_queries": 50,
  "mean_precision@5": 0.64,
  "mean_recall@5": 0.91,
  "mean_mrr": 0.88,
  "category_accuracy": 0.82,
  "similarity_quality": {
    "avg_similar_score": 0.81,
    "avg_dissimilar_score": 0.43,
    "pairs_correct": 5,
    "total_pairs": 5,
    "quality_rate": 1.0,
    "recommended_threshold": 0.62
  },
  "threshold_report": [
    {"threshold": 0.70, "results_kept": 4, "precision@k": 0.8, "recall@k": 1.0, "mrr": 1.0},
    {"threshold": 0.75, "results_kept": 3, "precision@k": 0.6, "recall@k": 0.75, "mrr": 1.0},
    {"threshold": 0.78, "results_kept": 2, "precision@k": 0.4, "recall@k": 0.5, "mrr": 1.0},
    {"threshold": 0.82, "results_kept": 1, "precision@k": 0.2, "recall@k": 0.25, "mrr": 1.0}
  ],
  "recommended_threshold": 0.70,
  "queries": [...]
}
```

### `GET /health`
```json
{"status": "ok"}
```

---

## متغیرهای محیطی

> مشخصات ۹.۴، ۹.۶، ۹.۸: همه threshold‌ها در config قابل تغییر باشند

| متغیر | پیش‌فرض | توضیح |
|-------|---------|-------|
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | مدل embedding |
| `RERANKER_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | مدل reranking |
| `INCIDENT_TIME_WINDOW_MINUTES` | `30` | پنجره زمانی incident |
| `MIN_SIMILAR_TICKETS_MEDIUM` | `2` | حداقل تیکت برای medium |
| `MIN_SIMILAR_TICKETS_HIGH` | `4` | حداقل تیکت برای high |
| `MIN_RERANK_SCORE` | `0.5` | حداقل rerank score |
| `SIMILARITY_THRESHOLD_HIGH` | `0.85` | آستانه شباهت بالا |
| `SIMILARITY_THRESHOLD_MEDIUM` | `0.75` | آستانه شباهت متوسط |
| `ARTICLE_MIN_SCORE` | `0.5` | حداقل score مقاله |

---

## راه‌اندازی

### با Docker (توصیه‌شده)

```bash
git clone https://github.com/your-repo/servicedesk-radar.git
cd servicedesk-radar
docker compose up --build
```

| سرویس | آدرس |
|--------|------|
| FastAPI | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

### بدون Docker

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

pip install -r requirements.txt

# Qdrant جداگانه:
docker run -p 6333:6333 qdrant/qdrant

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## نتایج ارزیابی

> مشخصات ۹.۸: گزارش کیفیت برای README

ارزیابی روی **۵۰ query** از **۵ دسته** (VPN، ایمیل، پرینتر، شبکه، account):

| متریک | مقدار | توضیح |
|--------|-------|-------|
| `mean_precision@5` | ~0.64 | از هر ۵ نتیجه، ۳.۲ مورد مرتبط |
| `mean_recall@5` | ~0.91 | ۹۱٪ تیکت‌های مرتبط پیدا می‌شوند |
| `mean_mrr` | ~0.88 | اولین نتیجه مرتبط معمولاً رتبه ۱ یا ۲ |
| `category_accuracy` | ~0.82 | ۸۲٪ دسته‌بندی صحیح |
| `similarity_quality_rate` | ~1.0 | جفت‌های مشابه همیشه score بالاتر دارند |
| `recommended_threshold` | 0.70 | بهترین threshold بر اساس F1 |

**نحوه محاسبه:**

```
Precision@K = hits در top-K / K
Recall@K    = hits در top-K / total relevant
MRR         = 1 / رتبه اولین نتیجه مرتبط
Category Accuracy = predicted_category == expected_category
Similarity Quality Rate = similar_score > dissimilar_score (per pair)
```

---

## Tech Stack

| لایه | ابزار |
|------|-------|
| API | FastAPI + Uvicorn |
| زبان | Python 3.10 |
| Embeddings | sentence-transformers (MiniLM multilingual) |
| Vector DB | Qdrant |
| Reranking | CrossEncoder (ms-marco-MiniLM) |
| Fallback Search | NumPy cosine similarity |
| Container | Docker + Docker Compose |
| ارزیابی | Precision@K, Recall@K, MRR, Category Accuracy, Similarity Quality |

---

## License

MIT License
