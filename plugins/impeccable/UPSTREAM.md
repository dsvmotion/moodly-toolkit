# Origen de este plugin

- **Origen:** https://github.com/pbakaus/impeccable
- **Commit:** `ec229b48547f24685ffb22aa51c462c5ae27908c`
- **Revisado:** 2026-11-10
- **Licencia:** Apache-2.0 (ver `LICENSE` y `NOTICE.md`)

## Qué se copió

De la carpeta `plugin/` del origen: `.claude-plugin/plugin.json`, `agents/` y `skills/impeccable/` (`SKILL.md` y `reference/`). De la raíz: `LICENSE` y `NOTICE.md`.

## Qué se quitó

- `hooks/hooks.json`: tres hooks (`SessionStart`, `PostToolUse` en cada `Edit` o `Write`, y `Stop`) que ejecutaban el lanzador del motor.
- `skills/impeccable/scripts/` entero: el lanzador (`impeccable` e `impeccable.cmd`), que descarga un binario nativo de las releases de GitHub del autor (`engine-v0.1.22`, comprobado con sha256) en `~/.impeccable/` y lo ejecuta; ese binario puede además escribir hooks en `.claude/settings.local.json`. También sus datos y el JavaScript del modo `live`, que solo usa el motor.
- `.grok-plugin/`.

Sin el motor, la skill sigue su propio camino previsto («Launcher unavailable» en `SKILL.md`): lee `PRODUCT.md` y `DESIGN.md` directamente y aplica las guías de `reference/`. Los subcomandos que dependen del motor (`detect`, `live`, `hooks`, `doctor`, `pin`, `build-phase`) no funcionan.

## Qué se cambió respecto al origen

Nada: los archivos copiados son idénticos a los del origen.

Para actualizarlo, sigue «Cómo se actualiza un plugin» del README del repositorio.
