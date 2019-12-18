import json
import os
import zipfile

from flask import request
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph

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
    from webapp.constants import R_POST_FILE_DIR, os

    # 默认文件存储在"./post_file"路径下（相对路径）
    if not os.path.exists(R_POST_FILE_DIR):
        os.makedirs(R_POST_FILE_DIR)
    save_path = R_POST_FILE_DIR
    if dot_index != -1:
        # 文件需要进行分类存储
        from webapp.constants import FILE_TYPE_MAP
        t = filename[dot_index + 1:]
        file_type = t
        for category, types in FILE_TYPE_MAP.items():
            if t in types:
                file_type = category
                save_path = '/'.join([R_POST_FILE_DIR, category])
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                break
    # todo: 相同文件检测

    # if os.path.exists(samefile()) and os.path.isfile(save_path):
    #     src_size = os.path.getsize(save_path)
    #     if src_size != 0 and src_size == length:

    try:
        buffer_size = 1024 * 1024  # 每次最多读取1MB的数据来保存
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


def zip_file(zip_path: str, paths: list):
    if len(paths) > 0:
        zfile = zipfile.ZipFile(file=zip_path, mode='a', compression=zipfile.ZIP_DEFLATED)
        for filepath in paths:
            filename = os.path.basename(filepath)
            zfile.write(filepath, arcname=filename)
        print('压缩zip文件结束')
        zfile.__repr__()
        zfile.close()
    pass


def query_by_page(model) -> json:
    """ 分页查询 """
    from .constants import DEFAULT_LIMIT, DEFAULT_PAGE, RetCode
    args = get_req_args()
    try:
        limit = DEFAULT_LIMIT
        lt = int(args.get('limit', -1))
        if lt > 0:
            limit = lt
    except ValueError as e:
        print(f'取limit参数出现异常，原因{e}')
        return resp_json(RetCode.EMPTY_ARG, f"limit = {args.get('limit')} 不是整数")
    try:
        page = DEFAULT_PAGE
        p = int(args.get('page', -1))
        if p > 0:
            page = p
    except ValueError as e:
        print(f'取page参数出现异常，原因{e}')
        return resp_json(RetCode.INVALID_PARAMETER, f"page = {args.get('page')} 不是整数")

    offset = (page - 1) * limit
    m_list = model.query.limit(limit).offset(offset).all()
    if not m_list:
        return resp_json(RetCode.RES_NOT_EXIST, '已到最后一页')

    model_list = []
    for m in m_list:
        # 把Instruction对象信息转为字典形式保持，方便json序列化
        model_list.append(m.dict_form())
    resp_data = {
        'retCode': 0,
        'retMsg': '',
        model.__tablename__: model_list
    }
    return json.dumps(resp_data, ensure_ascii=False)


def check_pwd(pwd, pwd_hash) -> bool:
    return cph(pwd_hash, pwd)


def gen_pwd_hash(pwd) -> str:
    return gph(pwd)
