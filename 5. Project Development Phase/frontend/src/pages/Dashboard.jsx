import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Compass, Map } from "lucide-react";
import { useAuth } from "../api/auth.jsx";
import { templatesAPI, tripsAPI } from "../api/tripsAPI";
import TemplateCard from "../components/TemplateCard.jsx";

export default function Dashboard() {
  const { token, user } = useAuth();
  const [trips, setTrips] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    tripsAPI.list(token).then(setTrips).catch((err) => setError(err.message));
    templatesAPI.list().then(setTemplates).catch(() => {});
  }, [token]);

  return (
    <>
      <p className="kicker">Hello {user?.name}</p>
      <div className="section-head">
        <h1><Map size={28} /> Your trips</h1>
        <Link className="btn" to="/plan"><Compass size={16} /> Custom trip</Link>
      </div>
      {error && <p className="error">{error}</p>}
      {!trips.length && (
        <div className="card">
          <h3>Nothing saved yet</h3>
          <p className="muted">Grab a ready-made weekend below — or answer four questions and generate one.</p>
        </div>
      )}
      <div className="trip-grid">
        {trips.map((trip) => (
          <Link className="card" key={trip.id} to={`/trips/${trip.id}`}>
            <p className="kicker">{trip.companions || trip.vibe || "trip"}</p>
            <h3>{trip.title}</h3>
            <p className="muted">
              {trip.destination}<br />
              {trip.start_date} → {trip.end_date}
            </p>
          </Link>
        ))}
      </div>
      <div className="section-head" style={{ marginTop: 36 }}>
        <h2>Ready-made plans</h2>
        <Link to="/explore">Browse all</Link>
      </div>
      <div className="photo-grid">
        {templates.slice(0, 3).map((item) => (
          <TemplateCard key={item.id} item={item} />
        ))}
      </div>
    </>
  );
}
