import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../api/auth.jsx";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await register(name, email, password);
      navigate("/preferences");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="card auth-card">
      <p className="kicker">Start planning</p>
      <h2>Create an account</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={onSubmit}>
        <label htmlFor="name">Name</label>
        <input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        <label htmlFor="email">Email</label>
        <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label htmlFor="password">Password</label>
        <input id="password" type="password" minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button className="btn" type="submit">Create account</button>
      </form>
      <p>Already registered? <Link to="/login">Log in</Link></p>
    </div>
  );
}
