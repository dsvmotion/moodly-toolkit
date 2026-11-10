#!/usr/bin/env python3
"""Exporta los plugins de este repositorio a una carpeta `.claude/` aplanada.

Uso:  python3 scripts/export-claude-dir.py <destino>

`<destino>` es la carpeta `.claude/` del repositorio que recibe las copias.
Debe no existir o no tener todavía `skills/`, `agents/`, `hooks/` ni `toolkit/`.
No escribe `settings.json`: el hook de arranque se registra a mano en el
`.claude/settings.json` del repositorio (el bloque está en el README).

Por qué hace falta: una sesión de Claude Code en la nube no carga los plugins
de un repositorio (ni de un marketplace ni enteros dentro de `.claude/skills/`),
pero sí las skills sueltas, los agentes y los hooks que viajan en `.claude/`.

Qué escribe en `<destino>`:
  skills/<nombre>/      una carpeta por skill, con su SKILL.md
  agents/<nombre>.md    los agentes de impeccable
  hooks/session-start   el hook de arranque de superpowers, sin cambios
  toolkit/              licencias, origen de cada plugin y archivos de apoyo

Qué cambia respecto a `plugins/` (todo lo demás se copia byte a byte):
  - legal: las skills llevan el nombre de su plugin delante, porque los cuatro
    plugins repiten nombres (`customize`, `matter-workspace`...). Cambia la
    carpeta y la línea `name:` del frontmatter.
  - legal: la plantilla del perfil (`CLAUDE.md` del plugin) pasa a
    `toolkit/<plugin>/practice-profile-template.md` y la ruta que la cita en
    `cold-start-interview` se reescribe.
  - ui-ux-pro-max: la ruta de plugin del buscador pasa a `${CLAUDE_SKILL_DIR}`,
    y su carpeta de scripts lleva un `.gitignore` nuevo para el `__pycache__/`
    que deja el buscador al ejecutarse.
  - taste-skill: solo `SKILL.md` y `references/`, con un aviso al principio de
    que faltan `scripts/` y `assets/`.

No ejecuta nada de los plugins: solo lee y copia archivos.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
LEGAL = ["privacy-legal", "ai-governance-legal", "product-legal", "commercial-legal"]

TASTE_NOTICE = """
> **Copia reducida (moodly-toolkit).** Esta copia trae solo este `SKILL.md` y
> `references/`. No trae `scripts/` ni `assets/` del original: los pasos que
> piden ejecutar `node <skill>/scripts/...` o copiar algo de `assets/` no están
> disponibles aquí. No los simules ni inventes su resultado: aplica las reglas
> de diseño de este documento y de `references/`, y di qué comprobación no se
> pudo hacer.
"""


def die(msg):
    sys.exit(f"export-claude-dir: {msg}")


def split_frontmatter(text, path):
    if not text.startswith("---\n"):
        die(f"{path} no empieza por frontmatter")
    end = text.index("\n---\n", 4)
    return text[4:end], text[end + 5:]


def copy_skill(src, dest_skills, name):
    dest = dest_skills / name
    if dest.exists():
        die(f"dos skills se llaman igual: {name}")
    shutil.copytree(src, dest)
    return dest


def rewrite(path, old, new, count=None):
    text = path.read_text(encoding="utf-8")
    found = text.count(old)
    if found == 0 or (count is not None and found != count):
        die(f"{path}: se esperaban {count or 'una o más'} apariciones de {old!r}, hay {found}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def copy_meta(plugin, dest_toolkit):
    out = dest_toolkit / plugin
    out.mkdir(parents=True, exist_ok=True)
    for name in ("LICENSE", "NOTICE.md", "UPSTREAM.md"):
        if (PLUGINS / plugin / name).is_file():
            shutil.copy2(PLUGINS / plugin / name, out / name)
    return out


def main():
    if len(sys.argv) != 2:
        die("uso: export-claude-dir.py <destino>")
    dest = Path(sys.argv[1]).resolve()
    for sub in ("skills", "agents", "hooks", "toolkit"):
        if (dest / sub).exists():
            die(f"{dest / sub} ya existe; quítalo antes de exportar")
    skills, agents, hooks, toolkit = (dest / s for s in ("skills", "agents", "hooks", "toolkit"))
    for d in (skills, agents, hooks, toolkit):
        d.mkdir(parents=True)

    # superpowers, design-motion, impeccable: skills tal cual.
    for plugin in ("superpowers", "design-motion", "impeccable"):
        for src in sorted((PLUGINS / plugin / "skills").iterdir()):
            if (src / "SKILL.md").is_file():
                copy_skill(src, skills, src.name)
        copy_meta(plugin, toolkit)

    # superpowers: su hook de arranque. Lee ../skills/using-superpowers/SKILL.md
    # desde donde está, así que vale sin cambios en <destino>/hooks/.
    shutil.copy2(PLUGINS / "superpowers" / "hooks" / "session-start", hooks / "session-start")

    # design-motion: las dos chuletas no son skills.
    for name in ("ui-cheatsheet.md", "performance-cheatsheet.md"):
        shutil.copy2(PLUGINS / "design-motion" / name, toolkit / "design-motion" / name)

    # impeccable: agentes.
    for src in sorted((PLUGINS / "impeccable" / "agents").glob("*.md")):
        shutil.copy2(src, agents / src.name)

    # ui-ux-pro-max: una skill, con la ruta del buscador reescrita.
    uupm = copy_skill(PLUGINS / "ui-ux-pro-max" / ".claude" / "skills" / "ui-ux-pro-max", skills, "ui-ux-pro-max")
    rewrite(uupm / "SKILL.md", "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/", "${CLAUDE_SKILL_DIR}/")
    (uupm / "scripts" / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    copy_meta("ui-ux-pro-max", toolkit)

    # taste-skill: solo SKILL.md y references/, con aviso.
    taste_src = PLUGINS / "taste-skill" / "skills" / "taste-skill"
    text = (taste_src / "SKILL.md").read_text(encoding="utf-8")
    front, body = split_frontmatter(text, taste_src / "SKILL.md")
    name = re.search(r"^name:\s*(\S+)\s*$", front, re.M).group(1)
    taste = skills / name
    if taste.exists():
        die(f"dos skills se llaman igual: {name}")
    taste.mkdir()
    (taste / "SKILL.md").write_text(f"---\n{front}\n---\n{TASTE_NOTICE}{body}", encoding="utf-8")
    shutil.copytree(taste_src / "references", taste / "references")
    copy_meta("taste-skill", toolkit)

    # legal: skills con el plugin delante; plantilla y apoyo a toolkit/.
    for plugin in LEGAL:
        meta = copy_meta(plugin, toolkit)
        template = f".claude/toolkit/{plugin}/practice-profile-template.md"
        shutil.copy2(PLUGINS / plugin / "CLAUDE.md", meta / "practice-profile-template.md")
        shutil.copy2(PLUGINS / plugin / "README.md", meta / "README.md")
        if (PLUGINS / plugin / "references").is_dir():
            shutil.copytree(PLUGINS / plugin / "references", meta / "references")
        for src in sorted((PLUGINS / plugin / "skills").iterdir()):
            if not (src / "SKILL.md").is_file():
                continue
            new_name = f"{plugin}-{src.name}"
            out = copy_skill(src, skills, new_name)
            rewrite(out / "SKILL.md", f"\nname: {src.name}\n", f"\nname: {new_name}\n", count=1)
            if src.name == "cold-start-interview":
                rewrite(out / "SKILL.md", "`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`", f"`{template}` (desde la raíz del repositorio)", count=1)

    n_skills = sum(1 for p in skills.iterdir() if (p / "SKILL.md").is_file())
    n_agents = sum(1 for _ in agents.glob("*.md"))
    print(f"exportado en {dest}: {n_skills} skills, {n_agents} agentes, 1 hook")


if __name__ == "__main__":
    main()
