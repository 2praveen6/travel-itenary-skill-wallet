import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import {
  ArrowLeft,
  ArrowRight,
  CalendarRange,
  CircleDollarSign,
  Heart,
  MapPin,
  Sparkles,
  Users,
  Utensils,
} from "lucide-react";
import { useAuth } from "../api/auth.jsx";
import { prefsAPI, templatesAPI, tripsAPI } from "../api/tripsAPI";

const STEPS = [
  { id: 1, title: "Where & when", icon: MapPin },
  { id: 2, title: "Group & budget", icon: Users },
  { id: 3, title: "Style & needs", icon: Heart },
  { id: 4, title: "Review", icon: Sparkles },
];

const empty = {
  destination: "",
  destination_id: "",
  start_date: "",
  end_date: "",
  travelers: 1,
  companions: "solo",
  budget: 1200,
  travel_style: "culture",
  interests: ["food", "museums"],
  dietary: "",
  mobility: "",
  pace: "moderate",
  notes: "",
  title: "",
};

const INTERESTS = ["museums", "food", "nature", "nightlife", "shopping", "beaches", "history", "adventure"];

export default function TripBuilder() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    ...empty,
    destination: params.get("destination") || "",
    destination_id: params.get("destination_id") || "",
  });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [readyPlans, setReadyPlans] = useState([]);

  useEffect(() => {
    templatesAPI.list().then(setReadyPlans).catch(() => {});
    prefsAPI
      .get(token)
      .then((prefs) => {
        if (!prefs) return;
        setForm((f) => ({
          ...f,
          travel_style: prefs.vibe || f.travel_style,
          pace: prefs.pace === "slow" ? "relaxed" : prefs.pace === "packed" ? "fast" : prefs.pace || f.pace,
          dietary: prefs.dietary || "",
          mobility: prefs.mobility || "",
          travelers: prefs.travelers || f.travelers,
          budget: prefs.budget_max || f.budget,
          interests: prefs.interests?.length ? prefs.interests : f.interests,
        }));
      })
      .catch(() => {});
  }, [token]);

  function set(key, value) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  function toggleInterest(value) {
    setForm((f) => ({
      ...f,
      interests: f.interests.includes(value) ? f.interests.filter((i) => i !== value) : [...f.interests, value],
    }));
  }

  function validate(current) {
    if (current === 1 && (!form.destination || !form.start_date || !form.end_date)) {
      return "Destination and both dates are required.";
    }
    if (current === 1 && form.end_date < form.start_date) return "End date must be after the start date.";
    if (current === 2 && form.travelers < 1) return "Add at least one traveler.";
    return "";
  }

  function next() {
    const message = validate(step);
    if (message) {
      setError(message);
      return;
    }
    setError("");
    setStep((s) => Math.min(4, s + 1));
  }

  async function submit() {
    const message = validate(1);
    if (message) {
      setError(message);
      setStep(1);
      return;
    }
    setBusy(true);
    setError("");
    try {
      const trip = await tripsAPI.create(
        {
          ...form,
          travelers: Number(form.travelers),
          budget: Number(form.budget) || null,
          vibe: form.travel_style,
        },
        token
      );
      navigate(`/trips/${trip.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  const Icon = STEPS[step - 1].icon;

  return (
    <div className="card builder">
      <p className="kicker">Guided trip builder</p>
      <h1>Collect the details that shape your plan</h1>
      <ol className="stepper">
        {STEPS.map((item) => (
          <li key={item.id} className={item.id === step ? "active" : item.id < step ? "done" : ""}>
            <item.icon size={16} /> {item.title}
          </li>
        ))}
      </ol>
      {error && <p className="error">{error}</p>}
      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          initial={{ opacity: 0, x: 24 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -24 }}
          transition={{ duration: 0.22 }}
        >
          <h2 className="row" style={{ alignItems: "center", gap: 8 }}>
            <Icon size={22} /> {STEPS[step - 1].title}
          </h2>

          {step === 1 && (
            <div className="grid-2">
              {readyPlans.length > 0 && (
                <div style={{ gridColumn: "1 / -1" }}>
                  <p className="muted">Or jump to a ready city</p>
                  <div className="chips">
                    {readyPlans.map((plan) => (
                      <button
                        type="button"
                        key={plan.id}
                        className={form.destination === plan.destination ? "chip on" : "chip"}
                        onClick={() => setForm((f) => ({
                          ...f,
                          destination: plan.destination,
                          destination_id: plan.destination_id || "",
                          companions: plan.companions,
                          travelers: plan.travelers,
                          travel_style: plan.travel_style,
                          budget: plan.budget,
                          title: plan.title,
                        }))}
                      >
                        {plan.destination}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              <div>
                <label htmlFor="destination">Destination</label>
                <input id="destination" value={form.destination} onChange={(e) => set("destination", e.target.value)} placeholder="Paris, Goa, Kyoto…" />
              </div>
              <div>
                <label htmlFor="title">Trip title</label>
                <input id="title" value={form.title} onChange={(e) => set("title", e.target.value)} placeholder="Optional" />
              </div>
              <div>
                <label htmlFor="start"><CalendarRange size={14} /> Start date</label>
                <input id="start" type="date" value={form.start_date} onChange={(e) => set("start_date", e.target.value)} />
              </div>
              <div>
                <label htmlFor="end">End date</label>
                <input id="end" type="date" value={form.end_date} onChange={(e) => set("end_date", e.target.value)} />
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="grid-2">
              <div>
                <label htmlFor="companions">Who is traveling</label>
                <select
                  id="companions"
                  value={form.companions}
                  onChange={(e) => {
                    const companions = e.target.value;
                    const size = companions === "solo" ? 1 : companions === "couple" ? 2 : Math.max(3, Number(form.travelers) || 3);
                    setForm((f) => ({ ...f, companions, travelers: size }));
                  }}
                >
                  <option value="solo">solo weekend</option>
                  <option value="couple">couple</option>
                  <option value="friends">small group / friends</option>
                  <option value="family">family</option>
                </select>
              </div>
              <div>
                <label htmlFor="travelers"><Users size={14} /> Travelers</label>
                <input id="travelers" type="number" min="1" max="20" value={form.travelers} onChange={(e) => set("travelers", e.target.value)} />
              </div>
              <div>
                <label htmlFor="budget"><CircleDollarSign size={14} /> Budget</label>
                <input id="budget" type="number" min="0" value={form.budget} onChange={(e) => set("budget", e.target.value)} />
              </div>
              <div>
                <label htmlFor="style">Travel style</label>
                <select id="style" value={form.travel_style} onChange={(e) => set("travel_style", e.target.value)}>
                  {["culture", "adventure", "relaxation", "food", "romance", "family", "luxury", "nature"].map((v) => (
                    <option key={v} value={v}>{v}</option>
                  ))}
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
            </div>
          )}

          {step === 3 && (
            <>
              <p>Interests</p>
              <div className="chips">
                {INTERESTS.map((item) => (
                  <button type="button" key={item} className={form.interests.includes(item) ? "chip on" : "chip"} onClick={() => toggleInterest(item)}>
                    {item}
                  </button>
                ))}
              </div>
              <label htmlFor="dietary"><Utensils size={14} /> Dietary needs</label>
              <input id="dietary" value={form.dietary} onChange={(e) => set("dietary", e.target.value)} placeholder="vegetarian, halal, gluten-free…" />
              <label htmlFor="mobility">Mobility notes</label>
              <input id="mobility" value={form.mobility} onChange={(e) => set("mobility", e.target.value)} placeholder="avoid long walks, stroller-friendly…" />
              <label htmlFor="notes">Notes</label>
              <textarea id="notes" rows="3" value={form.notes} onChange={(e) => set("notes", e.target.value)} />
            </>
          )}

          {step === 4 && (
            <ul className="review">
              <li><strong>Destination</strong> {form.destination}</li>
              <li><strong>Dates</strong> {form.start_date} → {form.end_date}</li>
              <li><strong>Travelers</strong> {form.companions} · {form.travelers} people · budget {form.budget}</li>
              <li><strong>Style / pace</strong> {form.travel_style} / {form.pace}</li>
              <li><strong>Interests</strong> {form.interests.join(", ") || "—"}</li>
              <li><strong>Dietary</strong> {form.dietary || "none"}</li>
              <li><strong>Mobility</strong> {form.mobility || "none"}</li>
            </ul>
          )}
        </motion.div>
      </AnimatePresence>

      <div className="row" style={{ marginTop: 18 }}>
        {step > 1 && (
          <button className="btn ghost" type="button" onClick={() => setStep((s) => s - 1)}>
            <ArrowLeft size={16} /> Back
          </button>
        )}
        {step < 4 ? (
          <button className="btn" type="button" onClick={next}>
            Next <ArrowRight size={16} />
          </button>
        ) : (
          <button className="btn" type="button" disabled={busy} onClick={submit}>
            {busy ? "Generating itinerary…" : "Create trip & generate"}
          </button>
        )}
      </div>
    </div>
  );
}
