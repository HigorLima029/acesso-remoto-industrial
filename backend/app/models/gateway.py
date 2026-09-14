import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class GatewayStatus(str, enum.Enum):
    online = "online"
    offline = "offline"


class Gateway(Base):
    """
    Representa o Gateway Linux (Edge Host) instalado junto à máquina,
    responsável por terminar o túnel WireGuard e fazer a ponte até o CLP.
    """

    __tablename__ = "gateways"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    wireguard_public_key = Column(String, nullable=True)
    wireguard_ip_atribuido = Column(String, nullable=True)  # ex: 10.10.0.5/32
    status = Column(Enum(GatewayStatus), default=GatewayStatus.offline)
    ultimo_heartbeat = Column(DateTime, nullable=True)

    maquina = relationship("Machine", back_populates="gateway", uselist=False)
