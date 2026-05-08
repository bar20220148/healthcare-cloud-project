import { useState } from "react";

const API = import.meta.env.VITE_API_BASE_URL;

export default function App() {
  const [username, setUsername] = useState("patient");
  const [password, setPassword] = useState("patient123");
  const [token, setToken] = useState("");
  const [role, setRole] = useState("");
  const [heartRate, setHeartRate] = useState(80);
  const [temperature, setTemperature] = useState(36.8);
  const [spo2, setSpo2] = useState(98);
  const [bloodPressure, setBloodPressure] = useState("120/80");
  const [result, setResult] = useState("");

  async function login() {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();
    if (data.access_token) {
      setToken(data.access_token);
      setRole(data.role);
      setResult("Login success");
    } else {
      setResult(JSON.stringify(data));
    }
  }

  async function submitReading() {
    const res = await fetch(`${API}/readings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        heart_rate: Number(heartRate),
        temperature: Number(temperature),
        spo2: Number(spo2),
        blood_pressure: bloodPressure,
      }),
    });
    const data = await res.json();
    setResult(JSON.stringify(data, null, 2));
  }

  async function getMyReadings() {
    const res = await fetch(`${API}/readings/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    setResult(JSON.stringify(data, null, 2));
  }

  async function getAllReadings() {
    const res = await fetch(`${API}/readings/all`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    setResult(JSON.stringify(data, null, 2));
  }

  async function getAlerts() {
    const res = await fetch(`${API}/alerts`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    setResult(JSON.stringify(data, null, 2));
  }

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Healthcare Monitoring App</h1>

      <h2>Login</h2>
      <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="username" />
      <br /><br />
      <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" />
      <br /><br />
      <button onClick={login}>Login</button>

      <h2>Submit Reading</h2>
      <input value={heartRate} onChange={(e) => setHeartRate(e.target.value)} placeholder="Heart Rate" />
      <br /><br />
      <input value={temperature} onChange={(e) => setTemperature(e.target.value)} placeholder="Temperature" />
      <br /><br />
      <input value={spo2} onChange={(e) => setSpo2(e.target.value)} placeholder="SpO2" />
      <br /><br />
      <input value={bloodPressure} onChange={(e) => setBloodPressure(e.target.value)} placeholder="Blood Pressure" />
      <br /><br />
      <button onClick={submitReading}>Submit Reading</button>
      <br /><br />
      <button onClick={getMyReadings}>My Readings</button>
      <br /><br />
      {role === "doctor" && <button onClick={getAllReadings}>All Readings</button>}
      <br /><br />
      {role === "doctor" && <button onClick={getAlerts}>Alerts</button>}

      <h2>Output</h2>
      <pre>{result}</pre>
    </div>
  );
}