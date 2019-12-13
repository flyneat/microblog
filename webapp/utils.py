from werkzeug.security import generate_password_hash as generate_pwd_hash
from werkzeug.security import check_password_hash as check_pwd_hash
import json
from flask import request

'''
    args = request.args -> GET方法请求参数
    values = request.values -> GET方法请求参数 + GET/POST方法body里面的上送参数（包含form表单）
    form = request.form -> 获取所有参数
    json = request.json -> 获取dict形式的json数据
    data = request.data -> 获取bytes形式的数据
    file = request.file -> 获取上传的文件
'''


def resp_json(retcode=-1, retmsg='未知异常'):
    resp = {'retCode': retcode, 'retMsg': retmsg}
    return json.dumps(resp, ensure_ascii=False)


def resp_succ():
    return resp_json(0, '')


def get_req_data() -> bytes:
    return request.data


def get_req_stream():
    return request.stream


def get_req_text() -> str:
    data = request.data.decode()
    print('请求数据: ' + data)
    return data


def get_req_json() -> json:
    if request.is_json:
        return request.json
    else:
        try:
            return json.loads(request.data)
        except Exception as e:
            print(f'Json序列化异常，原因：{e}')
            raise e


def get_req_args() -> dict:
    return request.args


def get_req_values() -> dict:
    return request.values


def get_req_form() -> dict:
    return request.form


def get_req_files():
    return request.files


def get_http_method() -> str:
    return request.method
