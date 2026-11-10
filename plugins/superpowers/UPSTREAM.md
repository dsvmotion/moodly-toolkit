# Origen de este plugin

- **Origen:** https://github.com/obra/superpowers
- **Commit:** `22f0b463e7a5e579904dd6211a520321035526f7`
- **Revisado:** 2026-11-10
- **Licencia:** MIT (ver `LICENSE`)

## Qué se copió

`.claude-plugin/plugin.json`, `hooks/` (`hooks.json`, `run-hook.cmd` y `session-start`), `skills/` y `LICENSE`.

## Qué se quitó

Todo lo que no es el plugin de Claude Code: los manifiestos de otras herramientas (`.codex-plugin`, `.cursor-plugin`, `.opencode`, `.pi` y demás), `hooks/hooks-cursor.json`, `index.js`, `package.json`, `scripts/` (herramientas de desarrollo del autor), `tests/`, `docs/` y `assets/`.

## Qué se cambió respecto al origen

Una línea de `skills/brainstorming/scripts/server.cjs`: `SUPERPOWERS_TELEMETRY_DISABLED` vale siempre `true`. En el origen, la página del «visual companion» carga un logotipo desde `primeradiant.com` como telemetría, salvo que se defina una variable de entorno. Aquí no lo carga nunca.

Para actualizarlo, sigue «Cómo se actualiza un plugin» del README del repositorio.
