from webapp import app, db
from webapp.models import Instruction, PostFile
from webapp.constants import RetCode

from webapp.utils import json, get_req_data, resp_json, resp_succ, get_req_args, get_req_json, get_req_files, \
    get_req_form


@app.route("/api/postfile/add", methods=['POST'])
def add_postfile():
    files = get_req_files()
    form = get_req_form()
    sn = form.get('sn')

    up_file_len = len(files)
    if up_file_len < 1:
        return resp_json(RetCode.ValueError, "未上传文件")
    else:
        from webapp.utils import save_upfile as save
        if up_file_len == 1:
            fs = files.get('file')
            succ, file_info = save(fs)
            if not succ:
                return resp_json(RetCode.FILE_SAVE_ERROR, f'文件{fs.filename}保存失败')
            file_info.setdefault('sn', sn)
            succ = save_upfile_info(file_info)
            if not succ:
                return resp_json(RetCode.DB_ADD_ERROR, '上传保存文件信息失败')
            return resp_succ()
        else:
            # 多文件上传处理
            fail_info = []
            for i in range(1, up_file_len + 1):
                fs = files.get('file' + str(i))
                succ, file_info = save(fs)
                if succ:
                    file_info.setdefault('sn', sn)
                    succ1 = save_upfile_info(file_info)
                    if not succ1:
                        fail_info.append({
                            "seq_no": i,
                            'name': fs.filename,
                            'reason': '文件信息保存失败'
                        })
                        # 文件保存成功，但文件信息未保存成功，所以需要删除已保存的文件
                        save_path = file_info.get('path')
                        from os import remove as delfile
                        delfile(save_path)
                else:
                    # return resp_json(RetCode.FILE_SAVE_ERROR, f'文件{i}:{fs.filename}保存失败')
                    fail_info.append({
                        "seq_no": i,
                        'name': fs.filename,
                        'reason': '文件保存失败'
                    })
            fail_times = len(fail_info)
            succ_times = up_file_len - fail_times
            if fail_times > 0:
                tip = {
                    'retCode': RetCode.FILE_SAVE_ERROR,
                    'retMsg': f'共上传{up_file_len}个文件，成功{succ_times}个，失败{fail_times}个',
                    'sn': sn,
                    'detail': fail_info
                }
                return json.dumps(tip, ensure_ascii=False)
            else:
                return resp_succ()


def delete():
    pass


def update():
    pass


def query():
    pass


def save_upfile_info(fileinfo: dict):
    try:
        pf = PostFile(fileinfo)
        db.session.add(pf)
        db.session.commit()
    except Exception as e:
        print(f'保存上传文件信息失败，原因:{e}')
        return False
    return True
