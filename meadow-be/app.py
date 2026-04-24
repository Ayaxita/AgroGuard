from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, verify_jwt_in_request

from App import create_app


app = create_app()


# 全局拦截器进行身份验证
@app.before_request
def before_request():
    path = request.path
    url = request.url
    suffix = url.endswith('.png') or url.endswith('.jpg') or url.endswith('.css') or url.endswith('.js')
    method = request.method
    passUrl = ['/login', '/register', '/logout', '/refresh', '/basic/basicinfo/import_template',
               '/basic/basicinfo/detail', '/login/test', '/w_information/immunizationMessage/index']
    # print(path, method, suffix)
    if method != 'OPTIONS':
        if path not in passUrl and not suffix:
            verify_jwt_in_request()
            username = get_jwt_identity()
            # print(url)
            # result = {
            #     "code": 200,
            #     "data": username,
            #     "msg": "验证成功"
            # }
    if request.method == 'POST' and request.path not in passUrl and request.content_type == 'application/json':
        if request.is_json:
            # 处理 JSON 数据
            data = request.get_json()
            if isinstance(data, list):
                pass
            else:
                # 去除 JSON 数据中所有字符串两端的空格
                for key, value in data.items():
                    if isinstance(value, str):
                        data[key] = value.strip()
                # 更新请求的 JSON 数据
                request._json = data
        elif request.form:
            # 处理表单数据
            if isinstance(request.form, list):
                pass
            else:
                for key, value in request.form.items():
                    if isinstance(value, str):
                        request.form[key] = value.strip()


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    accesstoken = create_access_token(identity=identity)
    print('刷新了')
    result = {
        "code": 200,
        "data": accesstoken,
        "msg": "刷新成功"
    }
    return jsonify(result)


if __name__ == '__main__':
    API_ADDR = '0.0.0.0'
    API_PORT = '5000'
    app.run(host=API_ADDR, port=API_PORT, debug=True)
