# Túnel Seguro — WireGuard (Etapa 3)

Este documento cobre **o que o túnel precisa fazer**, do ponto de vista da
arquitetura da API. A instalação/configuração prática do Linux que vai
rodar o gateway fica para depois — quando chegarmos nessa etapa, montamos
juntos a VM do zero.

## Papel de cada ponta

- **Servidor WireGuard (nuvem ou perto da borda)**: concentra os peers.
  Cada técnico autorizado e cada gateway de fábrica é um "peer".
- **Gateway Linux (fábrica)**: cliente WireGuard permanente, com IP fixo
  dentro da rede virtual do túnel (ex.: `10.10.0.5/32`). É ele quem faz a
  ponte para a rede local do CLP.
- **Estação do técnico**: recebe um peer temporário/dinâmico quando uma
  sessão é aprovada pela API.

## O que já existe no backend (placeholder)

- Tabela `gateways` já guarda `wireguard_public_key` e
  `wireguard_ip_atribuido`.
- Tabela `access_sessions` já guarda `ip_cliente_vpn` para registrar qual
  IP do túnel foi atribuído ao técnico naquela sessão.
- O endpoint `POST /sessions/request` já é o ponto de extensão onde, no
  futuro, entra a chamada real para:
  1. gerar um par de chaves WireGuard temporário para o técnico (ou usar
     um peer fixo, se preferir simplificar o MVP);
  2. adicionar esse peer à interface WireGuard do servidor
     (`wg set wg0 peer <chave-pública> allowed-ips <ip>/32`);
  3. devolver ao frontend o arquivo de configuração `.conf` (ou QR code)
     para o técnico importar no cliente WireGuard dele.

## Isolamento do CLP

O gateway Linux deve rotear **apenas** o tráfego necessário até o CLP
(ex.: uma única porta/IP interno), nunca a rede industrial inteira. Isso
é feito nas regras de `AllowedIPs` do peer do gateway e em regras de
firewall (iptables/nftables) no próprio gateway — algo que detalhamos
quando formos configurar a VM.

## Próximo passo prático

Quando você quiser avançar, começamos por:
1. Decidir onde o **servidor WireGuard** vai rodar (mesma VM da API? VM
   dedicada?).
2. Gerar o par de chaves do servidor.
3. Só então partimos para a configuração do **Gateway Linux** (a etapa que
   você pediu para deixar por último).
