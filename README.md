# skills

Skills para [Claude Code](https://claude.com/claude-code) y otros agentes que leen `SKILL.md`.

| Skill | Qué hace | Uso |
|---|---|---|
| [`prompt-retro`](prompt-retro/SKILL.md) | Revisa tus mensajes de la sesión y muestra cómo escribirlos mejor. Solo marca los que costaron turnos o retrabajo, y separa lo que fue culpa del prompt de lo que fue del agente o del contexto. | `/prompt-retro` al cerrar una sesión |

## Instalación

Para todos tus proyectos:

```bash
git clone https://github.com/shadownrx/skills.git ~/code/skills
ln -s ~/code/skills/prompt-retro ~/.claude/skills/prompt-retro
```

Para un solo repo, copiá la carpeta a `.claude/skills/` de ese repo.

Después abrí una sesión nueva y escribí `/prompt-retro`.
