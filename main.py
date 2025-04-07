from telethon import TelegramClient, events
from datetime import datetime
import json

# 🔐 Дані для входу
api_id = 28590491
api_hash = '7fc871ece8ef5d680f3cb6421515f7ab'
channel = 'https://t.me/air_alert_ua'

# ⚠️ Ключові слова для тривоги та відбою
key_words = ["Повітряна тривога в", "Тривога в", "Відбій тривоги в", "Відбій повітряной тривоги в"]

# 🗂️ Файл збереження
json_file = 'alerts.json'

# 🔄 Ініціалізація
client = TelegramClient("alerts_session", api_id, api_hash)

# 🧠 Завантаження існуючих даних
try:
    with open(json_file, 'r') as f:
        alerts_data = json.load(f)
except FileNotFoundError:
    alerts_data = []

# 📩 Обробник нових повідомлень
@client.on(events.NewMessage(chats=channel))
async def handler(event):
    message_text = event.message.message
    now = datetime.utcnow().isoformat()

    for keyword in key_words:
        if keyword in message_text:
            # Витягуємо основне повідомлення (перший рядок, з емодзі)
            clean_message = message_text.split("\n")[0].split("#")[0].strip()

            # Виділяємо регіон: усе, що після ключового слова, до кінця першого рядка
            region_line = clean_message.replace(keyword, "").strip().rstrip(".")

            entry = {
                "time": now,
                "region": region_line,
                "message": clean_message
            }

            alerts_data.append(entry)
            print(f"[{now}] 🔔 {clean_message}")

            # 🔒 Збереження в файл
            with open(json_file, 'w') as f:
                json.dump(alerts_data, f, indent=2, ensure_ascii=False)
            break

# 🛰️ Початок слухання каналу
print("🛰️ Слухаємо канал... (Ctrl+C щоб зупинити)")
client.start()
client.run_until_disconnected()
