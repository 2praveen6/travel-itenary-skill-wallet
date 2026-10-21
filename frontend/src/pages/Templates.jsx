import { useEffect, useMemo, useState } from "react";
import { templatesAPI } from "../api/tripsAPI";
import TemplateCard from "../components/TemplateCard.jsx";

const FILTERS = [
  { id: "all", label: "All" },
  { id: "solo", label: "Solo weekend" },
  { id: "couple", label: "Couple" },
  { id: "friends", label: "Friends group" },
];

export default function Templates() {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState("all");
  const [error, setError] = useState("");

  useEffect(() => {
    templatesAPI.list().then(setItems).catch((err) => setError(err.message));
  }, []);

  const shown = useMemo(
    () => (filter === "all" ? items : items.filter((item) => item.companions === filter)),
    [items, filter]
  );

  return (
    <>
      <p className="kicker">Ready-made itineraries</p>
      <h1>Choose a trip, then save it to your dates</h1>
      <p className="lead">No blank form. Open a plan, skim the days, and clone it in one tap.</p>
      {error && <p className="error">{error}</p>}
      <div className="chips">
        {FILTERS.map((item) => (
          <button
            type="button"
            key={item.id}
            className={filter === item.id ? "chip on" : "chip"}
            onClick={() => setFilter(item.id)}
          >
            {item.label}
          </button>
        ))}
      </div>
      <div className="photo-grid">
        {shown.map((item) => (
          <TemplateCard key={item.id} item={item} />
        ))}
      </div>
    </>
  );
}
