# skills

Skills para [Claude Code](https://claude.com/claude-code) y otros agentes que leen `SKILL.md`.

| Skill | Qué hace | Uso |
|---|---|---|
| [`prompt-retro`](prompt-retro/SKILL.md) | Revisa tus mensajes de la sesión y muestra cómo escribirlos mejor. Solo marca los que costaron turnos o retrabajo, y separa lo que fue culpa del prompt de lo que fue del agente o del contexto. | `/prompt-retro` al cerrar una sesión |
| [`read-whatsapp`](read-whatsapp/SKILL.md) | Lee tus chats, grupos y canales de WhatsApp Desktop (macOS) desde la base local. Solo lee: trabaja sobre una copia y nunca envía. | "¿Qué dijeron hoy en el grupo X?" |
| [`stage-no-tests`](stage-no-tests/SKILL.md) | Hook que impide que el agente stagee tests: bloquea cualquier `git add` que incluiría un test. Los que stageás vos no se tocan. | Instalá el hook (ver la skill) |
| [`decisiones-tecnicas`](decisiones-tecnicas/SKILL.md) | Revisa las decisiones técnicas de la sesión, empezando por las de arquitectura, y explica cuál habría sido la mejor y por qué. | `/decisiones-tecnicas` al cerrar una sesión |
| [`roast-sesion`](roast-sesion/SKILL.md) | Un informe con humor sobre la sesión, con números reales: tareas, bugs propios, «listo» que no lo eran y el momento más irónico. | `/roast-sesion` |

## Instalación

Para todos tus proyectos:

```bash
git clone https://github.com/shadownrx/skills.git ~/code/skills
ln -s ~/code/skills/prompt-retro ~/.claude/skills/prompt-retro
ln -s ~/code/skills/read-whatsapp ~/.claude/skills/read-whatsapp
ln -s ~/code/skills/stage-no-tests ~/.claude/skills/stage-no-tests
ln -s ~/code/skills/decisiones-tecnicas ~/.claude/skills/decisiones-tecnicas
ln -s ~/code/skills/roast-sesion ~/.claude/skills/roast-sesion
```

Para un solo repo, copiá la carpeta a `.claude/skills/` de ese repo.

Después abrí una sesión nueva. `read-whatsapp` necesita WhatsApp Desktop instalado y que la terminal tenga Acceso total al disco (Ajustes del Sistema → Privacidad y seguridad).
