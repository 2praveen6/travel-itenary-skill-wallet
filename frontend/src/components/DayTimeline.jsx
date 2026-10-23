import { Clock3, MapPin } from "lucide-react";

export default function DayTimeline({ days, onRegenerateDay, onRemoveActivity }) {
  return (days || []).map((day, index) => (
    <section className="day" key={day.id || day.day_number || index}>
      <div className="day-head">
        <div>
          <p className="kicker">Day {day.day_number}{day.date ? ` · ${day.date}` : ""}</p>
          <h2>{day.theme}</h2>
        </div>
        {onRegenerateDay ? (
          <button className="btn ghost" type="button" onClick={() => onRegenerateDay(day)}>
            Refresh day
          </button>
        ) : null}
      </div>
      <p className="muted">{day.summary}</p>
      <div className="timeline">
        {(day.activities || []).map((activity, idx) => (
          <article className={`activity cat-${activity.category || "other"}`} key={activity.id || idx}>
            <div className="slot">
              <Clock3 size={14} /> {activity.start_time || activity.time_slot}
              {activity.travel_minutes ? <small>{activity.travel_minutes} min hop</small> : null}
            </div>
            <div>
              <div className="activity-title">
                <strong>{activity.title}</strong>
                {activity.category ? <span className="pill">{activity.category}</span> : null}
              </div>
              <p>{activity.description}</p>
              {activity.location ? (
                <div className="muted"><MapPin size={12} /> {activity.location}</div>
              ) : null}
            </div>
            <div className="cost">
              {activity.estimated_cost ? `$${activity.estimated_cost}` : "free"}
              {onRemoveActivity ? (
                <button className="linkish" type="button" onClick={() => onRemoveActivity(activity)}>
                  Remove
                </button>
              ) : null}
            </div>
          </article>
        ))}
      </div>
    </section>
  ));
}
