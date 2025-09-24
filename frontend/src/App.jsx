import { useState } from "react";

export default function LocationSearch() {
  const [query, setQuery] = useState("");
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setPlaces(data);
    } catch (err) {
      console.error(err);
      setPlaces([]);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black/80 p-6">
      {/* 🔹 Search bar di tengah */}
      <div className="flex justify-center mb-8">
        <form onSubmit={handleSubmit} className="flex w-full max-w-xl">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Cari tempat..."
            className="flex-1 rounded-l-xl border p-3 focus:outline-none  text-white"
          />
          <button
            type="submit"
            className="rounded-r-xl bg-white px-5 text-black hover:bg-white/75 cursor-pointer"
          >
            Search
          </button>
        </form>
      </div>

      {loading && <p className="text-center text-white">Loading...</p>}

      {/* 🔹 Grid hasil 3 kolom */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {places.map((p) => (
          <div
            key={p.place_id}
            className="rounded-2xl bg-white p-4 shadow hover:shadow-lg transition"
          >
            <h2 className="text-lg font-semibold mb-2">{p.name || "(No name)"}</h2>
            <p className="text-sm text-gray-600 mb-3">📍 {p.display_name}</p>
            <a
              href={`https://www.openstreetmap.org/${p.osm_type}/${p.osm_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline text-sm"
            >
              View on OpenStreetMap
            </a>

            <div className="mt-3 overflow-hidden rounded-lg">
              <iframe
                width="100%"
                height="200"
                frameBorder="0"
                scrolling="no"
                src={`https://www.openstreetmap.org/export/embed.html?bbox=${p.boundingbox[2]},${p.boundingbox[0]},${p.boundingbox[3]},${p.boundingbox[1]}&layer=mapnik&marker=${p.lat},${p.lon}`}
              ></iframe>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
