from flask import Flask, request, jsonify, render_template, Response, render_template
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datetime import datetime, timedelta
import random
import requests
from questions import questions
import os

app = Flask(__name__)
CORS(app)

os.environ["HF_TOKEN"] = "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"
# cache_dir="/mnt/nas7/m11215117/earthquake_app/cache"

# 加載模型
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        "taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", 
        cache_dir="./cache",
        token=os.getenv("HF_TOKEN")
    )
    model = AutoModelForCausalLM.from_pretrained(
        "taide/Llama3-TAIDE-LX-8B-Chat-Alpha1",
        cache_dir="./cache",
        token=os.getenv("HF_TOKEN"),
        device_map="balanced", # balanced or auto
        trust_remote_code=True,
        low_cpu_mem_usage=True
    )
    return tokenizer, model

tokenizer, model = load_model()

# 使用模型生成回應
def generate_response(user_input):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # 添加提示文字，確保只回答問題
    prompt = f"回答用戶的問題：{user_input}\n回答："
    
    # 準備輸入並生成 attention_mask
    inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(device)
    attention_mask = inputs["attention_mask"]
    
    # 明確傳遞 attention_mask 和 pad_token_id
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=attention_mask,
        max_length=500,
        pad_token_id=tokenizer.eos_token_id
    )
    
    # 解碼生成的回應
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
    return response_text

# 地震通知數據
def get_recent_earthquake_notifications():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
        "minmagnitude": 3  # 設定地震最小震級
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        taiwan_notifications = [
            {
                "date": datetime.fromtimestamp(feature["properties"]["time"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                "message": f"{feature['properties']['place']} 發生 {feature['properties']['mag']} 級地震"
            }
            for feature in data["features"]
            if "Taiwan" in feature["properties"]["place"]
        ]
        return taiwan_notifications
    else:
        return [{"date": "N/A", "message": "無法獲取地震數據"}]

# 路由：地震通知
@app.route('/earthquake_notifications', methods=['GET'])
def earthquake_notifications():
    notifications = get_recent_earthquake_notifications()
    return jsonify(notifications)

# 路由：加載地震模擬問答的題目
@app.route('/load_game_question', methods=['GET'])
def load_game_question():
    question = random.choice(questions)
    return jsonify({
        "question": question["question"],
        "options": [{"text": option, "value": chr(65 + i)} for i, option in enumerate(question["options"])],
        "answer": question["answer"]
    })

# 路由：檢查答案是否正確
@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    user_answer = data.get("userAnswer")
    question_text = data.get("question")
    
    # 找到問題並檢查答案
    correct_answer = next((q["answer"] for q in questions if q["question"] == question_text), None)
    if correct_answer:
        is_correct = user_answer == correct_answer
        return jsonify({"correct": is_correct, "correctAnswer": correct_answer})
    else:
        return jsonify({"error": "無法找到問題"}), 400

# 流式生成回應
@app.route('/ask_taide', methods=['POST'])
def ask_taide():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        taide_response = "你好，很高興為您服務！我是TAIDE，是您現在的地震互動機器人助手，請問您有什麼關於地震的問題需要問我嗎？我會盡我所能為您解惑～"
        return jsonify({"response": taide_response})

    def generate_stream():
        inputs = tokenizer(user_message, return_tensors="pt").to(model.device)
        for output in model.generate(inputs.input_ids, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id, do_sample=True, top_k=50):
            response_text = tokenizer.decode(output, skip_special_tokens=True)
            yield f"data: {response_text}\n\n"
    
    return Response(generate_stream(), mimetype="text/event-stream")

# @app.route("/")
# def home():
#     return render_template("index.html")

# 主頁（包含前端界面）
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)