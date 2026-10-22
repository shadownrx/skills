# skills

Skills para [Claude Code](https://claude.com/claude-code) y otros agentes que leen `SKILL.md`.

| Skill | Qué hace | Uso |
|---|---|---|
| [`prompt-retro`](prompt-retro/SKILL.md) | Revisa tus mensajes de la sesión y muestra cómo escribirlos mejor. Solo marca los que costaron turnos o retrabajo, y separa lo que fue culpa del prompt de lo que fue del agente o del contexto. | `/prompt-retro` al cerrar una sesión |
| [`read-whatsapp`](read-whatsapp/SKILL.md) | Lee tus chats, grupos y canales de WhatsApp Desktop (macOS) desde la base local. Solo lee: trabaja sobre una copia y nunca envía. | "¿Qué dijeron hoy en el grupo X?" |
| [`stage-no-tests`](stage-no-tests/SKILL.md) | Al stagear para revisar o commitear, deja los tests sin stage. Avisa cuáles quedaron afuera, porque no entran en el commit. | Automático al stagear |

## Instalación

Para todos tus proyectos:

```bash
git clone https://github.com/shadownrx/skills.git ~/code/skills
ln -s ~/code/skills/prompt-retro ~/.claude/skills/prompt-retro
ln -s ~/code/skills/read-whatsapp ~/.claude/skills/read-whatsapp
ln -s ~/code/skills/stage-no-tests ~/.claude/skills/stage-no-tests
```

Para un solo repo, copiá la carpeta a `.claude/skills/` de ese repo.

Después abrí una sesión nueva. `read-whatsapp` necesita WhatsApp Desktop instalado y que la terminal tenga Acceso total al disco (Ajustes del Sistema → Privacidad y seguridad).
