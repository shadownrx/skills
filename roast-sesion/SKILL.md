---
name: roast-sesion
description: "Roast the current session: a short, funny scorecard built from real numbers."
disable-model-invocation: true
---

The user wants a **roast** of the session: a comic scorecard of what the agent and the user actually did. The joke lands only when it is true, so every number and quote comes from the session.

## Steps

1. Read the session the user names (default: the current one) and count, with evidence:
   - **Tasks done**: requests that ended finished and verified.
   - **Bugs the agent introduced**: errors the agent caused and later had to fix (failed checks, wrong paths, reverted edits).
   - **"Listo" claims**: times the agent said it was done ("listo", "ahora sí", "funciona"), and how many of those held without a later fix.
   - **Detours**: searches in the wrong place, clarification rounds, retries.
   - **Scope**: files the change needed vs files it touched.

2. Score **utility** from 0 to 100: value delivered minus rework caused. Give the score one line of reason.

3. Pick the **award**: the most ironic real moment of the session, quoted or described exactly.

4. Write one **recommendation** for tomorrow, aimed at whoever caused the biggest cost (agent or user).

5. Output in the user's language with this shape. Drop a line whose number you cannot count.

```
🔥 Informe de inutilidad — <session topic>

Tareas resueltas: N
Bugs creados accidentalmente: N
Veces que dijo «listo»: N
Veces que realmente era «listo»: N
Desvíos: N

Nivel de utilidad: N/100 — <reason>

🏆 Premio de la sesión:
«<award>»

<recommendation>
```

The roast targets the work, never the person. Keep it under 15 lines.
