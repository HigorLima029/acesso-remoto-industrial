import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [erro, setErro] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setErro("");
    try {
      const { data } = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", data.access_token);
      navigate("/maquinas");
    } catch (err) {
      setErro(
        err?.response?.data?.detail || "Falha ao autenticar. Verifique suas credenciais."
      );
    }
  }

  return (
    <div style={styles.container}>
      <form onSubmit={handleSubmit} style={styles.card}>
        <h1 style={styles.title}>Acesso Remoto Industrial</h1>
        <p style={styles.subtitle}>Entre com suas credenciais de técnico</p>

        <label style={styles.label}>E-mail</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={styles.input}
        />

        <label style={styles.label}>Senha</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={styles.input}
        />

        {erro && <p style={styles.erro}>{erro}</p>}

        <button type="submit" style={styles.button}>
          Entrar
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#0f172a",
    fontFamily: "system-ui, sans-serif",
  },
  card: {
    background: "#1e293b",
    padding: "2.5rem",
    borderRadius: "12px",
    width: "320px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
  },
  title: { color: "#f1f5f9", fontSize: "1.3rem", marginBottom: "0.25rem" },
  subtitle: { color: "#94a3b8", fontSize: "0.85rem", marginBottom: "1.5rem" },
  label: { color: "#cbd5e1", fontSize: "0.8rem", display: "block", marginTop: "0.75rem" },
  input: {
    width: "100%",
    padding: "0.6rem",
    marginTop: "0.3rem",
    borderRadius: "6px",
    border: "1px solid #334155",
    background: "#0f172a",
    color: "#f1f5f9",
    boxSizing: "border-box",
  },
  button: {
    width: "100%",
    marginTop: "1.5rem",
    padding: "0.7rem",
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    fontWeight: 600,
    cursor: "pointer",
  },
  erro: { color: "#f87171", fontSize: "0.8rem", marginTop: "0.75rem" },
};
