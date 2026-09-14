from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Machine(Base):
    """
    Representa a máquina industrial (ex: injetora Chen Hsong) e seu CLP.
    O protocolo de comunicação industrial (OPC-UA / Modbus / etc.) é
    tratado como 'a validar', conforme pendências do documento de projeto.
    """

    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)  # ex: CH-001
    nome = Column(String, nullable=False)
    local = Column(String, nullable=True)  # ex: Amazonas
    fabricante_clp = Column(String, nullable=True)
    protocolo_industrial = Column(String, nullable=True)  # ex: "OPC-UA (a validar)"

    gateway_id = Column(Integer, ForeignKey("gateways.id"), unique=True, nullable=True)
    gateway = relationship("Gateway", back_populates="maquina")

    permissoes = relationship("MachinePermission", back_populates="machine")
    sessoes = relationship("AccessSession", back_populates="machine")
