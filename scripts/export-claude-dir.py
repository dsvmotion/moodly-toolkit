#!/usr/bin/env python3
"""Exporta los plugins de este repositorio a una carpeta `.claude/` aplanada.

Uso:  python3 scripts/export-claude-dir.py <destino> [--sin-hook]

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
                        (con `--sin-hook` no se escribe)
  toolkit/              licencias, origen de cada plugin y archivos de apoyo
  toolkit/SKILLS-INDEX.md  una línea por skill: las visibles y las ocultas

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

  - visibilidad: las skills de `scripts/visible-skills.txt` quedan como están
    (su descripción entra en el listado de cada sesión). A todas las demás se
    les añade `disable-model-invocation: true` al frontmatter: siguen en la
    carpeta, no gastan contexto y se usan leyendo su `SKILL.md` cuando el
    índice (`toolkit/SKILLS-INDEX.md`) dice que encajan con la tarea.

No ejecuta nada de los plugins: solo lee y copia archivos.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
LEGAL = ["privacy-legal", "ai-governance-legal", "product-legal", "commercial-legal"]
VISIBLE_FILE = ROOT / "scripts" / "visible-skills.txt"
HIDE = "disable-model-invocation: true"

INDEX_HEAD = """# Índice de skills

Generado por `scripts/export-claude-dir.py` de moodly-toolkit. No se edita a mano.

- **Visibles:** aparecen en el listado de skills de cada sesión y se cargan con
  la herramienta Skill cuando la tarea encaja.
- **Ocultas:** no aparecen en el listado y no gastan contexto. Cuando una
  encaja con la tarea, se lee su archivo `.claude/skills/<nombre>/SKILL.md` y se
  sigue. Si su texto cita `${CLAUDE_SKILL_DIR}`, es esa misma carpeta.

Quien planifica una tarea (o responde a una petición) mira este índice y dice
qué skill encaja; la persona no tiene que conocer los nombres.
"""

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


def read_visible():
    names = [l.strip() for l in VISIBLE_FILE.read_text(encoding="utf-8").splitlines()]
    return [n for n in names if n and not n.startswith("#")]


def summary(front):
    """La descripción del frontmatter, en una línea y recortada."""
    m = re.search(r"^description:[ \t]*(.*?)(?=^[A-Za-z][\w-]*:|\Z)", front, re.M | re.S)
    text = " ".join(m.group(1).split()) if m else ""
    text = text.strip("'\"")
    text = re.sub(r"^[>|][+-]?\s*", "", text)
    if len(text) > 160:
        text = text[:157].rsplit(" ", 1)[0] + "…"
    return text


def apply_visibility(skills, toolkit):
    """Oculta las skills que no están en la lista y escribe el índice."""
    visible = read_visible()
    present = sorted(p.name for p in skills.iterdir() if (p / "SKILL.md").is_file())
    missing = [n for n in visible if n not in present]
    if missing:
        die(f"{VISIBLE_FILE.name} nombra skills que no existen: {', '.join(missing)}")
    rows = {True: [], False: []}
    for name in present:
        path = skills / name / "SKILL.md"
        front, body = split_frontmatter(path.read_text(encoding="utf-8"), path)
        shown = name in visible
        if shown and HIDE in front:
            die(f"{name} está en {VISIBLE_FILE.name} pero su origen la trae oculta")
        if not shown and HIDE not in front:
            path.write_text(f"---\n{front}\n{HIDE}\n---\n{body}", encoding="utf-8")
        rows[shown].append(f"- `{name}`: {summary(front)}")
    out = [INDEX_HEAD, f"\n## Visibles ({len(rows[True])})\n", *rows[True],
           f"\n## Ocultas ({len(rows[False])})\n", *rows[False], ""]
    (toolkit / "SKILLS-INDEX.md").write_text("\n".join(out), encoding="utf-8")
    return len(rows[True]), len(rows[False])


def copy_meta(plugin, dest_toolkit):
    out = dest_toolkit / plugin
    out.mkdir(parents=True, exist_ok=True)
    for name in ("LICENSE", "NOTICE.md", "UPSTREAM.md"):
        if (PLUGINS / plugin / name).is_file():
            shutil.copy2(PLUGINS / plugin / name, out / name)
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--sin-hook"]
    with_hook = "--sin-hook" not in sys.argv[1:]
    if len(args) != 1 or args[0].startswith("--"):
        die("uso: export-claude-dir.py <destino> [--sin-hook]")
    dest = Path(args[0]).resolve()
    wanted = ("skills", "agents", "hooks", "toolkit") if with_hook else ("skills", "agents", "toolkit")
    for sub in ("skills", "agents", "hooks", "toolkit"):
        if sub in wanted and (dest / sub).exists():
            die(f"{dest / sub} ya existe; quítalo antes de exportar")
    skills, agents, hooks, toolkit = (dest / s for s in ("skills", "agents", "hooks", "toolkit"))
    for d in (dest / s for s in wanted):
        d.mkdir(parents=True)

    # superpowers, design-motion, impeccable: skills tal cual.
    for plugin in ("superpowers", "design-motion", "impeccable"):
        for src in sorted((PLUGINS / plugin / "skills").iterdir()):
            if (src / "SKILL.md").is_file():
                copy_skill(src, skills, src.name)
        copy_meta(plugin, toolkit)

    # superpowers: su hook de arranque. Lee ../skills/using-superpowers/SKILL.md
    # desde donde está, así que vale sin cambios en <destino>/hooks/.
    if with_hook:
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

    n_visible, n_hidden = apply_visibility(skills, toolkit)
    n_agents = sum(1 for _ in agents.glob("*.md"))
    print(f"exportado en {dest}: {n_visible + n_hidden} skills ({n_visible} visibles, {n_hidden} ocultas), "
          f"{n_agents} agentes, {1 if with_hook else 0} hook")


if __name__ == "__main__":
    main()
