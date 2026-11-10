# moodly-toolkit

Marketplace de plugins de Claude Code del proyecto. Cada plugin es una copia revisada de su origen, fijada a un commit (revisión del 2026-11-10). Nada se descarga de terceros al instalar: lo que hay aquí es lo que se ejecuta.

## Plugins

| Plugin | Para qué | Origen | Commit | Licencia |
| --- | --- | --- | --- | --- |
| `superpowers` | Método de trabajo: diseñar antes de construir, planes, TDD, depuración y revisión de código | [obra/superpowers](https://github.com/obra/superpowers) | `22f0b463e7a5e579904dd6211a520321035526f7` | MIT |
| `impeccable` | Diseño de interfaz: dar forma, criticar, auditar y pulir | [pbakaus/impeccable](https://github.com/pbakaus/impeccable), carpeta `plugin/` | `ec229b48547f24685ffb22aa51c462c5ae27908c` | Apache-2.0, con `NOTICE.md` |
| `ui-ux-pro-max` | Base de datos local de estilos, paletas, tipografías, gráficas y guías de UX | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `9b675f0b13c9c28dec445e8ce4633c18c39b6467` | MIT |
| `taste-skill` | Páginas web de empresa sin aspecto genérico | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | `f6b76575f949707b4e3c37cd86cb44b0b98643e8` | MIT |
| `design-motion` | Animación e interacción | [emilkowalski/skills](https://github.com/emilkowalski/skills): `skills/`, `ui-cheatsheet.md` y `performance-cheatsheet.md` | `715c1807e08c497cfd1dc4feb450a2a3300ef2a9` | MIT |
| `privacy-legal` | Privacidad: PIAs, DPAs y solicitudes de derechos | [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal), carpeta `privacy-legal/` | `4a6c651889c97cc9140580363c73e0eb17379c2b` | Apache-2.0 |
| `ai-governance-legal` | Gobierno de la IA: inventario, evaluaciones de impacto y términos de proveedores | mismo repositorio, carpeta `ai-governance-legal/` | `4a6c651889c97cc9140580363c73e0eb17379c2b` | Apache-2.0 |
| `product-legal` | Legal de producto: lanzamientos y afirmaciones de marketing | mismo repositorio, carpeta `product-legal/` | `4a6c651889c97cc9140580363c73e0eb17379c2b` | Apache-2.0 |
| `commercial-legal` | Legal comercial: contratos de proveedor, NDAs y renovaciones | mismo repositorio, carpeta `commercial-legal/` | `4a6c651889c97cc9140580363c73e0eb17379c2b` | Apache-2.0 |

Cada plugin lleva su `LICENSE` (y su `NOTICE.md` si el origen lo trae) y un `UPSTREAM.md` con el origen, el commit, lo que se copió, lo que se quitó y lo que se cambió.

Los plugins de legal ayudan a preparar y revisar; no sustituyen a un abogado.

## Cómo se usa

Hay dos formas. Solo la primera sirve en las sesiones en la nube.

### Copias en `.claude/` (sirve en todas partes)

Una sesión de Claude Code en la nube **no carga los plugins de un repositorio**: ni los de un marketplace declarado en su `.claude/settings.json`, ni un plugin entero puesto en `.claude/skills/`. Sí carga las skills sueltas, los agentes y los hooks que viajan en `.claude/`. Probado con sesiones reales en los PRs #4, #5 y #6 de este repositorio.

`scripts/export-claude-dir.py` escribe esa carpeta a partir de `plugins/`:

```bash
python3 scripts/export-claude-dir.py /ruta/al/repositorio/.claude
```

Deja 74 skills en `skills/`, los 4 agentes de `impeccable` en `agents/`, el hook de arranque de `superpowers` en `hooks/session-start` y, en `toolkit/`, las licencias, el origen de cada plugin y sus archivos de apoyo. Solo lee y copia archivos. Lo que cambia respecto a `plugins/` está en la cabecera del script:

- las skills de legal llevan el nombre de su plugin delante (`privacy-legal-dpa-review`), porque los cuatro plugins repiten nombres;
- la ruta del buscador de `ui-ux-pro-max` pasa a `${CLAUDE_SKILL_DIR}`;
- de `taste-skill` van solo `SKILL.md` y `references/` (queda como `design-taste-frontend`), con un aviso de que faltan `scripts/` y `assets/`.

El hook de arranque se registra a mano en el `.claude/settings.json` del repositorio:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "CLAUDE_PLUGIN_ROOT=\"$CLAUDE_PROJECT_DIR/.claude\" bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/session-start\""
          }
        ]
      }
    ]
  }
}
```

Las copias van en un PR del repositorio que las recibe, con el commit de este repositorio del que salen. Así quedan fijadas por construcción.

A tener en cuenta:

- **Sin prefijo de plugin.** Las skills se llaman `brainstorming` o `animate`, no `superpowers:brainstorming`.
- **Muchas skills, poco sitio.** Con las 74, la lista de skills de la sesión recorta: en la prueba, 20 llegaron solo con el nombre, sin descripción.
- **Tres skills no se listan** (`pick-ui-library`, `prototype` y `review-animations`): su origen las marca para que solo las lance una persona.
- **Legal guarda su perfil fuera del repositorio**, en `~/.claude/plugins/config/claude-for-legal/`. En una sesión en la nube esa carpeta se pierde al acabar.

### Marketplace (solo terminal y app de escritorio)

En el `.claude/settings.json` del repositorio que lo quiera:

```json
{
  "extraKnownMarketplaces": {
    "moodly-toolkit": {
      "source": { "source": "github", "repo": "dsvmotion/moodly-toolkit", "ref": "release/v1.0.0" }
    }
  },
  "enabledPlugins": {
    "superpowers@moodly-toolkit": true
  }
}
```

- **Fijado a una versión.** `ref` es una rama de versión de este repositorio (ver «Versiones»). Sin `ref`, quien lo instala sigue `main` y recibe cualquier cambio que entre aquí. Un marketplace no se puede fijar a un commit: `ref` solo admite una rama o una etiqueta. Un plugin suelto sí: su fuente (`github`, `url` o `git-subdir`) admite `sha`.
- Una vez por clon: `claude plugin marketplace add dsvmotion/moodly-toolkit#release/v1.0.0` y después, por cada plugin, `claude plugin install <plugin>@moodly-toolkit --scope project`.
- Este repositorio es público: no hacen falta credenciales para instalarlo, y por eso mismo aquí no entra nada interno del proyecto.

## Revisión de seguridad (2026-11-10)

Se revisó cada hook, script y `.mcp.json` de los seis repositorios de origen antes de copiar nada. No se ejecutó ningún script ni instalador de terceros. Criterio:

- se quita lo que se ejecuta solo (hooks) salvo que sea inocuo y necesario;
- se quita lo que descarga y ejecuta binarios, y los servidores MCP de servicios que el proyecto no usa;
- los scripts que quedan solo corren cuando Claude los lanza con Bash, bajo los permisos de la sesión.

Tras la revisión, el marketplace entero tiene **un hook** (el `SessionStart` de `superpowers`) y **ningún servidor MCP**. Las skills traen unos 165 scripts (7 en `superpowers`, 5 en `ui-ux-pro-max` y 153 en `taste-skill`): ninguno corre solo, pero una skill puede pedir a Claude que los lance, y algunos abren un Chrome sin interfaz o llaman a la red.

| Plugin | Pieza | Qué ejecuta | Red | Permisos | Decisión |
| --- | --- | --- | --- | --- | --- |
| superpowers | Hook `SessionStart` (`hooks/hooks.json` → `run-hook.cmd` → `session-start`) | Bash: lee `skills/using-superpowers/SKILL.md` y lo imprime como contexto de la sesión | Ninguna | Lectura de un archivo del propio plugin | **Se queda** |
| superpowers | `skills/brainstorming/scripts/` (`start-server.sh`, `stop-server.sh`, `server.cjs`, `helper.js`) | Servidor HTTP y WebSocket local para enseñar maquetas en el navegador; solo si la persona acepta el «visual companion» | Escucha en `127.0.0.1` (o en la interfaz que se le pase). En el origen, la página cargaba un logotipo de `primeradiant.com` como telemetría | Escribe en `/tmp/brainstorm-*` o en `.superpowers/brainstorm/`; puede abrir el navegador | **Se queda, con la telemetría apagada** (una línea cambiada) |
| superpowers | Scripts de `executing-plans`, `subagent-driven-development` y `systematic-debugging`; `writing-skills/render-graphs.js` | `git` de solo lectura, el comando de tests que se les pase, `npm test` y `dot` | Ninguna | Escriben en `.superpowers/sdd/` del repositorio | **Se quedan** |
| impeccable | `hooks/hooks.json`: `SessionStart`, `PostToolUse` (`Edit` y `Write`) y `Stop` | El lanzador `scripts/impeccable hook` en cada sesión, en cada edición y en cada parada | La del motor (fila siguiente) | Los del usuario | **Quitado** |
| impeccable | `skills/impeccable/scripts/` (lanzador, `impeccable.cmd`, `live-browser*.js`) | Descarga un binario nativo (`engine-v0.1.22`, con sha256) y lo ejecuta | `github.com/pbakaus/impeccable/releases`; según su documentación, el binario avisa además de versiones nuevas | Escribe en `~/.impeccable/`; el binario puede instalar hooks en `.claude/settings.local.json` | **Quitado**. La skill sigue su camino previsto sin motor |
| impeccable | `agents/` (4 agentes) | Solo instrucciones | Ninguna | `finish-reviewer` no puede escribir; los demás heredan las herramientas de la sesión | **Se quedan** |
| ui-ux-pro-max | `stack/.mcp.json` | Tres servidores MCP por `npx -y …@latest` (Playwright, Chrome DevTools y shadcn) | npm, sin versión fijada | Ejecución de paquetes de npm | **No se copia** |
| ui-ux-pro-max | Skills `banner-design`, `brand`, `design`, `design-system`, `slides` y `ui-styling` | Scripts de Python y Node | APIs de imagen de terceros (Gemini, Atlas Cloud y MuAPI), Pexels y `npx shadcn` | Leen claves de `~/.claude/.env` | **No se copian** |
| ui-ux-pro-max | `scripts/search.py`, `core.py`, `design_system.py`, `reasoning_contract.py` y `validate_data.py` | Python con la biblioteca estándar: busca en los CSV del plugin | Ninguna | Con `--persist`, escribe `design-system/MASTER.md` en el proyecto | **Se quedan** (sin `scripts/tests/`) |
| taste-skill | Hook `Stop` en el frontmatter de `SKILL.md` | `node scripts/gate.mjs --hook claude` en cada parada (hasta 600 s); puede bloquearla. Busca `gate.mjs` también en el proyecto y en `~/.claude` | Las de `gate.mjs` | Los del usuario | **Quitado** |
| taste-skill | `skills/taste-skill/scripts/*.mjs` (10 scripts, unas 17.000 líneas) y los 10 `.mjs` de `assets/` | Node: lanzan un Chrome sin interfaz y un servidor de archivos local, y `ffmpeg` si existe | Servidor en `127.0.0.1`; `icons.mjs` descarga de `cdn.jsdelivr.net`; `photos.mjs` busca y descarga en Wikimedia Commons; `assets/components/fx-map/bake.mjs` consulta la API Overpass de OpenStreetMap (`overpass-api.de` y `overpass.kumi.systems`); el comprobador pide las URLs de la página que revisa | Escriben en `.taste-skill/` del proyecto y en el directorio temporal | **Se quedan**. Revisados por superficie (red, procesos y borrados), no línea a línea |
| taste-skill | `install.sh` | Enlaza las skills en `~/.claude` | Ninguna | Escribe en el directorio personal | **No se copia** |
| design-motion | — | Nada: solo Markdown | Ninguna | Ninguno | Sin hooks, scripts ni MCP |
| privacy-legal | `.mcp.json` | Servidores MCP remotos | `mcp.slack.com` y `drivemcp.googleapis.com` | OAuth de Slack y de Google Drive | **Quitado** |
| privacy-legal | `hooks/hooks.json` | Nada (vacío) | — | — | **Quitado** |
| ai-governance-legal | `.mcp.json` | Servidores MCP remotos | Slack y Google Drive | OAuth | **Quitado** |
| product-legal | `.mcp.json` | Servidores MCP remotos | Slack, Google Drive, Linear, Atlassian y Asana | OAuth | **Quitado** |
| product-legal | `hooks/hooks.json` | Nada (vacío) | — | — | **Quitado** |
| product-legal | `agents/launch-watcher.md` | Agente programado | Los conectores quitados | `mcp__jira__*`, `mcp__linear__*` y `mcp__*__slack_send_message` | **Quitado** |
| commercial-legal | `.mcp.json` | Servidores MCP remotos | Ironclad, DocuSign, iManage, TopCounsel, Definely, Slack y Google Drive | OAuth | **Quitado** |
| commercial-legal | `hooks/hooks.json` | Nada (vacío) | — | — | **Quitado** |
| commercial-legal | `agents/` (`renewal-watcher`, `deal-debrief` y `playbook-monitor`) | Agentes programados | Los conectores quitados | Envío de mensajes por Slack y lectura por cualquier MCP conectado | **Quitados** |
| Los cuatro de legal | Skills | Solo instrucciones | Ninguna | Guardan el perfil de práctica y los asuntos en `~/.claude/plugins/config/claude-for-legal/` | **Se quedan** |

Lo que esta revisión no cubre:

- El contenido de las skills es texto que entra como instrucciones en el contexto de Claude. Se leyó buscando órdenes de instalar, descargar o tocar la configuración, no palabra por palabra.
- `superpowers` añade a cada sesión su texto de arranque, que pide usar sus skills antes de responder. Las instrucciones del repositorio (`CLAUDE.md`) mandan sobre él, y la propia skill lo dice.
- `taste-skill` trae logotipos de marcas de terceros entre sus iconos. No se usan para copiar la identidad visual de nadie.

## Referencias

Repositorios que se consultan pero **no se instalan ni se copian enteros**.

Cómo se consultan: `git clone --depth 1` a una carpeta temporal fuera del repositorio de trabajo, solo lectura, sin ejecutar sus scripts.

| Referencia | Commit | Regla de uso |
| --- | --- | --- |
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | `fcc70284932276d085f01ef9f83edde90b1258cb` | Solo para estudiar cómo documentan su diseño otras marcas. Nunca para copiar la identidad visual de una marca. |
| [DavidHDev/react-bits](https://github.com/DavidHDev/react-bits) | `9d9c687dc4f55b23539aa5417b703078047efa74` | Para copiar componentes concretos a `packages/ui` cuando se necesiten, adaptados a nuestros tokens. Licencia MIT + Commons Clause: usarlos en el producto, sí; redistribuir o vender la librería, no. En cada PR que lo use se anota de qué componente sale. |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | `be2a406907dbc61b73e6827ded415c96139d13a2` | Catálogo para buscar ideas. El repositorio no tiene licencia en la raíz: se comprueba la de cada skill antes de copiarla. No se instala nada de él. |

## Versiones

Cada estado revisado de `main` queda en una rama de versión, `release/vX.Y.Z`, que no recibe más commits. Quien usa el toolkit se fija a una, y pasar a la siguiente es un cambio en su propio repositorio, con su propia revisión.

| Versión | Qué trae |
| --- | --- |
| `release/v1.0.0` | Los 9 plugins de la revisión del 2026-11-10. Su contenido es el del commit `f43124b59943642b00eab6403a83ba3f333d7666`; después solo cambió este README. |

Son ramas y no etiquetas porque la sesión que montó el repositorio no puede empujar etiquetas. Una etiqueta sirve igual como `ref`.

Una rama de versión la puede mover quien tenga permiso de escritura en este repositorio. Protegerlas (y proteger `main`) se hace en los ajustes del repositorio en GitHub: una regla para `release/*` que impida empujar y borrar.

## Cómo se actualiza un plugin

1. Clona el origen con `git clone --depth 1` en una carpeta temporal fuera de este repositorio. No ejecutes sus scripts ni instaladores.
2. Revisa cada hook (`hooks/hooks.json` y el frontmatter de cada `SKILL.md` y de cada agente), cada script y cada `.mcp.json`: qué ejecuta, a qué red llama y qué permisos pide. Lo que no haga falta, fuera.
3. Copia solo lo revisado. Actualiza `UPSTREAM.md` y las tablas de este README con el commit nuevo y la fecha.
4. Si el origen no cambia su `version` en `plugin.json`, cámbiala tú: quien ya tiene el plugin instalado no recibe la copia nueva mientras la versión sea la misma.
5. `claude plugin validate .` y, por plugin, `claude --plugin-dir plugins/<nombre> plugin details <nombre>`: el inventario debe decir los hooks y servidores MCP que esperas.
6. PR con la tabla de la revisión.
7. Tras el merge, una rama de versión nueva sobre ese commit de `main` (ver «Versiones»). Una rama de versión no recibe más commits ni se reutiliza.
8. En cada repositorio que use el toolkit, un PR que cambie `ref` a la versión nueva. Hasta entonces sigue con la anterior.
