import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ambil token dari Render environment variable
TOKEN = os.environ['BOT_TOKEN']
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"
colab_url = None  # Akan diisi guna /setcolab

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    requests.post(url, json={'chat_id': chat_id, 'text': text})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if 'message' not in data:
        return 'ok'

    msg = data['message']
    chat_id = msg['chat']['id']
    text = msg.get('text', '')

    if text == '/start':
        send_message(chat_id, "Jarvis Design bot ready. Guna /setcolab <url> untuk link Colab, kemudian /generate <prompt>")
    elif text.startswith('/setcolab'):
        global colab_url
        parts = text.split(' ', 1)
        if len(parts) == 2:
            colab_url = parts[1].strip('/')
            send_message(chat_id, f"✅ Colab URL diset ke: {colab_url}")
        else:
            send_message(chat_id, "Format: /setcolab https://xxxx.ngrok.io")
    elif text.startswith('/generate'):
        if not colab_url:
            send_message(chat_id, "Sila set Colab URL dulu guna /setcolab")
        else:
            prompt = text.split(' ', 1)[1] if ' ' in text else ''
            if not prompt:
                send_message(chat_id, "Sila beri prompt. Contoh: /generate kucing angkasa")
                return 'ok'

            # Hantar POST ke Colab
            try:
                resp = requests.post(f"{colab_url}/generate", json={'prompt': prompt}, timeout=120)
                if resp.status_code == 200:
                    data = resp.json()
                    img_url = data.get('image_url')
                    if img_url:
                        # Download gambar dan hantar ke Telegram
                        img_data = requests.get(img_url).content
                        requests.post(f"{TELEGRAM_API}/sendPhoto",
                                      files={'photo': ('result.png', img_data)},
                                      data={'chat_id': chat_id})
                    else:
                        send_message(chat_id, "Colab respon tapi tiada image_url.")
                else:
                    send_message(chat_id, f"Colab return error {resp.status_code}: {resp.text}")
            except Exception as e:
                send_message(chat_id, f"Gagal hubungi Colab: {str(e)}")
    else:
        send_message(chat_id, "Command tidak dikenali. Guna /start untuk bantuan.")

    return 'ok'

if __name__ == '__main__':
    # Auto-set webhook bila app mula
    render_url = os.environ.get('RENDER_EXTERNAL_URL')
    if render_url:
        webhook_url = f"{render_url}/webhook"
        requests.post(f"{TELEGRAM_API}/setWebhook", json={'url': webhook_url})
        print(f"Webhook set to {webhook_url}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
