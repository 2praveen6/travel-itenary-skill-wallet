import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Share2 } from "lucide-react";
import { tripsAPI } from "../api/tripsAPI";
import DayTimeline from "../components/DayTimeline.jsx";

export default function ShareView() {
  const { token } = useParams();
  const [trip, setTrip] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    tripsAPI.getShared(token).then(setTrip).catch((err) => setError(err.message));
  }, [token]);

  if (!trip) return <p>{error || "Loading shared itinerary…"}</p>;

  return (
    <>
      <p className="kicker"><Share2 size={14} /> Shared plan</p>
      <h1>{trip.destination}</h1>
      <p>{trip.start_date} → {trip.end_date} · {trip.vibe || "mixed"}</p>
      <DayTimeline days={trip.days} />
    </>
  );
}
