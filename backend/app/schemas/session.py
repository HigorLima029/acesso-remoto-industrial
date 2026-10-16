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
    client_public_key: Optional[str] = None

    class Config:
        from_attributes = True


class SessionCreatedOut(SessionOut):
    """
    Resposta de POST /sessions/request: inclui, além dos dados da sessão,
    a configuração WireGuard pronta para o técnico importar no cliente dele,
    e o comando que o administrador precisa rodar no servidor VPN para
    autorizar esse peer (passo manual neste MVP local).
    """

    wireguard_config: Optional[str] = None
    comando_autorizacao_servidor: Optional[str] = None
