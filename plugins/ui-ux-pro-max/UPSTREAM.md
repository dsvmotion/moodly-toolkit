# Origen de este plugin

- **Origen:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **Commit:** `9b675f0b13c9c28dec445e8ce4633c18c39b6467`
- **Revisado:** 2026-11-10
- **Licencia:** MIT (ver `LICENSE`)

## Qué se copió

`.claude-plugin/plugin.json`, la skill `.claude/skills/ui-ux-pro-max/` (`SKILL.md`, `data/`, `references/` y `scripts/`) y `LICENSE`. Se conserva la ruta `.claude/skills/` porque `plugin.json` y `SKILL.md` la usan.

## Qué se quitó

- Las otras seis skills del origen (`banner-design`, `brand`, `design`, `design-system`, `slides` y `ui-styling`): generan logotipos, identidad de marca, banners y presentaciones, que el proyecto no necesita. Sus scripts leen claves de `~/.claude/.env` y llaman a APIs de imagen de terceros (Gemini, Atlas Cloud y MuAPI), descargan fotos de Pexels o lanzan `npx shadcn`.
- `stack/`, con su `.mcp.json` (tres servidores MCP por `npx … @latest`: Playwright, Chrome DevTools y shadcn).
- `cli/` (el instalador de npm), `gallery/`, `src/`, `scripts/` de la raíz, `docs/`, `projects/`, `preview/`, las capturas y los README traducidos.
- `scripts/tests/` de la skill.

## Qué se cambió respecto al origen

Nada: los archivos copiados son idénticos a los del origen (`plugin.json` pierde el bit de ejecutable que traía).

Para actualizarlo, sigue «Cómo se actualiza un plugin» del README del repositorio.
