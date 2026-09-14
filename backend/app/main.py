from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth, machines, sessions
import app.models  # noqa: F401  garante que os modelos sejam registrados no Base

app = FastAPI(
    title="Acesso Remoto a Máquinas Industriais - API",
    description="Backend do MVP de acesso remoto seguro a CLPs/PLCs via gateway Linux + WireGuard.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringir em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas automaticamente no MVP (em produção, usar Alembic migrations)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(machines.router)
app.include_router(machines.gateway_router)
app.include_router(sessions.router)


@app.get("/health", tags=["infra"])
def health_check():
    return {"status": "ok"}
