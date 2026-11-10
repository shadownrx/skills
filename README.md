# skills

Skills para [Claude Code](https://claude.com/claude-code) y otros agentes que leen `SKILL.md`.

| Skill | Qué hace | Uso |
|---|---|---|
| [`prompt-retro`](prompt-retro/SKILL.md) | Revisa tus mensajes de la sesión y muestra cómo escribirlos mejor. Solo marca los que costaron turnos o retrabajo, y separa lo que fue culpa del prompt de lo que fue del agente o del contexto. | `/prompt-retro` al cerrar una sesión |
| [`prompt-coach`](prompt-coach/SKILL.md) | Mejora un prompt **antes** de mandarlo: lo reescribe con lo que encuentra en el contexto (repo, ticket, skills) y te pregunta solo lo que falta. No ejecuta la tarea. | `/prompt-coach arreglá el bug del checkout` |
| [`prompt-optimize`](prompt-optimize/SKILL.md) | Optimiza un prompt que tu app le manda a un modelo: menos tokens, sin ambigüedades, mismo contrato de salida. Compara el antes y el después con inputs reales antes de tocar el archivo. | `/prompt-optimize src/prompts/resumen.ts` |
| [`read-whatsapp`](read-whatsapp/SKILL.md) | Lee tus chats, grupos y canales de WhatsApp Desktop (macOS) desde la base local. Solo lee: trabaja sobre una copia y nunca envía. | "¿Qué dijeron hoy en el grupo X?" |
| [`stage-no-tests`](stage-no-tests/SKILL.md) | Hook que impide que el agente stagee tests: bloquea cualquier `git add` que incluiría un test. Los que stageás vos no se tocan. | Instalá el hook (ver la skill) |
| [`decisiones-tecnicas`](decisiones-tecnicas/SKILL.md) | Revisa las decisiones técnicas de la sesión, empezando por las de arquitectura, y explica cuál habría sido la mejor y por qué. | `/decisiones-tecnicas` al cerrar una sesión |
| [`roast-sesion`](roast-sesion/SKILL.md) | Un informe con humor sobre la sesión, con números reales: tareas, bugs propios, «listo» que no lo eran y el momento más irónico. | `/roast-sesion` |
| [`example`](example/SKILL.md) | Genera 10 versiones de una pantalla en un solo HTML, cada una con un patrón UX distinto, para comparar y elegir. | `/example checkout de un plan` |

## Cómo funciona una skill

Cada carpeta tiene un `SKILL.md`: un encabezado con `name` y `description`, y debajo las instrucciones que el agente sigue.

- **Las que llamás vos** (`disable-model-invocation: true`): solo corren cuando escribís `/nombre`. No ocupan contexto mientras no las usás. Son todas menos `read-whatsapp`.
- **Las que el agente usa solo**: el agente lee la `description` y la carga cuando tu pedido encaja. `read-whatsapp` se activa con "¿qué dijeron en el grupo X?".
- **Hooks**: una skill puede traer un script que Claude Code corre antes de cada comando. `stage-no-tests` funciona así, por eso no depende de que el agente se acuerde de la regla.

Lo que escribas después del comando (`/example checkout de un plan`) le llega a la skill como argumento.

## Las tres skills de prompts

Cada una cubre un momento distinto:

| Momento | Skill | Qué mejora |
|---|---|---|
| Antes de mandar un pedido | `/prompt-coach <borrador>` | Tu mensaje al agente |
| Al cerrar la sesión | `/prompt-retro` | Tus mensajes de la sesión, mirando lo que costaron |
| Cuando tu app llama a un modelo | `/prompt-optimize <archivo>` | El prompt que tu código le manda al LLM |

Todas usan los mismos criterios para un buen pedido:

- **Objetivo**: el resultado que querés, no solo la acción.
- **Ubicación**: dónde está la cosa (ticket, archivo, link, rama, repo).
- **Nombre**: el término que usa el proyecto.
- **Terminado**: cómo se sabe que está listo.
- **Límites**: alcance, restricciones y qué no tocar.

**`prompt-coach`**: completa con el contexto (repo, rama, ticket, skills disponibles) lo que se puede saber, y te pregunta hasta 3 cosas que no. Devuelve el prompt reescrito, listo para copiar, con una línea por cambio. No ejecuta la tarea. Si el borrador ya está bien, lo dice y para.

```
/prompt-coach necesito crear un sistema operativo
```

**`prompt-retro`**: elige los 1–3 mensajes que más turnos o retrabajo causaron y separa lo que fue culpa del prompt de lo que fue del agente o del contexto. Para cada uno muestra el original, qué faltaba, qué costó, la versión mejor y qué habría evitado. Cierra con un patrón reutilizable por cada problema real.

**`prompt-optimize`**: encuentra el prompt, el modelo, los parámetros y el código que lee la respuesta (ese código fija el formato de salida). Separa los hallazgos en **correcciones** (cambian el comportamiento) y **recortes** (menos tokens, mismo comportamiento), y propone un diff con los tokens antes y después. Después corre el prompt viejo y el nuevo con las mismas entradas reales. Si no puede correrlos, deja el plan de prueba y no afirma que mejora. No edita el archivo sin tu OK.

```
/prompt-optimize backend/services/knowledge_base_hints.py
```

## Las otras

**`decisiones-tecnicas`**: lista las decisiones técnicas de la sesión y las ordena por impacto, con arquitectura primero. Para cada una muestra las opciones que había en ese momento, cuál era la mejor y por qué, y si conviene cambiarla ahora, más adelante o nunca. Lo que solo se sabía después lo marca como aprendizaje, no como error.

**`example`**: lee el contexto (repo, tokens de diseño, rutas, plataforma) y genera un HTML con 10 versiones de una pantalla. Cada versión usa un patrón UX distinto y tiene la tarea principal funcionando, con animaciones y accesibilidad. Se cambia de versión con `1`–`0` o las flechas. Si nombrás un producto que no encuentra, pregunta dónde está antes de suponer.

**`roast-sesion`**: un informe con humor sobre la sesión. Cada número sale de la sesión real; no inventa nada.

**`read-whatsapp`**: copia la base de WhatsApp Desktop a memoria y la lee con `wa.py`: `chats`, `read --since`, `search`. Nunca escribe ni envía.

**`stage-no-tests`**: `guard.py` intercepta cada `git add` del agente, corre `git add --dry-run` y lo bloquea si incluiría un test (`tests/`, `test_*.py`, `*.test.ts`, `__snapshots__/`, etc.). Lo que stageás vos a mano no pasa por el hook.

## Instalación

Para todos tus proyectos:

```bash
git clone https://github.com/shadownrx/skills.git ~/code/skills
ln -s ~/code/skills/prompt-retro ~/.claude/skills/prompt-retro
ln -s ~/code/skills/prompt-coach ~/.claude/skills/prompt-coach
ln -s ~/code/skills/prompt-optimize ~/.claude/skills/prompt-optimize
ln -s ~/code/skills/read-whatsapp ~/.claude/skills/read-whatsapp
ln -s ~/code/skills/stage-no-tests ~/.claude/skills/stage-no-tests
ln -s ~/code/skills/decisiones-tecnicas ~/.claude/skills/decisiones-tecnicas
ln -s ~/code/skills/roast-sesion ~/.claude/skills/roast-sesion
ln -s ~/code/skills/example ~/.claude/skills/example
```

Para un solo repo, copiá la carpeta a `.claude/skills/` de ese repo.

Después abrí una sesión nueva. `read-whatsapp` necesita WhatsApp Desktop instalado y que la terminal tenga Acceso total al disco (Ajustes del Sistema → Privacidad y seguridad).
