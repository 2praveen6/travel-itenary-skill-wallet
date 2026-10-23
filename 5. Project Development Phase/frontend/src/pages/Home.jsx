import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Compass, Map, Sparkles } from "lucide-react";
import { useAuth } from "../api/auth.jsx";
import { templatesAPI } from "../api/tripsAPI";
import TemplateCard from "../components/TemplateCard.jsx";

export default function Home() {
  const { user } = useAuth();
  const [templates, setTemplates] = useState([]);

  useEffect(() => {
    templatesAPI.list().then(setTemplates).catch(() => setTemplates([]));
  }, []);

  return (
    <>
      <section className="hero">
        <div>
          <p className="kicker">Ready-made + AI trips</p>
          <h1>Pick a plan. Tweak the dates. Go.</h1>
          <p>
            Browse curated weekend, couple, and group itineraries — or answer a few
            questions and let AI fill the days with stays, food, and routes.
          </p>
          <div className="row">
            <Link className="btn" to="/explore">
              <Map size={16} /> Browse ready itineraries
            </Link>
            <Link className="btn ghost" to={user ? "/plan" : "/register"}>
              <Compass size={16} /> Build my own
            </Link>
          </div>
        </div>
        <motion.div className="hero-visual" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }}>
          <img
            src="https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80"
            alt="Traveler looking over a city"
          />
          <div className="hero-float">
            <Sparkles size={16} />
            Stays, meals, and metro hops already in the timeline
          </div>
        </motion.div>
      </section>

      <div className="section-head">
        <h2>Start from a finished plan</h2>
        <Link to="/explore">See all</Link>
      </div>
      <div className="photo-grid">
        {templates.slice(0, 6).map((item) => (
          <TemplateCard key={item.id} item={item} />
        ))}
      </div>
    </>
  );
}
