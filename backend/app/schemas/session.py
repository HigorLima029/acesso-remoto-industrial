from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.session import SessionStatus


class SessionRequest(BaseModel):
    machine_id: int


class SessionOut(BaseModel):
    id: int
    machine_id: int
    user_id: int
    status: SessionStatus
    iniciada_em: Optional[datetime] = None
    encerrada_em: Optional[datetime] = None
    ip_cliente_vpn: Optional[str] = None

    class Config:
        from_attributes = True
