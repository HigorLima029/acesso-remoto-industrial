import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.session import AccessSession


def generate_keypair() -> tuple[str, str]:
    """
    Gera um par de chaves compatível com WireGuard (Curve25519),
    sem depender do binário `wg` instalado no sistema.
    Retorna (chave_privada_base64, chave_publica_base64).
    """
    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    return (
        base64.b64encode(private_bytes).decode("utf-8"),
        base64.b64encode(public_bytes).decode("utf-8"),
    )


def next_available_ip(db: Session, network_prefix: str = "10.10.0") -> str:
    """
    Escolhe o próximo IP livre dentro da rede do túnel (10.10.0.0/24).
    .1 é reservado para o servidor; clientes começam em .2.
    """
    sessoes = (
        db.query(AccessSession)
        .filter(AccessSession.ip_cliente_vpn.isnot(None))
        .all()
    )
    usados = set()
    for s in sessoes:
        try:
            ip = s.ip_cliente_vpn.split("/")[0]
            usados.add(int(ip.split(".")[-1]))
        except (ValueError, IndexError):
            continue

    for octeto in range(2, 255):
        if octeto not in usados:
            return f"{network_prefix}.{octeto}/32"

    raise RuntimeError("Sem IPs disponíveis no pool do túnel WireGuard")


def build_client_config(client_private_key: str, client_ip: str) -> str:
    """Monta o arquivo .conf que o técnico importa no cliente WireGuard dele."""
    return (
        "[Interface]\n"
        f"PrivateKey = {client_private_key}\n"
        f"Address = {client_ip}\n"
        "DNS = 1.1.1.1\n"
        "\n"
        "[Peer]\n"
        f"PublicKey = {settings.wg_server_public_key}\n"
        f"Endpoint = {settings.wg_server_endpoint}\n"
        "AllowedIPs = 10.10.0.0/24\n"
        "PersistentKeepalive = 25\n"
    )


def build_server_peer_command(client_public_key: str, client_ip: str) -> str:
    """
    Comando que precisa ser executado NO SERVIDOR WireGuard para autorizar
    esse peer. Em produção (API e servidor no mesmo host), isso seria
    disparado automaticamente via subprocess; hoje é um passo manual.
    """
    ip_sem_mascara = client_ip.split("/")[0]
    return f"sudo wg set wg0 peer {client_public_key} allowed-ips {ip_sem_mascara}/32"