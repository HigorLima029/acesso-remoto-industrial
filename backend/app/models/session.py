import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class SessionStatus(str, enum.Enum):
    solicitada = "solicitada"
    negada = "negada"
    ativa = "ativa"
    encerrada = "encerrada"
    falha = "falha"


class AccessSession(Base):
    """
    Registro de auditoria de cada sessão de acesso remoto:
    quem, qual máquina, quando começou/terminou e o resultado.
    Item obrigatório dos critérios de aceite do MVP.
    """

    __tablename__ = "access_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)

    status = Column(Enum(SessionStatus), default=SessionStatus.solicitada, nullable=False)
    iniciada_em = Column(DateTime, nullable=True)
    encerrada_em = Column(DateTime, nullable=True)
    ip_cliente_vpn = Column(String, nullable=True)  # IP atribuído ao técnico no túnel
    client_public_key = Column(String, nullable=True)  # chave pública WireGuard do técnico
    observacoes = Column(String, nullable=True)

    user = relationship("User", back_populates="sessoes")
    machine = relationship("Machine", back_populates="sessoes")
