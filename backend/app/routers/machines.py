from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.gateway import Gateway, GatewayStatus
from app.models.machine import Machine
from app.models.user import User, UserRole
from app.schemas.machine import MachineCreate, MachineOut, GatewayCreate, GatewayOut

router = APIRouter(prefix="/machines", tags=["máquinas"])
gateway_router = APIRouter(prefix="/gateways", tags=["gateways"])


def _require_admin(user: User):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem executar esta ação")


@router.get("/", response_model=List[MachineOut])
def listar_maquinas(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Lista o inventário de máquinas com status de conectividade do gateway."""
    return db.query(Machine).all()


@router.post("/", response_model=MachineOut, status_code=201)
def cadastrar_maquina(
    machine_in: MachineCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _require_admin(user)
    if db.query(Machine).filter(Machine.codigo == machine_in.codigo).first():
        raise HTTPException(status_code=400, detail="Código de máquina já cadastrado")

    machine = Machine(**machine_in.model_dump())
    db.add(machine)
    db.commit()
    db.refresh(machine)
    return machine


@gateway_router.post("/", response_model=GatewayOut, status_code=201)
def cadastrar_gateway(
    gateway_in: GatewayCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _require_admin(user)
    gateway = Gateway(**gateway_in.model_dump())
    db.add(gateway)
    db.commit()
    db.refresh(gateway)
    return gateway


@gateway_router.post("/{gateway_id}/heartbeat", response_model=GatewayOut)
def heartbeat_gateway(gateway_id: int, db: Session = Depends(get_db)):
    """
    Endpoint chamado periodicamente PELO gateway Linux (edge host) para
    reportar que está online. Sem esse heartbeat recente, o status cai
    para offline (ver rotina de expiração a ser implementada na Etapa 2).
    """
    gateway = db.query(Gateway).filter(Gateway.id == gateway_id).first()
    if not gateway:
        raise HTTPException(status_code=404, detail="Gateway não encontrado")

    gateway.status = GatewayStatus.online
    gateway.ultimo_heartbeat = datetime.now(timezone.utc)
    db.commit()
    db.refresh(gateway)
    return gateway
