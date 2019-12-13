from webapp import app, db
from webapp.models import Instruction, PostFile
from webapp.constants import *
from webapp.utils import json, get_req_data, resp_json, resp_succ, get_req_args, get_req_json, get_req_files, \
    get_req_form


@app.route("/api/postfile/add", methods=['POST'])
def add_postfile():
    files = get_req_files()
    form = get_req_form()
    sn = form.get('sn')
    fs = files.get('log')
    filename = fs.filename
    try:
        dst = open(f'./{filename}', 'wb')
        # read_len = 1024 * 1024 # 每次读取1MB的数据
        fs.save(dst)
    except Exception as e:
        print(f'写文件失败，原因:{e}')
        return resp_json(-1, '保存文件失败')
    else:
        return resp_succ()


def delete():
    pass


def update():
    pass


def query():
    pass
