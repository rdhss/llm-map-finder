from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import json
import aiohttp
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# konfigurasi origins
origins = [
    "http://localhost:3000",  # React/Next.js dev server
    "http://127.0.0.1:3000",
    "*"  # sementara semua origin diizinkan (bisa dibatesin nanti)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

def log(actor: str, message: str):
    print(f"[{datetime.now().isoformat()}] {actor}: {message}")

async def run_ollama(query: str) -> dict:
    log("User", query)
    log("AI", "Menerjemahkan query ke parameter OSM...")

    prompt = f"""
You are an assistant that converts a user's place query into a JSON object ready to be used as parameters for OpenStreetMap Nominatim API.

Rules:
1. Only output JSON. No extra text, no explanation.
2. Extract the full descriptive keywords for the place in "type_of_place" (do not generalize, include adjectives if relevant like "enak", "murah", "terdekat").
3. Extract the location details accurately in "location" (city, district, neighborhood if available).
4. Always produce valid JSON that can be parsed by standard JSON parsers.
5. The JSON must have these exact fields:
{{
  "q": "<type_of_place>, <location>",
  "format": "json",
  "limit": 10,
  "addressdetails": 1
}}

Examples:

User query: "restoran ramen enak di Jakarta Selatan"
Output:
{{
  "q": "restoran ramen enak, Jakarta Selatan",
  "format": "json",
  "limit": 10,
  "addressdetails": 1
}}

User query: "cafe kopi terdekat di Bandung"
Output:
{{
  "q": "cafe kopi terdekat, Bandung",
  "format": "json",
  "limit": 10,
  "addressdetails": 1
}}

Now convert this query:
"{query}"

"""

    # Jalankan Ollama sebagai subprocess async
    process = await asyncio.create_subprocess_exec(
        "ollama", "run", "llama3", prompt,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        log("AI", f"❌ Ollama error: {stderr.decode().strip()}")
        raise Exception(f"Ollama error: {stderr.decode().strip()}")

    output = stdout.decode().strip()
    log("AI", f"✅ JSON berhasil dibuat: {output}")

    try:
        data = json.loads(output)
        log("AI", f"🔹 Parsed JSON for OSM: {data}")
        return data
    except json.JSONDecodeError:
        log("AI", f"❌ Gagal parsing JSON: {output}")
        raise

async def fetch_osm(params: dict) -> list:
    url = "https://nominatim.openstreetmap.org/search"
    log("Server", f"Mengirim request ke OSM dengan params: {params}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="OSM request failed")
            data = await response.json()
            log("Server", f"✅ Response OSM diterima, mengirim ke user")
            return data

@app.post("/search")
async def search(req: QueryRequest):
    try:
        osm_params = await run_ollama(req.query)
        places = await fetch_osm(osm_params)
        return places
    except Exception as e:
        log("Server", f"❌ Terjadi error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
