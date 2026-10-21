import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Download, RefreshCw, Share2, Sparkles, Trash2 } from "lucide-react";
import { useAuth } from "../api/auth.jsx";
import { download } from "../api/client";
import { tripsAPI } from "../api/tripsAPI";
import DayTimeline from "../components/DayTimeline.jsx";

export default function TripDetail() {
  const { id } = useParams();
  const { token } = useAuth();
  const navigate = useNavigate();
  const [trip, setTrip] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [title, setTitle] = useState("");
  const [feedback, setFeedback] = useState("");
  const [shareUrl, setShareUrl] = useState("");
  const [newActivity, setNewActivity] = useState({ dayId: "", title: "", time_slot: "morning" });

  function load() {
    setLoading(true);
    tripsAPI
      .get(id, token)
      .then((data) => {
        setTrip(data);
        setTitle(data.title);
        if (data.days?.[0]) setNewActivity((a) => ({ ...a, dayId: data.days[0].id }));
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(load, [id, token]);

  async function exportFormat(format) {
    const body = await tripsAPI.export(id, format, token);
    const name = `${trip.destination}.${format === "markdown" ? "md" : format}`;
    const mime = format === "ics" ? "text/calendar" : format === "json" ? "application/json" : "text/markdown";
    const content = typeof body === "string" ? body : JSON.stringify(body, null, 2);
    download(name, content, mime);
  }

  const spent = (trip?.days || []).reduce(
    (sum, day) => sum + (day.activities || []).reduce((s, a) => s + Number(a.estimated_cost || 0), 0),
    0
  );

  if (loading) return <p>Loading itinerary…</p>;
  if (!trip) return <p>{error || "Trip not found"}</p>;

  return (
    <>
      <p className="kicker"><Link to="/app">My trips</Link> / {trip.destination}</p>
      <h1>{trip.title || trip.destination}</h1>
      <div className="stat-row">
        <span>{trip.start_date} → {trip.end_date}</span>
        <span>{trip.companions || "solo"} · {trip.travelers || 1}</span>
        <span>${spent}{trip.budget ? ` / ${trip.budget}` : ""}</span>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="toolbar">
        <input value={title} onChange={(e) => setTitle(e.target.value)} style={{ maxWidth: 240, margin: 0 }} />
        <button className="btn ghost" type="button" onClick={async () => setTrip(await tripsAPI.update(id, { title }, token))}>Rename</button>
        <button className="btn secondary" type="button" onClick={async () => setTrip(await tripsAPI.generate(id, token))}><RefreshCw size={16} /> AI regenerate</button>
        <button className="btn ghost" type="button" onClick={() => exportFormat("md")}><Download size={16} /> Markdown</button>
        <button className="btn ghost" type="button" onClick={() => exportFormat("ics")}>Calendar</button>
        <button className="btn ghost" type="button" onClick={async () => {
          const data = await tripsAPI.share(id, token);
          setShareUrl(data.url);
          await navigator.clipboard.writeText(data.url).catch(() => {});
        }}><Share2 size={16} /> Share</button>
        <button className="btn danger" type="button" onClick={async () => { await tripsAPI.remove(id, token); navigate("/app"); }}><Trash2 size={16} /> Delete</button>
      </div>
      {shareUrl && <p>Share link copied: {shareUrl}</p>}

      <DayTimeline
        days={trip.days}
        onRegenerateDay={async (day) => setTrip(await tripsAPI.refine(id, { feedback: "Refresh this day with a similar vibe.", day_number: day.day_number }, token))}
        onRemoveActivity={async (activity) => { await tripsAPI.removeActivity(id, activity.id, token); load(); }}
      />

      <form className="card" onSubmit={async (e) => {
        e.preventDefault();
        setTrip(await tripsAPI.refine(id, { feedback }, token));
        setFeedback("");
      }}>
        <h3><Sparkles size={18} /> Tweak with AI</h3>
        <p className="muted">Keep the structure, change the vibe.</p>
        <textarea rows="3" value={feedback} onChange={(e) => setFeedback(e.target.value)} placeholder="More food, slower mornings…" required />
        <button className="btn" type="submit">Update plan</button>
      </form>

      <form className="card" style={{ marginTop: 16 }} onSubmit={async (e) => {
        e.preventDefault();
        await tripsAPI.addActivity(id, newActivity.dayId, newActivity, token);
        setNewActivity((a) => ({ ...a, title: "" }));
        load();
      }}>
        <h3>Add a stop</h3>
        <div className="grid-2">
          <div>
            <label htmlFor="day">Day</label>
            <select id="day" value={newActivity.dayId} onChange={(e) => setNewActivity((a) => ({ ...a, dayId: e.target.value }))}>
              {(trip.days || []).map((day) => <option key={day.id} value={day.id}>Day {day.day_number}</option>)}
            </select>
          </div>
          <div>
            <label htmlFor="slot">When</label>
            <select id="slot" value={newActivity.time_slot} onChange={(e) => setNewActivity((a) => ({ ...a, time_slot: e.target.value }))}>
              <option value="morning">morning</option>
              <option value="afternoon">afternoon</option>
              <option value="evening">evening</option>
            </select>
          </div>
        </div>
        <label htmlFor="act">Title</label>
        <input id="act" value={newActivity.title} onChange={(e) => setNewActivity((a) => ({ ...a, title: e.target.value }))} required />
        <button className="btn" type="submit">Add</button>
      </form>
    </>
  );
}
