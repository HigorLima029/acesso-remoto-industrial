# Gateway Linux (Edge Host) — FICA PARA O FINAL

Combinado: essa parte fica por último. Quando chegar a hora, eu te guio
do zero, incluindo:

- Como criar a máquina virtual (VirtualBox, VMware, ou uma VM na nuvem —
  vemos qual faz mais sentido pro seu caso).
- Qual distribuição Linux usar (recomendo Ubuntu Server ou Debian, por
  serem leves e bem documentados).
- Instalação e configuração do cliente WireGuard.
- Instalação de um pequeno agente/script para:
  - enviar heartbeat periódico para `POST /gateways/{id}/heartbeat`;
  - fazer a ponte de rede até o CLP.
- Regras básicas de firewall para isolar o CLP.

Não precisa se preocupar em lembrar nada agora — quando avisar que quer
seguir para essa etapa, começamos pelo básico (criar a VM) e vamos
subindo o nível aos poucos.
