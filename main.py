from pyrogram import Client, filters
from pyrogram.types import Message
import config, os

ALLOWED_EXTENSIONS = ['.zip', '.rar']
user_data = {}

app = Client("renamer_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.document)
async def recibir_archivo(client, message: Message):
    doc = message.document
    ext = os.path.splitext(doc.file_name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        await message.reply("❌ Solo se permiten archivos .zip o .rar")
        return

    user_id = message.from_user.id
    user_data[user_id] = {"file_id": doc.file_id, "file_name": doc.file_name}

    await message.reply("📸 Ahora envíame la imagen que quieres usar como portada.")

@app.on_message(filters.photo)
async def recibir_portada(client, message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.reply("❗ Primero envíame un archivo .zip o .rar.")
        return

    photo_id = message.photo.file_id
    user_data[user_id]["photo_id"] = photo_id

    await message.reply("✏️ Ahora dime el nuevo nombre que tendrá el archivo (sin la extensión).")

@app.on_message(filters.text & ~filters.command(["start"]))
async def recibir_nombre(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_data or "photo_id" not in user_data[user_id]:
        return

    new_name = message.text.strip()
    file_ext = os.path.splitext(user_data[user_id]["file_name"])[1]
    new_file_name = new_name + file_ext

    await message.reply_document(
        document=user_data[user_id]["file_id"],
        caption=f"✅ Aquí tienes tu archivo renombrado a: `{new_file_name}`",
        thumb=user_data[user_id]["photo_id"],
    )

    await message.reply("🎉 Subido correctamente. ¡Gracias por usar el bot!")
    user_data.pop(user_id, None)

app.run()