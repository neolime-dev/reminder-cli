# Lembrete CLI

Um utilitário de linha de comando (CLI) simples e leve para Linux que envia notificações nativas após um determinado período. Ideal para usuários de Window Managers (i3, Sway, Hyprland) ou qualquer ambiente desktop.

## 🚀 Funcionalidades

- Sintaxe simples e natural (ex: `10m`, `1h`, `15:30`).
- Integração nativa com o sistema de notificações (`notify-send`).
- Leve: Escrito em Python, sem dependências pesadas.
- Roda em segundo plano (libera seu terminal imediatamente).

## 📋 Pré-requisitos

- **Python 3**
- **libnotify** (comando `notify-send`)
  - Arch: `sudo pacman -S libnotify`
  - Debian/Ubuntu: `sudo apt install libnotify-bin`

## 🛠️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/lembrete-cli.git
   cd lembrete-cli
   ```

2. Dê permissão de execução e instale no seu PATH (ex: `~/.local/bin`):
   ```bash
   chmod +x lembrete.py
   cp lembrete.py ~/.local/bin/lembrete
   ```

3. Certifique-se de que `~/.local/bin` está no seu PATH.

## 📖 Uso

```bash
lembrete "Mensagem" <tempo>
```

### Exemplos

```bash
# Daqui a 10 minutos
lembrete "Tirar o lixo" 10m

# Daqui a 1 hora
lembrete "Reunião com a equipe" 1h

# Em um horário específico (hoje)
lembrete "Almoço" 12:00

# Apenas segundos
lembrete "Teste rápido" 30s
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
