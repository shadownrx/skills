#!/usr/bin/env python3
"""Read the user's WhatsApp chats from the local WhatsApp Desktop database on macOS.

Every run reads a fresh snapshot, so the live database is never written or locked.
"""

import argparse
import os
import sqlite3
import sys
from datetime import datetime, timedelta

DB_PATH = os.path.expanduser(
    "~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite"
)
APPLE_EPOCH_OFFSET = 978307200  # seconds from 1970-01-01 to 2001-01-01 (Core Data dates)
DEFAULT_LIMIT = 50

# Labels for non-text messages; the caption, when present, follows the label.
MEDIA_LABELS = {
    1: "[image]",
    2: "[video]",
    3: "[audio]",
    7: "[link]",
    8: "[document]",
    15: "[sticker]",
}
SESSION_LABELS = {0: "direct", 1: "group", 2: "broadcast", 3: "status", 4: "community", 5: "channel"}


def open_snapshot():
    """Copy the live database (WAL included) into memory, so nothing is left on disk."""
    if not os.path.exists(DB_PATH):
        sys.exit(f"WhatsApp Desktop database not found: {DB_PATH}")
    source = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    target = sqlite3.connect(":memory:")
    source.backup(target)
    source.close()
    return target


def to_local(apple_seconds):
    """Convert a Core Data timestamp to a local 'YYYY-MM-DD HH:MM' string."""
    if apple_seconds is None:
        return "?"
    return datetime.fromtimestamp(apple_seconds + APPLE_EPOCH_OFFSET).strftime("%Y-%m-%d %H:%M")


def since_to_apple(since):
    """Turn '3d', '12h' or 'YYYY-MM-DD' into a Core Data timestamp."""
    if since[-1] in "dh" and since[:-1].isdigit():
        amount = int(since[:-1])
        delta = timedelta(days=amount) if since[-1] == "d" else timedelta(hours=amount)
        start = datetime.now() - delta
    else:
        start = datetime.strptime(since, "%Y-%m-%d")
    return start.timestamp() - APPLE_EPOCH_OFFSET


def find_chat(db, name):
    """Resolve a chat by exact name, then by unique partial match."""
    rows = db.execute(
        "SELECT Z_PK, ZPARTNERNAME FROM ZWACHATSESSION WHERE ZREMOVED = 0 AND ZPARTNERNAME LIKE ?"
        " ORDER BY ZLASTMESSAGEDATE DESC",
        (f"%{name}%",),
    ).fetchall()
    exact = [row for row in rows if row[1] and row[1].lower() == name.lower()]
    if len(exact) == 1:
        return exact[0]
    if len(rows) == 1:
        return rows[0]
    if not rows:
        sys.exit(f"No chat matches '{name}'. Run `chats {name[:3]}` to look for it.")
    names = "\n".join(f"  {row[1]}" for row in rows[:20])
    sys.exit(f"'{name}' matches {len(rows)} chats; repeat with the exact name:\n{names}")


MESSAGE_SELECT = """
SELECT m.ZMESSAGEDATE, m.ZISFROMME, m.ZMESSAGETYPE, m.ZTEXT, mi.ZTITLE,
       COALESCE(gm.ZCONTACTNAME, pn.ZPUSHNAME, m.ZPUSHNAME, gm.ZMEMBERJID, c.ZPARTNERNAME),
       c.ZPARTNERNAME
FROM ZWAMESSAGE m
JOIN ZWACHATSESSION c ON c.Z_PK = m.ZCHATSESSION
LEFT JOIN ZWAMEDIAITEM mi ON mi.Z_PK = m.ZMEDIAITEM
LEFT JOIN ZWAGROUPMEMBER gm ON gm.Z_PK = m.ZGROUPMEMBER
LEFT JOIN ZWAPROFILEPUSHNAME pn ON pn.ZJID = gm.ZMEMBERJID
"""


def message_body(kind, text, caption):
    """Render one message body; message kinds without a label show their type number."""
    if kind == 0:
        return text or ""
    label = MEDIA_LABELS.get(kind, f"[type {kind}]")
    detail = text or caption
    return f"{label} {detail}" if detail else label


def print_messages(rows, show_chat, limit):
    """Print messages oldest first, one per line, and flag a result cut by the limit."""
    if len(rows) == limit:
        print(f"(showing the latest {limit}; older messages exist, raise --limit or narrow --since)")
    for date, from_me, kind, text, caption, sender, chat in reversed(rows):
        author = "me" if from_me else sender
        prefix = f"[{chat}] " if show_chat else ""
        body = message_body(kind, text, caption).replace("\n", "\n    ")
        print(f"{to_local(date)} {prefix}{author}: {body}")


def cmd_chats(db, args):
    """List chats by most recent activity."""
    # Pinned chats store a far-future ZLASTMESSAGEDATE, so use the last message's real date.
    rows = db.execute(
        "SELECT c.ZPARTNERNAME, c.ZSESSIONTYPE, c.ZUNREADCOUNT,"
        " COALESCE(last.ZMESSAGEDATE, c.ZLASTMESSAGEDATE) AS last_date"
        " FROM ZWACHATSESSION c LEFT JOIN ZWAMESSAGE last ON last.Z_PK = c.ZLASTMESSAGE"
        " WHERE c.ZREMOVED = 0 AND c.ZPARTNERNAME LIKE ? ORDER BY last_date DESC LIMIT ?",
        (f"%{args.query or ''}%", args.limit),
    ).fetchall()
    for name, session_type, unread, last in rows:
        kind = SESSION_LABELS.get(session_type, f"type {session_type}")
        unread_note = f" ({unread} unread)" if unread else ""
        print(f"{to_local(last)}  [{kind}] {name}{unread_note}")


def cmd_read(db, args):
    """Print the latest messages of one chat."""
    chat_pk, _ = find_chat(db, args.chat)
    since = since_to_apple(args.since) if args.since else -1e12
    rows = db.execute(
        MESSAGE_SELECT + " WHERE c.Z_PK = ? AND m.ZMESSAGEDATE >= ?"
        " ORDER BY m.ZMESSAGEDATE DESC LIMIT ?",
        (chat_pk, since, args.limit),
    ).fetchall()
    print_messages(rows, show_chat=False, limit=args.limit)


def cmd_search(db, args):
    """Find messages whose text or caption contains the query."""
    since = since_to_apple(args.since) if args.since else -1e12
    pattern = f"%{args.query}%"
    rows = db.execute(
        MESSAGE_SELECT + " WHERE (m.ZTEXT LIKE ? OR mi.ZTITLE LIKE ?) AND m.ZMESSAGEDATE >= ?"
        " ORDER BY m.ZMESSAGEDATE DESC LIMIT ?",
        (pattern, pattern, since, args.limit),
    ).fetchall()
    print_messages(rows, show_chat=True, limit=args.limit)


def main():
    """Parse the command line and run one subcommand."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    chats = sub.add_parser("chats", help="list chats by recent activity")
    chats.add_argument("query", nargs="?", help="part of the chat name")
    chats.add_argument("--limit", type=int, default=30)
    chats.set_defaults(run=cmd_chats)

    read = sub.add_parser("read", help="latest messages of one chat")
    read.add_argument("chat", help="chat name, exact or a unique part")
    read.add_argument("--since", help="'3d', '12h' or 'YYYY-MM-DD'")
    read.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    read.set_defaults(run=cmd_read)

    search = sub.add_parser("search", help="messages containing a text, across chats")
    search.add_argument("query")
    search.add_argument("--since", help="'3d', '12h' or 'YYYY-MM-DD'")
    search.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    search.set_defaults(run=cmd_search)

    args = parser.parse_args()
    args.run(open_snapshot(), args)


if __name__ == "__main__":
    main()
