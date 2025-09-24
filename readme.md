# 📌 AI Location Search

Aplikasi pencarian lokasi menggunakan **FastAPI (Backend)** + **React/Next.js (Frontend)** + **Ollama (LLaMA 3)** + **OpenStreetMap (Nominatim API)**.  
User cukup masukkan query (contoh: *"cafe kopi enak di Bandung"*) → AI konversi query ke parameter OSM → hasil ditampilkan di grid + embedded map.

---

## ⚡ Install Ollama

### 🔹 Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 🔹 Windows

Download installer dari https://ollama.com/download


## Setup

1. Clone Repo
```bash
git clone https://github.com/rdhss/llm-map-finder.git
```

## Jalankan Backend

Masuk folder backend :
```bash
cd llm-map-finder/backend
```

Buat virtual environment & install dependencies:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

Jalankan server FastAPI:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Jalankan Frontend

Masuk folder backend :
```bash
cd llm-map-finder/frontend
```

Install dependencies:
```bash
npm install
```

Jalankan development server:
```bash
npm run dev
```

