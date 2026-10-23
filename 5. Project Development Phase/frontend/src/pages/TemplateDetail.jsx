import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { CalendarRange, MapPin } from "lucide-react";
import { useAuth } from "../api/auth.jsx";
import { templatesAPI } from "../api/tripsAPI";
import DayTimeline from "../components/DayTimeline.jsx";

function ymd(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function defaultStart() {
  const d = new Date();
  const add = (6 - d.getDay() + 7) % 7 || 7;
  d.setDate(d.getDate() + add);
  return ymd(d);
}

export default function TemplateDetail() {
  const { id } = useParams();
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const [item, setItem] = useState(null);
  const [start, setStart] = useState(defaultStart);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    templatesAPI.get(id).then(setItem).catch((err) => setError(err.message));
  }, [id]);

  async function save() {
    if (!user) {
      navigate("/login");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const trip = await templatesAPI.clone(id, { start_date: start }, token);
      navigate(`/trips/${trip.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  if (!item && !error) return <p>Loading plan…</p>;
  if (!item) return <p className="error">{error}</p>;

  return (
    <>
      <p className="kicker"><Link to="/explore">Ready itineraries</Link> / {item.destination}</p>
      <header className="cover" style={{ backgroundImage: `url(${item.image})` }}>
        <div>
          <span className="badge">{item.companions}</span>
          <h1>{item.title}</h1>
          <p>{item.blurb}</p>
        </div>
      </header>
      <div className="stat-row">
        <span><MapPin size={16} /> {item.destination}</span>
        <span>{item.days?.length} days</span>
        <span>{item.travelers} traveler(s)</span>
        <span>about ${item.budget}</span>
        <span>{item.pace} pace</span>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="save-bar card">
        <label htmlFor="start"><CalendarRange size={14} /> Start date</label>
        <input id="start" type="date" value={start} onChange={(e) => setStart(e.target.value)} />
        <button className="btn" type="button" disabled={busy} onClick={save}>
          {busy ? "Saving…" : user ? "Save to my trips" : "Log in to save"}
        </button>
        <Link className="btn ghost" to={`/plan?destination=${encodeURIComponent(item.destination)}&destination_id=${item.destination_id || ""}`}>
          Customize with AI
        </Link>
      </div>
      <div className="chips">
        {(item.highlights || []).map((bit) => (
          <span className="chip on" key={bit}>{bit}</span>
        ))}
      </div>
      <DayTimeline days={item.days} />
    </>
  );
}
