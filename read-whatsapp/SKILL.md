---
name: read-whatsapp
description: "Read the user's WhatsApp chats, groups, and messages from the local WhatsApp Desktop app on macOS. Use when the user asks what a chat or group said, to find a message, or to summarize recent WhatsApp activity."
---

The user's WhatsApp Desktop keeps every chat in a local database. `wa.py` (next to this file) reads a fresh **snapshot** of it, so it only reads and never sends.

## Steps

1. Find the chat. Run `python3 <skill-dir>/wa.py chats <part of the name>`. When the user gives a nickname or no name, run `chats` with no query and match by recent activity.

2. Read it. Use `wa.py read "<exact chat name>" --since 3d`, or `--limit N` for the last N messages. To find a topic across chats, use `wa.py search "<text>" --since 7d`.

3. Answer from the messages. Quote the date, sender, and text when the user needs proof. Widen `--since` or `--limit` until the period the user asked about is fully covered.

## Reference

- Output: one line per message, oldest first: `YYYY-MM-DD HH:MM sender: text`. `me` is the user.
- Non-text messages show a label (`[image]`, `[audio]`, `[link]`…) plus the caption when there is one. `[type N]` is a kind with no label (system notices, reactions, deleted messages).
- Audio, images, and files are not transcribed or opened: say a message is media and what its caption says.
- The data stops at the last sync of WhatsApp Desktop. When the user expects newer messages, ask them to open the app.
- Chats are private: share in the answer only the messages the request needs.
