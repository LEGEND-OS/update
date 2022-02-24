""" command: .unzip
coded by @The_LegendBoy
code rewritten my SnapDragon7410
"""
import asyncio
import os
import time
import time as t
import zipfile
from datetime import datetime

from LEGENDBOT.utils import admin_cmd, edit_or_reply, sudo_cmd
from userbot.cmdhelp import CmdHelp

extracted = Config.TMP_DOWNLOAD_DIRECTORY + "extracted/"
thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@bot.on(admin_cmd(pattern="zip", outgoing=True))
@bot.on(sudo_cmd(pattern="zip", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await edit_or_reply(event, "Reply to a file to compress it. Bruh.")
        return
    mone = await edit_or_reply(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            directory_name = downloaded_file_name
            await edit_or_reply(event, downloaded_file_name)
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED).write(
        directory_name
    )
    await borg.send_file(
        event.chat_id,
        directory_name + ".zip",
        caption="**Zipped!**",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
    )
    await asyncio.sleep(7)
    await event.delete()


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))


@bot.on(admin_cmd(pattern="unzip", outgoing=True))
@bot.on(sudo_cmd(pattern="unzip", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await edit_or_reply(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            t.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                "Stored the zip to `{}` in {} seconds.".format(downloaded_file_name, ms)
            )

        with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
            zip_ref.extractall(extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        # filename = filename + "/"
        await edit_or_reply(event, "Unzipping now")
        # r=root, d=directories, f = files
        for single_file in filename:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                try:
                    await bot.send_file(
                        event.chat_id,
                        single_file,
                        caption=f"**Unzipped** `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=document_attributes,
                        # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        #     progress(d, t, event, c_time, "trying to upload")
                        # )
                    )
                except Exception as e:
                    await bot.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id,
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


CmdHelp("zipper").add_command(
    "zip", "<reply to media>", "Makes a zip file of replied media"
).add_command(
    "unzip",
    "<reply to a zip file>",
    "Unzips the replied zip file and sends the files from that zip file",
).add_command(
    "compress", "<reply to media>", "Compress the replied media"
).add()
