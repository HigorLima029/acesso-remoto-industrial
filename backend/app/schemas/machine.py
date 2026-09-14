from typing import Optional

from pydantic import BaseModel

from app.models.gateway import GatewayStatus


class GatewayOut(BaseModel):
    id: int
    nome: str
    status: GatewayStatus
    wireguard_ip_atribuido: Optional[str] = None

    class Config:
        from_attributes = True


class GatewayCreate(BaseModel):
    nome: str
    wireguard_public_key: Optional[str] = None


class MachineCreate(BaseModel):
    codigo: str
    nome: str
    local: Optional[str] = None
    fabricante_clp: Optional[str] = None
    protocolo_industrial: Optional[str] = "OPC-UA (a validar)"
    gateway_id: Optional[int] = None


class MachineOut(BaseModel):
    id: int
    codigo: str
    nome: str
    local: Optional[str] = None
    protocolo_industrial: Optional[str] = None
    gateway: Optional[GatewayOut] = None

    class Config:
        from_attributes = True
