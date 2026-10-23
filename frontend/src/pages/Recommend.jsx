import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { MapPin, Sparkles, Utensils, Footprints } from "lucide-react";
import { useAuth } from "../api/auth.jsx";
import { prefsAPI } from "../api/tripsAPI";

export default function Recommend() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    prefsAPI.recommend({}, token).then(setResult).catch((err) => setError(err.message));
  }, [token]);

  return (
    <>
      <p className="kicker">AI recommendations · engine {result?.engine || "…"}</p>
      <h1><Sparkles size={28} /> Curated destinations</h1>
      <p>Filtered by your vibe, budget, and travel style — not a generic tourist list.</p>
      {error && <p className="error">{error}</p>}
      <div className="rec-grid">
        {(result?.items || []).map((item, index) => (
          <motion.div className="card" key={item.id} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.06 }}>
            <p className="kicker"><MapPin size={14} /> {item.country} {item.region ? `· ${item.region}` : ""}</p>
            <h3>{item.name}</h3>
            <p className="score">Score {item.score}</p>
            <p>{item.reason || item.summary}</p>
            <button className="btn" type="button" onClick={() => navigate(`/plan?destination=${encodeURIComponent(item.name)}&destination_id=${item.id}`)}>
              Build itinerary
            </button>
          </motion.div>
        ))}
      </div>
      {(result?.dining || []).length > 0 && (
        <>
          <h2><Utensils size={20} /> Dining matches</h2>
          <div className="rec-grid">
            {result.dining.map((item) => (
              <div className="card" key={item.id || item.name}><h3>{item.name}</h3><p>{item.reason}</p></div>
            ))}
          </div>
        </>
      )}
      {(result?.activities || []).length > 0 && (
        <>
          <h2><Footprints size={20} /> Activity matches</h2>
          <div className="rec-grid">
            {result.activities.map((item) => (
              <div className="card" key={item.id || item.name}><h3>{item.name}</h3><p>{item.reason}</p></div>
            ))}
          </div>
        </>
      )}
      <p><Link to="/preferences">Adjust preferences</Link></p>
    </>
  );
}
