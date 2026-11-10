# Origen de este plugin

- **Origen:** https://github.com/anthropics/claude-for-legal
- **Commit:** `4a6c651889c97cc9140580363c73e0eb17379c2b`
- **Revisado:** 2026-11-10
- **Licencia:** Apache-2.0 (ver `LICENSE`)

## Qué se copió

La carpeta `product-legal/` del origen (`.claude-plugin/plugin.json`, `skills/`, `CLAUDE.md`, `README.md` y `references/`) y el `LICENSE` de la raíz. El origen no trae `NOTICE`.

## Qué se quitó

- `.mcp.json`: servidores MCP remotos de Slack, Google Drive, Linear, Atlassian y Asana.
- `hooks/hooks.json`: vacío.
- `agents/launch-watcher.md`: agente programado que lee Jira o Linear y puede enviar mensajes por Slack (`mcp__*__slack_send_message`).

## Qué se cambió respecto al origen

Nada: los archivos copiados son idénticos a los del origen. Algunos textos mencionan los conectores y agentes quitados; no están disponibles aquí.

Para actualizarlo, sigue «Cómo se actualiza un plugin» del README del repositorio.
