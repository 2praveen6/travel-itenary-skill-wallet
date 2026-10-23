import { Link } from "react-router-dom";
import { Clock3, Users } from "lucide-react";

export default function TemplateCard({ item }) {
  return (
    <Link className="photo-card" to={`/explore/${item.id}`}>
      <div className="photo-card-media" style={{ backgroundImage: `url(${item.image})` }}>
        <span className="badge">{item.companions}</span>
      </div>
      <div className="photo-card-body">
        <p className="kicker">{item.destination}</p>
        <h3>{item.title}</h3>
        <p>{item.blurb}</p>
        <div className="meta-row">
          <span><Clock3 size={14} /> {item.day_count || item.nights} days</span>
          <span><Users size={14} /> {item.travelers}</span>
          <span>from ${item.budget}</span>
        </div>
      </div>
    </Link>
  );
}
