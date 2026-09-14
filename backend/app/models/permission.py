from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class MachinePermission(Base):
    """Autorização de um usuário para acessar remotamente uma máquina específica."""

    __tablename__ = "machine_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)

    user = relationship("User", back_populates="permissoes")
    machine = relationship("Machine", back_populates="permissoes")
