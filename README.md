# Acesso Remoto a Máquinas Industriais — MVP

Prova de conceito (PoC) para acesso remoto seguro a máquinas industriais (CLP/PLC)
localizadas em campo, sem expor a rede da fábrica à Internet pública.

Baseado na especificação: `Projeto_Acesso_Remoto_a_Maquinas_Industriais.pdf`.

## Arquitetura

```
Usuário / Técnico → Cloud / API → VPN / Túnel Seguro (WireGuard) → Gateway Linux → CLP / PLC
```

## Stack

| Componente          | Tecnologia        |
|---------------------|--------------------|
| Frontend            | React (Vite)       |
| Backend             | Python / FastAPI   |
| Banco de Dados      | PostgreSQL         |
| Túnel Seguro        | WireGuard          |
| Gateway             | Linux (Edge Host)  |
| Comunicação Industrial | OPC-UA (a validar) |

## Estrutura do repositório

```
acesso-remoto-industrial/
├── backend/            # API FastAPI
│   ├── app/
│   │   ├── core/       # config, database, security, deps
│   │   ├── models/     # User, Machine, Gateway, MachinePermission, AccessSession
│   │   ├── routers/    # auth, machines/gateways, sessions
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/           # App React
│   └── src/
│       ├── pages/       # Login, MachineList
│       ├── components/  # RotaProtegida
│       └── services/    # api.js (axios)
├── docs/
│   └── wireguard-tunnel.md   # notas sobre a Etapa 3 (túnel VPN)
├── docker-compose.yml  # sobe PostgreSQL + backend
└── README.md
```

## Como rodar (ambiente local — Etapa 1 do roadmap)

### 1. Banco de dados + Backend via Docker

```bash
cd acesso-remoto-industrial
cp backend/.env.example backend/.env
# edite backend/.env se necessário (SECRET_KEY etc.)

docker compose up -d db
docker compose up backend
```

A API sobe em `http://localhost:8000`. Documentação automática (Swagger) em
`http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse `http://localhost:5173`.

### 3. Criando o primeiro usuário admin

Use o Swagger (`/docs`) ou `curl` para chamar `POST /auth/register` com
`role: "admin"`. Depois cadastre gateways (`POST /gateways/`) e máquinas
(`POST /machines/`) associando o `gateway_id`.

## Fluxo implementado no MVP

1. Login (`POST /auth/login`) — gera token JWT.
2. Listagem de máquinas com status do gateway (`GET /machines/`).
3. Solicitação de acesso (`POST /sessions/request`):
   - valida permissão do usuário para a máquina;
   - valida se o gateway está online;
   - registra a sessão para auditoria (`AccessSession`).
4. Encerramento de sessão (`POST /sessions/{id}/close`).
5. Histórico/auditoria (`GET /sessions/`).

## O que falta para o MVP completo (roadmap)

- **Etapa 2 — Gateway simulado**: script Linux que registra heartbeat
  (`POST /gateways/{id}/heartbeat`) periodicamente.
- **Etapa 3 — Infraestrutura VPN real**: provisionamento automático de peers
  WireGuard quando uma sessão é solicitada (hoje é um placeholder na API).
  Ver `docs/wireguard-tunnel.md`.
- **Etapa 4 — Teste de conectividade ponta a ponta** pela Internet.
- **Etapa 5 — Integração industrial (OPC-UA)**: pendente de especificação
  técnica do CLP real (ver seção 6 do documento original — pendências
  junto ao fornecedor, ex. Chen Hsong).
- **Configuração do Gateway Linux (VM)**: deixada propositalmente para o
  final. Quando você quiser, seguimos juntos passo a passo — desde criar a
  VM até instalar o WireGuard e o agente do gateway.

## Segurança

- Senhas armazenadas com hash bcrypt.
- Autenticação via JWT (expiração configurável).
- CLP nunca exposto diretamente à Internet — todo tráfego passa pelo túnel
  WireGuard, terminado no Gateway Linux.
- Toda sessão de acesso é registrada para auditoria (usuário, máquina,
  início, fim, resultado).
