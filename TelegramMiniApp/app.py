from flask import Flask, render_template, request, jsonify
import asyncio
import aiohttp
from datetime import datetime

app = Flask(__name__)

# OpenRouter API
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Асинхронный вызов модели
async def async_generate_answer(question):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": [{"role": "user", "content": question}]
            }
            async with session.post(OPENROUTER_URL, headers=headers, json=data) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result['choices'][0]['message']['content']
                else:
                    return f"Ошибка API: {resp.status}"
    except Exception as e:
        return f"Ошибка сети: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    loop = asyncio.new_event_loop()
    question = request.form.get('question')
    if not question:
        return jsonify({'error': 'Вопрос не указан'}), 400

    answer = loop.run_until_complete(async_generate_answer(question))
    return jsonify({
        'answer': answer,
        'timestamp': datetime.now().strftime('%H:%M')
    })

if __name__ == '__main__':
    app.run(debug=True)