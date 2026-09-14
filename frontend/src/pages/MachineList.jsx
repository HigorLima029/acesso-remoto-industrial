import { useEffect, useState } from "react";
import api from "../services/api";

export default function MachineList() {
  const [maquinas, setMaquinas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    carregarMaquinas();
  }, []);

  async function carregarMaquinas() {
    setCarregando(true);
    try {
      const { data } = await api.get("/machines/");
      setMaquinas(data);
    } catch (err) {
      setMensagem("Erro ao carregar máquinas. Faça login novamente.");
    } finally {
      setCarregando(false);
    }
  }

  async function solicitarAcesso(machineId) {
    setMensagem("");
    try {
      await api.post("/sessions/request", { machine_id: machineId });
      setMensagem("Sessão iniciada com sucesso! Túnel VPN estabelecido com o gateway.");
    } catch (err) {
      setMensagem(err?.response?.data?.detail || "Não foi possível iniciar a sessão.");
    }
  }

  if (carregando) return <p style={styles.info}>Carregando máquinas...</p>;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Máquinas Disponíveis</h1>
      {mensagem && <p style={styles.mensagem}>{mensagem}</p>}

      <div style={styles.grid}>
        {maquinas.map((m) => {
          const online = m.gateway?.status === "online";
          return (
            <div key={m.id} style={styles.card}>
              <div style={styles.cardHeader}>
                <strong>{m.codigo}</strong>
                <span style={online ? styles.badgeOnline : styles.badgeOffline}>
                  {online ? "Online" : "Offline"}
                </span>
              </div>
              <p style={styles.nome}>{m.nome}</p>
              <p style={styles.local}>Local: {m.local || "não informado"}</p>
              <p style={styles.protocolo}>Protocolo: {m.protocolo_industrial}</p>
              <button
                style={online ? styles.button : styles.buttonDisabled}
                disabled={!online}
                onClick={() => solicitarAcesso(m.id)}
              >
                Solicitar Acesso Remoto
              </button>
            </div>
          );
        })}
        {maquinas.length === 0 && <p>Nenhuma máquina cadastrada ainda.</p>}
      </div>
    </div>
  );
}

const styles = {
  container: { fontFamily: "system-ui, sans-serif", padding: "2rem", background: "#0f172a", minHeight: "100vh" },
  title: { color: "#f1f5f9", marginBottom: "1rem" },
  info: { color: "#f1f5f9", padding: "2rem" },
  mensagem: { color: "#93c5fd", marginBottom: "1rem" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: "1rem" },
  card: { background: "#1e293b", borderRadius: "10px", padding: "1.2rem", color: "#e2e8f0" },
  cardHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" },
  badgeOnline: { background: "#16a34a", color: "#fff", padding: "0.15rem 0.5rem", borderRadius: "999px", fontSize: "0.7rem" },
  badgeOffline: { background: "#64748b", color: "#fff", padding: "0.15rem 0.5rem", borderRadius: "999px", fontSize: "0.7rem" },
  nome: { margin: "0.3rem 0", fontSize: "0.95rem" },
  local: { fontSize: "0.8rem", color: "#94a3b8" },
  protocolo: { fontSize: "0.8rem", color: "#94a3b8", marginBottom: "0.8rem" },
  button: { width: "100%", padding: "0.5rem", background: "#2563eb", color: "#fff", border: "none", borderRadius: "6px", cursor: "pointer" },
  buttonDisabled: { width: "100%", padding: "0.5rem", background: "#334155", color: "#94a3b8", border: "none", borderRadius: "6px", cursor: "not-allowed" },
};
