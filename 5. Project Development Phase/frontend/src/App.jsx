import { Compass, LogOut } from "lucide-react";
import { Link, NavLink, Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./api/auth.jsx";
import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Preferences from "./pages/Preferences.jsx";
import Recommend from "./pages/Recommend.jsx";
import TripBuilder from "./pages/TripBuilder.jsx";
import TripDetail from "./pages/TripDetail.jsx";
import ShareView from "./pages/ShareView.jsx";
import Templates from "./pages/Templates.jsx";
import TemplateDetail from "./pages/TemplateDetail.jsx";

function Private({ children }) {
  const { token, ready } = useAuth();
  if (!ready) return <div className="shell">Loading…</div>;
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

function Nav() {
  const { user, logout } = useAuth();
  return (
    <nav className="nav">
      <Link to="/" className="brand">
        Way<span>point</span>
      </Link>
      <div className="nav-links">
        <NavLink to="/explore">Explore</NavLink>
        {user ? (
          <>
            <NavLink to="/app">My trips</NavLink>
            <NavLink to="/recommend">Ideas</NavLink>
            <NavLink to="/plan"><Compass size={16} /> Custom</NavLink>
            <button className="btn ghost" type="button" onClick={logout}>
              <LogOut size={16} /> Log out
            </button>
          </>
        ) : (
          <>
            <NavLink to="/login">Log in</NavLink>
            <Link className="btn" to="/register">Get started</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <div className="shell">
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/explore" element={<Templates />} />
        <Route path="/explore/:id" element={<TemplateDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/app" element={<Private><Dashboard /></Private>} />
        <Route path="/preferences" element={<Private><Preferences /></Private>} />
        <Route path="/recommend" element={<Private><Recommend /></Private>} />
        <Route path="/plan" element={<Private><TripBuilder /></Private>} />
        <Route path="/trips/:id" element={<Private><TripDetail /></Private>} />
        <Route path="/share/:token" element={<ShareView />} />
      </Routes>
      <footer className="site">Waypoint · pick a ready itinerary or generate your own</footer>
    </div>
  );
}
