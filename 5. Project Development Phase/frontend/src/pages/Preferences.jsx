import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../api/auth.jsx";
import { api } from "../api/client";

const VIBES = ["culture", "adventure", "relaxation", "food", "romance", "family", "luxury", "nature"];

export default function Preferences() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    vibe: "culture",
    climate: "mild",
    companions: "solo",
    pace: "moderate",
    travelers: 1,
    budget_min: 400,
    budget_max: 1800,
    currency: "USD",
    interests: "museums, food",
    dietary: "",
    mobility: "",
    season: "",
  });
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api("/api/preferences", { token })
      .then((data) => {
        if (!data) return;
        setForm((f) => ({
          ...f,
          ...data,
          interests: Array.isArray(data.interests) ? data.interests.join(", ") : data.interests || f.interests,
        }));
      })
      .catch((err) => setError(err.message));
  }, [token]);

  function set(key, value) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await api("/api/preferences", {
        method: "PUT",
        token,
        body: {
          ...form,
          budget_min: Number(form.budget_min) || null,
          budget_max: Number(form.budget_max) || null,
          interests: String(form.interests)
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
        },
      });
      setSaved(true);
      navigate("/recommend");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="card">
      <p className="kicker">Milestone 3.1</p>
      <h1>Traveler preferences</h1>
      <p>These drive destination ranking and vibe-based itineraries.</p>
      {error && <p className="error">{error}</p>}
      {saved && <p>Saved.</p>}
      <form onSubmit={onSubmit}>
        <div className="grid-2">
          <div>
            <label htmlFor="vibe">Vibe</label>
            <select id="vibe" value={form.vibe} onChange={(e) => set("vibe", e.target.value)}>
              {VIBES.map((v) => <option key={v} value={v}>{v}</option>)}
            </select>
          </div>
          <div>
            <label htmlFor="climate">Climate</label>
            <select id="climate" value={form.climate} onChange={(e) => set("climate", e.target.value)}>
              <option value="tropical">tropical</option>
              <option value="warm">warm</option>
              <option value="mild">mild</option>
              <option value="cool">cool</option>
              <option value="cold">cold</option>
              <option value="hot">hot</option>
            </select>
          </div>
          <div>
            <label htmlFor="companions">Companions</label>
            <select id="companions" value={form.companions} onChange={(e) => set("companions", e.target.value)}>
              <option value="solo">solo</option>
              <option value="couple">couple</option>
              <option value="friends">friends</option>
              <option value="family">family</option>
            </select>
          </div>
          <div>
            <label htmlFor="pace">Pace</label>
            <select id="pace" value={form.pace} onChange={(e) => set("pace", e.target.value)}>
          <option value="relaxed">relaxed</option>
          <option value="moderate">moderate</option>
          <option value="fast">fast</option>
        </select>
          </div>
          <div>
            <label htmlFor="min">Budget min</label>
            <input id="min" type="number" value={form.budget_min} onChange={(e) => set("budget_min", e.target.value)} />
          </div>
          <div>
            <label htmlFor="max">Budget max</label>
            <input id="max" type="number" value={form.budget_max} onChange={(e) => set("budget_max", e.target.value)} />
          </div>
        </div>
        <label htmlFor="interests">Interests (comma-separated)</label>
        <input id="interests" value={form.interests} onChange={(e) => set("interests", e.target.value)} />
        <label htmlFor="travelers">Travelers</label>
        <input id="travelers" type="number" min="1" value={form.travelers} onChange={(e) => set("travelers", Number(e.target.value))} />
        <label htmlFor="dietary">Dietary</label>
        <input id="dietary" value={form.dietary} onChange={(e) => set("dietary", e.target.value)} />
        <label htmlFor="mobility">Mobility notes</label>
        <input id="mobility" value={form.mobility} onChange={(e) => set("mobility", e.target.value)} />
        <label htmlFor="season">Preferred season</label>
        <input id="season" value={form.season} onChange={(e) => set("season", e.target.value)} />
        <button className="btn" type="submit">Save and recommend destinations</button>
      </form>
    </div>
  );
}
