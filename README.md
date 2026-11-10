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

En el `.claude/settings.json` del repositorio que lo quiera:

```json
{
  "extraKnownMarketplaces": {
    "moodly-toolkit": {
      "source": { "source": "github", "repo": "dsvmotion/moodly-toolkit" }
    }
  },
  "enabledPlugins": {
    "superpowers@moodly-toolkit": true
  }
}
```

- **En el terminal o en la app de escritorio:** al confiar en la carpeta, Claude Code registra el marketplace. Cada persona instala después cada plugin una vez por clon: `claude plugin install <plugin>@moodly-toolkit --scope project`.
- **En una sesión en la nube** (claude.ai/code): hoy no se instalan los plugins que un repositorio activa en su `.claude/settings.json` ([documentación](https://code.claude.com/docs/en/cloud-environments#what-carries-over-from-your-setup)). Allí solo cargan los plugins de la cuenta de claude.ai y los de la configuración gestionada de la organización.
- Este repositorio es público: no hacen falta credenciales para instalarlo, y por eso mismo aquí no entra nada interno del proyecto.

## Revisión de seguridad (2026-11-10)

Se revisó cada hook, script y `.mcp.json` de los seis repositorios de origen antes de copiar nada. No se ejecutó ningún script ni instalador de terceros. Criterio:

- se quita lo que se ejecuta solo (hooks) salvo que sea inocuo y necesario;
- se quita lo que descarga y ejecuta binarios, y los servidores MCP de servicios que el proyecto no usa;
- los scripts que quedan solo corren cuando Claude los lanza con Bash, bajo los permisos de la sesión.

Tras la revisión, el marketplace entero tiene **un hook** (el `SessionStart` de `superpowers`) y **ningún servidor MCP**.

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
| taste-skill | `skills/taste-skill/scripts/*.mjs` (10 scripts, unas 17.000 líneas) y los `.mjs` de `assets/` | Node: lanzan un Chrome sin interfaz y un servidor de archivos local, y `ffmpeg` si existe | Servidor en `127.0.0.1`; `icons.mjs` descarga de `cdn.jsdelivr.net`; `photos.mjs` busca y descarga en Wikimedia Commons; el comprobador pide las URLs de la página que revisa | Escriben en `.taste-skill/` del proyecto y en el directorio temporal | **Se quedan**. Revisados por superficie (red, procesos y borrados), no línea a línea |
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

## Cómo se actualiza un plugin

1. Clona el origen con `git clone --depth 1` en una carpeta temporal fuera de este repositorio. No ejecutes sus scripts ni instaladores.
2. Revisa cada hook (`hooks/hooks.json` y el frontmatter de cada `SKILL.md` y de cada agente), cada script y cada `.mcp.json`: qué ejecuta, a qué red llama y qué permisos pide. Lo que no haga falta, fuera.
3. Copia solo lo revisado. Actualiza `UPSTREAM.md` y las tablas de este README con el commit nuevo y la fecha.
4. Si el origen no cambia su `version` en `plugin.json`, cámbiala tú: quien ya tiene el plugin instalado no recibe la copia nueva mientras la versión sea la misma.
5. `claude plugin validate .` y, por plugin, `claude --plugin-dir plugins/<nombre> plugin details <nombre>`: el inventario debe decir los hooks y servidores MCP que esperas.
6. PR con la tabla de la revisión.
