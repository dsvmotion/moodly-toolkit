# Origen de este plugin

- **Origen:** https://github.com/Leonxlnx/taste-skill
- **Commit:** `f6b76575f949707b4e3c37cd86cb44b0b98643e8`
- **Revisado:** 2026-11-10
- **Licencia:** MIT (ver `LICENSE`)

## Qué se copió

`skills/taste-skill/` (`SKILL.md`, `references/`, `library/`, `scripts/` y `assets/`) y `LICENSE`. Los créditos y licencias de fotos e iconos van dentro de `assets/` (archivos `*credits.json`).

## Qué se quitó

`install.sh` (enlaza las skills en `~/.claude`), `.codex-plugin/`, `.agents/`, `.github/`, `tests/`, `examples/` y las imágenes del README.

## Qué se cambió respecto al origen

- **Nuevo:** `.claude-plugin/plugin.json`. El origen solo lo declaraba en su `marketplace.json`.
- `skills/taste-skill/SKILL.md`: se quita del frontmatter el bloque `hooks`. Añadía un hook `Stop` (hasta 600 s) que, una vez invocada la skill, lanzaba `scripts/gate.mjs` con un Chrome sin interfaz en cada parada y podía bloquearla; además buscaba `gate.mjs` en la carpeta del proyecto y en `~/.claude`, fuera de esta copia. El comprobador se lanza a mano: `node scripts/gate.mjs` (ver `references/gate.md`).

Para actualizarlo, sigue «Cómo se actualiza un plugin» del README del repositorio.
