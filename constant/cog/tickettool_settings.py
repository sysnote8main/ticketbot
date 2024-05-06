from discord import PermissionOverwrite

EVERYONE_PERM = PermissionOverwrite()
EVERYONE_PERM.send_messages=False
EVERYONE_PERM.read_messages=False

SENDER_PERM = PermissionOverwrite()
SENDER_PERM.send_messages=True
SENDER_PERM.read_messages=True