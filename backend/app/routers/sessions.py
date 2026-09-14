from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.gateway import GatewayStatus
from app.models.machine import Machine
from app.models.permission import MachinePermission
from app.models.session import AccessSession, SessionStatus
from app.models.user import User, UserRole
from app.schemas.session import SessionRequest, SessionOut

router = APIRouter(prefix="/sessions", tags=["sessões de acesso"])


@router.post("/request", response_model=SessionOut, status_code=201)
def solicitar_sessao(
    payload: SessionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Implementa o fluxo operacional do documento:
    1. Valida se o usuário tem permissão para a máquina.
    2. Verifica se o gateway está online.
    3. Cria o registro de sessão (auditoria).
    4. (Placeholder) Aciona a configuração do túnel WireGuard.
    """
    machine = db.query(Machine).filter(Machine.id == payload.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina não encontrada")

    # 1. Validação de permissão (admins sempre podem; técnicos precisam de permissão explícita)
    if user.role != UserRole.admin:
        tem_permissao = (
            db.query(MachinePermission)
            .filter(
                MachinePermission.user_id == user.id,
                MachinePermission.machine_id == machine.id,
            )
            .first()
        )
        if not tem_permissao:
            sessao_negada = AccessSession(
                user_id=user.id,
                machine_id=machine.id,
                status=SessionStatus.negada,
                observacoes="Usuário sem permissão para esta máquina",
            )
            db.add(sessao_negada)
            db.commit()
            raise HTTPException(status_code=403, detail="Acesso negado: sem permissão para esta máquina")

    # 2. Verifica status do gateway
    if not machine.gateway or machine.gateway.status != GatewayStatus.online:
        sessao_falha = AccessSession(
            user_id=user.id,
            machine_id=machine.id,
            status=SessionStatus.falha,
            observacoes="Gateway offline ou não configurado",
        )
        db.add(sessao_falha)
        db.commit()
        raise HTTPException(status_code=409, detail="Gateway offline: não é possível iniciar sessão")

    # 3. Cria sessão ativa (o provisionamento real do túnel WireGuard entra na Etapa 3)
    sessao = AccessSession(
        user_id=user.id,
        machine_id=machine.id,
        status=SessionStatus.ativa,
        iniciada_em=datetime.now(timezone.utc),
    )
    db.add(sessao)
    db.commit()
    db.refresh(sessao)
    return sessao


@router.post("/{session_id}/close", response_model=SessionOut)
def encerrar_sessao(
    session_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    sessao = db.query(AccessSession).filter(AccessSession.id == session_id).first()
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    if sessao.user_id != user.id and user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Sem permissão para encerrar esta sessão")

    sessao.status = SessionStatus.encerrada
    sessao.encerrada_em = datetime.now(timezone.utc)
    db.commit()
    db.refresh(sessao)
    return sessao


@router.get("/", response_model=List[SessionOut])
def listar_sessoes(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    """Log de auditoria: admin vê tudo, técnico vê apenas as próprias sessões."""
    query = db.query(AccessSession)
    if user.role != UserRole.admin:
        query = query.filter(AccessSession.user_id == user.id)
    return query.order_by(AccessSession.id.desc()).all()
