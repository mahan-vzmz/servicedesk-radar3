# ServiceDesk Radar — AI Infrastructure

> بخش ۹ از پروژه ServiceDesk Radar | Implementation Taskbook
> پیاده‌سازی کامل لایه هوش مصنوعی برای helpdesk سازمانی

---

## فهرست مطالب

- [هدف پروژه](#هدف-پروژه)
- [وضعیت پیاده‌سازی نسبت به مشخصات](#وضعیت-پیادهسازی-نسبت-به-مشخصات)
- [معماری سیستم](#معماری-سیستم)
- [ساختار فایل‌ها و نگاشت به مشخصات](#ساختار-فایلها-و-نگاشت-به-مشخصات)
- [Pipeline بازیابی اطلاعات](#pipeline-بازیابی-اطلاعات)
- [راه‌اندازی و اجرا](#راهاندازی-و-اجرا)
- [API Endpoints](#api-endpoints)
- [متغیرهای محیطی](#متغیرهای-محیطی)
- [نتایج ارزیابی](#نتایج-ارزیابی)
- [نکات مهم پیاده‌سازی](#نکات-مهم-پیادهسازی)
- [موارد باقیمانده برای توسعه](#موارد-باقیمانده-برای-توسعه)

---

## هدف پروژه

> **مشخصات — بخش ۹.۱:**
> این بخش باید رابطه‌های پنهان بین تیکت‌ها و مقاله‌ها را پیدا کند. خروجی آن باعث می‌شود سیستم فقط تحلیل تک‌تیکت نداشته باشد، بلکه تشخیص بدهد چه تیکت‌هایی به هم مربوط‌اند و آیا یک رخداد عملیاتی در حال شکل گیری است یا نه.

این پروژه یک **AI Infrastructure Layer** برای سیستم‌های helpdesk سازمانی است که شامل موارد زیر می‌شود:

- جستجوی معنایی تیکت‌های مشابه با استفاده از embeddings
- بازیابی ترکیبی (Hybrid Retrieval) با ترکیب جستجوی معنایی و کلیدواژه
- رتبه‌بندی مجدد نتایج با Cross-Encoder
- بازیابی مقالات پایگاه دانش
- تشخیص رخداد (Incident Detection) با سطح‌بندی medium/high
- ارزیابی کیفیت بازیابی با متریک‌های استاندارد IR

---

## وضعیت پیاده‌سازی نسبت به مشخصات

### ۹.۳ — Embedding Pipeline

| مورد | وضعیت | فایل مرتبط |
|------|--------|------------|
| مدل یک‌بار در startup لود شود | ✅ پیاده‌سازی شده | `embedding_service.py` |
| ساخت متن استاندارد تیکت (title + description) | ✅ پیاده‌سازی شده | `startup.py` |
| ساخت embedding برای هر تیکت | ✅ پیاده‌سازی شده | `embedding_service.py` |
| ذخیره embedding در Qdrant | ✅ پیاده‌سازی شده | `qdrant_store.py` |
| ثبت نسخه مدل در metadata | ⚠️ در حال اجرا لاگ می‌شود | `embedding_service.py` |

### ۹.۴ — Similar Ticket Search

| مورد | وضعیت | فایل مرتبط |
|------|--------|------------|
| تابع find_similar_tickets | ✅ پیاده‌سازی شده | `infrastructure_service.py` |
| نتایج مرتب بر اساس score | ✅ پیاده‌سازی شده | `hybrid_retriever.py` |
| ذخیره similarity score در response | ✅ پیاده‌سازی شده | `score_fusion.py` |
| Threshold مشابهت قابل تنظیم | ✅ پیاده‌سازی شده | `thresholds.py` |
| فیلتر metadata (department, tenant) | ✅ پیاده‌سازی شده | `qdrant_store.py` |
| فیلتر تیکت‌های حذف‌شده/بسته | ⚠️ نیاز به فیلد `status` | `fake_tickets.py` |
| جلوگیری از self-match | ⚠️ نیاز به پیاده‌سازی | `hybrid_retriever.py` |

### ۹.۵ — Knowledge Base Retrieval

| مورد | وضعیت | فایل مرتبط |
|------|--------|------------|
| ساختار مقاله با id, title, content | ✅ پیاده‌سازی شده | `fake_articles.py` |
| حداقل ۱۰ مقاله seed | ✅ ۱۰ مقاله موجود است | `fake_articles.py` |
| ساخت embedding مقالات در startup | ✅ پیاده‌سازی شده | `startup.py` |
| تابع find_related_article | ✅ پیاده‌سازی شده | `knowledge_retriever.py` |
| اعمال حداقل score برای فیلتر مقالات بی‌ربط | ✅ پیاده‌سازی شده | `knowledge_retriever.py` |
| فیلد category و tags در مقالات | ⚠️ هنوز اضافه نشده | `fake_articles.py` |
| اتصال به Suggested Reply | 🔲 آینده | — |

### ۹.۶ — Incident Detection

| مورد | وضعیت | فایل مرتبط |
|------|--------|------------|
| تعریف قانون incident در config | ✅ پیاده‌سازی شده | `thresholds.py` |
| تشخیص incident سطح medium (2-3 تیکت) | ✅ پیاده‌سازی شده | `incident_detector.py` |
| تشخیص incident سطح high (4+ تیکت) | ✅ پیاده‌سازی شده | `incident_detector.py` |
| عنوان فارسی رخداد | ✅ پیاده‌سازی شده | `incident_detector.py` |
| دلیل فارسی رخداد | ✅ پیاده‌سازی شده | `incident_detector.py` |
| جلوگیری از incident تکراری (dedup) | ⚠️ نیاز به پیاده‌سازی | — |

### ۹.۷ — Qdrant (اختیاری)

| مورد | وضعیت | فایل مرتبط |
|------|--------|------------|
| راه‌اندازی Qdrant در Docker | ✅ پیاده‌سازی شده | `docker-compose.yml` |
| ساخت collection tickets | ✅ پیاده‌سازی شده | `qdrant_store.py` |
| ساخت collection knowledge_articles | ✅ پیاده‌سازی شده | `qdrant_store.py` |
| Upsert تیکت‌ها با payload کامل | ✅ پیاده‌سازی شده | `qdrant_store.py` |
| جستجو در Qdrant با فیلتر | ✅ پیاده‌سازی شده | `qdrant_store.py` |
| Fallback بدون Qdrant | ⚠️ نیاز به پیاده‌سازی | — |

### ۹.۸ — Evaluation و Threshold Tuning

| مورد | وضعیت | فایل مرتبط |
|------|--------|------------|
| محاسبه Precision@K | ✅ پیاده‌سازی شده | `metrics.py` |
| محاسبه Recall@K | ✅ پیاده‌سازی شده | `metrics.py` |
| محاسبه MRR | ✅ پیاده‌سازی شده | `metrics.py` |
| evaluation dataset | ✅ پیاده‌سازی شده | `evaluation_dataset.py` |
| حداقل ۵۰ تیکت فارسی در dataset | ⚠️ فعلاً ۸ query | `evaluation_dataset.py` |
| similarity pairs برای threshold tuning | ⚠️ نیاز به پیاده‌سازی | — |

---

## معماری سیستم

```
┌──────────────────────────────────────────────┐
│                  User Query                   │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│              FastAPI (main.py)                │
│   /tickets  /incidents  /knowledge  /eval     │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│           InfrastructureService               │
│         infrastructure_service.py             │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│            HybridRetriever                    │
│           hybrid_retriever.py                 │
├─────────────────────┬────────────────────────┤
│   QdrantRetriever   │   KeywordRetriever      │
│  (Semantic Search)  │   (Lexical Search)      │
└─────────────────────┴────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│              ScoreFusion                      │
│  semantic × 0.7  +  keyword × 0.3             │
│           score_fusion.py                     │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│          CrossEncoderReranker                 │
│       cross_encoder_reranker.py               │
│   ms-marco-MiniLM-L-6-v2                      │
└───────────────────────┬──────────────────────┘
                        │
              ┌─────────┴──────────┐
              ▼                    ▼
┌─────────────────────┐  ┌────────────────────┐
│  IncidentDetector   │  │   Final Results     │
│ incident_detector.py│  │  (tickets/similar)  │
│ medium / high       │  └────────────────────┘
└─────────────────────┘
```

---

## ساختار فایل‌ها و نگاشت به مشخصات

```
app/
│
├── main.py
│   └── [9.3] lifespan startup — لود مدل و index کردن داده‌ها
│
├── api/routes/
│   ├── tickets.py       [9.4] POST /tickets/similar
│   ├── incidents.py     [9.6] POST /incidents/detect
│   ├── knowledge.py     [9.5] GET /knowledge/search
│   └── evaluation.py    [9.8] GET /evaluation/retrieval
│
├── services/
│   ├── infrastructure_service.py   [9.4] get_similar_tickets()
│   ├── incident_service.py         [9.6] analyze_incident()
│   ├── knowledge_service.py        [9.5] search_articles()
│   └── evaluation_service.py       [9.8] evaluate()
│
├── infrastructure/
│   │
│   ├── data/
│   │   ├── fake_tickets.py     [9.4, 9.6] 15 تیکت با 5 cluster موضوعی
│   │   └── fake_articles.py    [9.5] 10 مقاله seed پایگاه دانش
│   │
│   ├── embeddings/
│   │   └── embedding_service.py    [9.3] singleton model — paraphrase-multilingual-MiniLM-L12-v2
│   │
│   ├── vector_db/
│   │   ├── qdrant_clientt.py        [9.7] اتصال به Qdrant
│   │   └── qdrant_store.py          [9.7] CRUD collections + metadata filter
│   │
│   ├── retrieval/
│   │   ├── hybrid/
│   │   │   └── hybrid_retriever.py  [9.4] ترکیب semantic + keyword
│   │   ├── qdrant/
│   │   │   ├── qdrant_retriever.py     [9.4, 9.7] semantic search
│   │   │   └── knowledge_retriever.py  [9.5] جستجو در مقالات
│   │   └── keyword/
│   │       └── keyword_retriever.py    [9.4] جستجوی کلیدواژه نرمالایز شده
│   │
│   ├── ranking/
│   │   └── score_fusion.py     [9.4] ترکیب score با وزن 70/30
│   │
│   ├── reranking/
│   │   └── cross_encoder_reranker.py   [9.4] رتبه‌بندی نهایی
│   │
│   ├── incidents/
│   │   └── incident_detector.py    [9.6] تشخیص medium/high + عنوان فارسی
│   │
│   ├── evaluation/
│   │   ├── metrics.py              [9.8] Precision@K, Recall@K, MRR
│   │   └── evaluation_dataset.py   [9.8] ground truth dataset
│   │
│   ├── thresholds.py   [9.4, 9.6, 9.8] همه تنظیمات از env variable
│   └── logger.py       لاگ‌گیری ساختاریافته
│
└── core/
    └── startup.py  [9.3, 9.7] index کردن تیکت‌ها و مقالات در Qdrant
```

---

## Pipeline بازیابی اطلاعات

### مرحله ۱ — Embedding Generation
> **مشخصات ۹.۳:** مدل MiniLM multilingual یک‌بار در startup لود شود

```
Query Text
    ↓
EmbeddingService.generate_embedding()       ← singleton, بار نمی‌کند مجدد
    ↓
384-dimensional dense vector
```

مدل: `paraphrase-multilingual-MiniLM-L12-v2` — پشتیبانی از فارسی و چندزبانه

---

### مرحله ۲ — Hybrid Retrieval
> **مشخصات ۹.۴:** ترکیب semantic و keyword برای نتایج بهتر

```
                    Query
                   /     \
    Semantic Search       Keyword Search
    (Qdrant vector)       (BM25-style, normalized 0-1)
         ↓                      ↓
    top-10 results         top-10 results
                   \     /
               ScoreFusion
          semantic×0.7 + keyword×0.3
                     ↓
              fused_results
```

**نکته:** `keyword_score` قبل از fusion به بازه 0-1 نرمالایز می‌شود تا با `semantic_score` سازگار باشد.

---

### مرحله ۳ — Cross-Encoder Reranking
> **مشخصات ۹.۴:** رتبه‌بندی نهایی برای دقت بیشتر

مدل `cross-encoder/ms-marco-MiniLM-L-6-v2` هر جفت (query, ticket) را جداگانه بررسی و امتیاز نهایی می‌دهد. بازه score: `-10` تا `+10`.

---

### مرحله ۴ — Incident Detection
> **مشخصات ۹.۶:** تشخیص رخداد با سطح‌بندی

| تعداد تیکت مشابه در ۳۰ دقیقه | سطح | خروجی |
|-------------------------------|-----|--------|
| ۲ یا ۳ | medium | عنوان و دلیل فارسی |
| ۴ یا بیشتر | high | عنوان و دلیل فارسی |
| کمتر از ۲ | — | incident_detected: false |

---

## راه‌اندازی و اجرا

### پیش‌نیازها

- Docker Desktop
- Docker Compose

### اجرا

```bash
git clone https://github.com/your-repo/servicedesk-radar.git
cd servicedesk-radar
docker compose up --build
```

سرویس‌ها:

| سرویس | آدرس |
|--------|------|
| FastAPI | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

### اجرای بدون Docker (توسعه محلی)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

pip install -r requirements.txt

# Qdrant باید جداگانه اجرا شود:
docker run -p 6333:6333 qdrant/qdrant

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## API Endpoints

### `POST /tickets/similar`
> **مشخصات ۹.۴:** یافتن تیکت‌های مشابه

**Request:**
```json
{
  "query": "VPN login failed MFA not working",
  "top_k": 5,
  "department": "IT",
  "tenant": "company_a"
}
```

**Response:**
```json
{
  "results": [
    {
      "item": {
        "id": 1,
        "title": "VPN login failed",
        "description": "...",
        "department": "IT",
        "priority": "high",
        "tenant": "company_a",
        "created_at": "2025-01-01T10:00:00"
      },
      "semantic_score": 0.92,
      "keyword_score": 1.0,
      "final_score": 0.944,
      "rerank_score": 8.3
    }
  ]
}
```

---

### `POST /incidents/detect`
> **مشخصات ۹.۶:** تشخیص رخداد احتمالی

**Request:**
```json
{
  "query": "VPN login failed"
}
```

**Response:**
```json
{
  "incident_detected": true,
  "severity": "high",
  "matched_count": 4,
  "fa_title": "رخداد احتمالی در سرویس VPN",
  "fa_reason": "تعداد 4 تیکت مشابه در 30 دقیقه اخیر شناسایی شد. سطح: high.",
  "matched_tickets": [...]
}
```

---

### `GET /knowledge/search?query=VPN issue&top_k=3`
> **مشخصات ۹.۵:** جستجو در پایگاه دانش

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "title": "VPN Troubleshooting Guide",
      "content": "If VPN login fails...",
      "semantic_score": 0.87
    }
  ]
}
```

فقط مقالاتی برگردانده می‌شوند که `semantic_score >= ARTICLE_MIN_SCORE` (پیش‌فرض: `0.5`)

---

### `GET /evaluation/retrieval`
> **مشخصات ۹.۸:** ارزیابی کیفیت بازیابی

**Response:**
```json
{
  "mean_precision@5": 0.64,
  "mean_recall@5": 0.91,
  "mean_mrr": 0.88,
  "queries": [
    {
      "query": "VPN MFA issue",
      "precision@5": 0.8,
      "recall@5": 1.0,
      "mrr": 1.0
    }
  ]
}
```

---

### `GET /health`

```json
{"status": "ok"}
```

---

## متغیرهای محیطی

> **مشخصات ۹.۴، ۹.۶، ۹.۸:** همه threshold‌ها در config قابل تغییر باشند

تمام تنظیمات از طریق environment variable قابل تغییر هستند و نیازی به تغییر کد نیست:

| متغیر | پیش‌فرض | توضیح |
|-------|---------|-------|
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | مدل embedding |
| `RERANKER_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | مدل reranking |
| `INCIDENT_TIME_WINDOW_MINUTES` | `30` | پنجره زمانی برای incident |
| `MIN_SIMILAR_TICKETS_MEDIUM` | `2` | حداقل تیکت برای incident medium |
| `MIN_SIMILAR_TICKETS_HIGH` | `4` | حداقل تیکت برای incident high |
| `MIN_RERANK_SCORE` | `0.5` | حداقل rerank score برای incident |
| `SIMILARITY_THRESHOLD_HIGH` | `0.85` | آستانه شباهت بالا |
| `SIMILARITY_THRESHOLD_MEDIUM` | `0.75` | آستانه شباهت متوسط |
| `ARTICLE_MIN_SCORE` | `0.5` | حداقل score برای نمایش مقاله |

---

## نتایج ارزیابی

> **مشخصات ۹.۸:** گزارش کیفیت برای README

ارزیابی روی ۸ query از ۵ دسته (VPN، Outlook، Printer، Network، Account):

| متریک | مقدار | توضیح |
|--------|-------|-------|
| `mean_precision@5` | ~0.64 | از هر ۵ نتیجه، ۳.۲ مورد مرتبط |
| `mean_recall@5` | ~0.91 | ۹۱٪ تیکت‌های مرتبط پیدا می‌شوند |
| `mean_mrr` | ~0.88 | اولین نتیجه مرتبط معمولاً در رتبه ۱ یا ۲ |

**نحوه محاسبه:**

```
Precision@K = تعداد hits در top-K / K
Recall@K    = تعداد hits در top-K / تعداد کل relevant
MRR         = 1 / رتبه اولین نتیجه مرتبط
```

---

## نکات مهم پیاده‌سازی

### Singleton Model Loading
> **مشخصات ۹.۳:** مدل در هر request دوباره load نشود

```python
class EmbeddingService:
    _model = None          # یک‌بار لود، همیشه در حافظه

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(EMBEDDING_MODEL)
        return cls._model
```

### Score Normalization در Keyword Retrieval
> جلوگیری از تسلط keyword score بر semantic score

```python
normalized_score = raw_match_count / len(query_words)  # همیشه 0-1
```

### Threshold‌های قابل تنظیم
> **مشخصات ۹.۴، ۹.۶:** threshold در config قابل تغییر باشد

```python
# thresholds.py — همه از env variable
INCIDENT_TIME_WINDOW_MINUTES = int(os.getenv("...", "30"))
MIN_RERANK_SCORE = float(os.getenv("...", "0.5"))
```

### Docker Cache برای مدل‌ها
```yaml
volumes:
  - huggingface_cache:/root/.cache/huggingface
```
مدل‌ها یک‌بار دانلود می‌شوند و در volume ذخیره می‌مانند.

---

## موارد باقیمانده برای توسعه

### اولویت بالا — مشخصات پیاده‌سازی نشده

**self-match prevention (مشخصات ۹.۴)**
تیکت با خودش match نشود. نیاز به اضافه کردن پارامتر `exclude_id` به `get_similar_tickets()`.

**incident dedup (مشخصات ۹.۶)**
اگر incident باز مشابه وجود دارد، همان آپدیت شود. نیاز به نگهداری state رخدادهای باز.

**Qdrant fallback (مشخصات ۹.۷)**
اگر Qdrant خاموش بود، جستجوی ساده Python کار کند.

### اولویت متوسط — بهبود کیفیت

**توسعه evaluation dataset (مشخصات ۹.۸)**
رساندن dataset از ۸ query به حداقل ۵۰ تیکت فارسی با دسته‌های VPN، ایمیل، شبکه، پرینتر، account.

**category و tags برای مقالات (مشخصات ۹.۵)**
اضافه کردن فیلدهای `category` و `tags` به `fake_articles.py` و `qdrant_store.py`.

### آینده — توسعه‌های جدید

**RAG — پاسخ هوشمند با LLM**
ترکیب knowledge retrieval با LLM برای تولید پاسخ پیشنهادی به اپراتور helpdesk.

**Redis Cache**
Cache کردن embedding‌های query‌های تکراری برای کاهش latency.

**RRF — Reciprocal Rank Fusion**
جایگزین weighted score fusion برای ترکیب بهتر نتایج بدون نیاز به تنظیم وزن.

**Multi-Tenant Security واقعی**
JWT authentication + middleware برای جداسازی داده tenant‌ها.

---

## Tech Stack

| لایه | ابزار |
|------|-------|
| API | FastAPI + Uvicorn |
| زبان | Python 3.10 |
| Embeddings | sentence-transformers |
| Vector DB | Qdrant |
| Reranking | CrossEncoder (sentence-transformers) |
| Container | Docker + Docker Compose |
| ارزیابی | Precision@K, Recall@K, MRR |

---

## License

MIT License
