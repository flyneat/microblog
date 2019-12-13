import json
import os

from flask import request
from werkzeug.datastructures import FileStorage

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


def samefile(src, dst):
    # Macintosh, Unix.
    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False

    # All other platforms: check for same pathname.
    return (os.path.normcase(os.path.abspath(src)) ==
            os.path.normcase(os.path.abspath(dst)))


def save_upfile(fs: FileStorage) -> (bool, dict):
    """
    :return 保存是否成功，文件信息
    """
    filename = fs.filename
    file_type = 'unknown'
    dot_index = filename.rfind('.')
    from webapp.constants import POST_FILE_DIR, os

    # 默认文件存储在"./post_file"路径下
    if not os.path.exists(POST_FILE_DIR):
        os.makedirs(POST_FILE_DIR)
    save_path = POST_FILE_DIR
    if dot_index != -1:
        # 文件需要进行分类存储
        from webapp.constants import FILE_TYPE_MAP
        t = filename[dot_index + 1:]
        file_type = t
        for category, types in FILE_TYPE_MAP.items():
            if t in types:
                file_type = category
                save_path = '/'.join([POST_FILE_DIR, category])
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                break
    # todo: 相同文件检测

    # if os.path.exists(samefile()) and os.path.isfile(save_path):
    #     src_size = os.path.getsize(save_path)
    #     if src_size != 0 and src_size == length:

    try:
        buffer_size = 100 * 1024  # 每次读取100KB的数据来保存
        file_path = save_path + f'/{filename}'
        print('文件保存路径：' + file_path)
        fs.save(file_path, buffer_size)
        file_length = os.path.getsize(file_path)
        file_info = {
            'name': filename,
            'type': file_type,
            'length': file_length,
            'path': file_path
        }
        return True, file_info
    except Exception as e:
        print(f'写文件失败，原因:{e}')
        return False, None
    finally:
        fs.close()
