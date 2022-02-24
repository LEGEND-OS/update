# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon.errors import rpcbaseerrors

from LEGENDBOT.utils import admin_cmd, errors_handler, sudo_cmd
from userbot import BOTLOG, BOTLOG_CHATID
from userbot import bot as LEGENDBOT


@LEGENDBOT.on(admin_cmd(outgoing=True, pattern="del$"))
@LEGENDBOT.on(sudo_cmd(allow_sudo=True, pattern="del$"))
@errors_handler
async def delete_it(safai):
    """For .del command, delete the replied message."""
    msg_src = await safai.get_reply_message()
    if safai.reply_to_msg_id:
        try:
            await msg_src.delete()
            await safai.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "#DEL \nDeletion of message was successful"
                )
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Well, I can't delete a message"
                )
