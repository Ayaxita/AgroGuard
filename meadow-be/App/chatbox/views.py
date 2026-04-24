from flask import Blueprint, jsonify, request, Response
from zhipuai import ZhipuAI
import json

chatbox = Blueprint('chatbox', __name__)

ZHIPU_API_KEY = "c22e75ec763e4b7183a3eb24e3232c76.MOHB0b4CS5wZS6Zs"

MODEL_MAP = {
    "GLM-4.7-Flash": "glm-4-flash",
    "GLM-4.6V": "glm-4v"
}

DEFAULT_MODEL = "glm-4-flash"


@chatbox.route('/chatbox/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    model_type = data.get('model_type', 'GLM-4.7-Flash')

    if not message:
        return jsonify({"code": 400, "msg": "消息不能为空"})

    model = MODEL_MAP.get(model_type, DEFAULT_MODEL)
    client = ZhipuAI(api_key=ZHIPU_API_KEY)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=True
        )

        def generate():
            full_content = ""
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_content += content
                    yield content

            print(f"【智谱AI对话完成】使用模型: {model}")

        return Response(generate(), content_type='text/event-stream; charset=utf-8')

    except Exception as e:
        print(f"智谱AI调用错误: {str(e)}")
        return jsonify({"code": 500, "msg": f"智谱AI调用失败: {str(e)}"})


@chatbox.route('/chatbox/models', methods=['GET'])
def list_models():
    return jsonify({
        "code": 200,
        "data": {
            "models": [
                {"id": "GLM-4.7-Flash", "name": "GLM-4.7-Flash", "description": "免费使用"},
                {"id": "GLM-4.6V", "name": "GLM-4.6V", "description": "最新版本"}
            ]
        },
        "msg": "success"
    })


@chatbox.route('/chatbox/getWsToken', methods=['GET'])
def get_ws_token():
    return jsonify({
        "code": 200,
        "data": {
            "apiResponse": {
                "Token": "zhipu-no-token-needed",
                "InputLenLimit": 3000
            }
        },
        "msg": "智谱AI无需WsToken"
    })