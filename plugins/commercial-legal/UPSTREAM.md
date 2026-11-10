# Origen de este plugin

- **Origen:** https://github.com/anthropics/claude-for-legal
- **Commit:** `4a6c651889c97cc9140580363c73e0eb17379c2b`
- **Revisado:** 2026-11-10
- **Licencia:** Apache-2.0 (ver `LICENSE`)

## Qué se copió

La carpeta `commercial-legal/` del origen (`.claude-plugin/plugin.json`, `skills/`, `CLAUDE.md`, `README.md` y `logs/`) y el `LICENSE` de la raíz. El origen no trae `NOTICE`.

## Qué se quitó

- `.mcp.json`: servidores MCP remotos de Ironclad, DocuSign, iManage, TopCounsel, Definely, Slack y Google Drive.
- `hooks/hooks.json`: vacío.
- `agents/`: `renewal-watcher`, `deal-debrief` y `playbook-monitor`, agentes programados que dependen de esos conectores; dos de ellos pueden enviar mensajes por Slack y el tercero pide las herramientas `search`, `fetch`, `query` y `list` de cualquier servidor MCP conectado.

## Qué se cambió respecto al origen

Nada: los archivos copiados son idénticos a los del origen. Algunos textos mencionan los conectores y agentes quitados; no están disponibles aquí.

Para actualizarlo, sigue «Cómo se actualiza un plugin» del README del repositorio.
