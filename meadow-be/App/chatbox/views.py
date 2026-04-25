import os

from flask import Blueprint, jsonify, request, Response
from zhipuai import ZhipuAI
import json
from App.chatbox.db_tools import TOOL_FUNCTION_MAP
from App.chatbox.tools_schema import TOOLS, SYSTEM_PROMPT

chatbox = Blueprint('chatbox', __name__)

ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")

MODEL_MAP = {
    "GLM-4.7-Flash": "glm-4-flash",
    "GLM-4.6V": "glm-4v"
}

DEFAULT_MODEL = "glm-4-flash"

MAX_TOOL_ROUNDS = 5


def _execute_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}
    try:
        func_args = json.loads(tool_call.function.arguments)
    except (json.JSONDecodeError, TypeError):
        func_args = {}
    func = TOOL_FUNCTION_MAP.get(func_name)
    if func is None:
        return {"error": f"未知工具: {func_name}"}
    try:
        result = func(**func_args)
        if isinstance(result, dict):
            return result
        return {"result": str(result)}
    except Exception as e:
        return {"error": f"工具执行出错: {str(e)}"}


@chatbox.route('/chatbox/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    model_type = data.get('model_type', 'GLM-4.7-Flash')
    history = data.get('history', [])

    if not message:
        return jsonify({"code": 400, "msg": "消息不能为空"})

    model = MODEL_MAP.get(model_type, DEFAULT_MODEL)
    client = ZhipuAI(api_key=ZHIPU_API_KEY)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in history:
        if h.get('role') in ('user', 'assistant') and h.get('content'):
            messages.append({"role": h['role'], "content": h['content']})
    messages.append({"role": "user", "content": message})

    try:
        tool_round = 0
        while tool_round < MAX_TOOL_ROUNDS:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=TOOLS,
                stream=False,
            )

            choice = response.choices[0]
            finish_reason = choice.finish_reason

            if finish_reason == "stop" or (not hasattr(choice, 'message') or not choice.message):
                break

            assistant_msg = choice.message

            if finish_reason == "tool_calls" and hasattr(assistant_msg, 'tool_calls') and assistant_msg.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": assistant_msg.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in assistant_msg.tool_calls
                    ]
                })

                for tool_call in assistant_msg.tool_calls:
                    tool_result = _execute_tool(tool_call)
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_result, ensure_ascii=False),
                        "tool_call_id": tool_call.id,
                    })
                tool_round += 1
            else:
                break

        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )

        def generate():
            full_content = ""
            for chunk in final_response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_content += content
                    yield content
            print(f"【智谱AI对话完成】使用模型: {model}, 工具调用轮次: {tool_round}")

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
