from webapp import app, db
from ..models import Instruction, PostFile
from ..constants import RetCode, R_DATA_DIR

from ..utils import json, resp_json, resp_succ, get_req_args, get_req_json, get_req_files, \
    get_req_form, query_by_page


@app.route("/api/postfile/add", methods=['POST'])
def add_postfile():
    files = get_req_files()
    form = get_req_form()

    sn = form.get('sn')
    insts_id = form.get('insts_id')

    if not check_insts_valid(insts_id, sn):
        return resp_json(RetCode.INVALID_PARAMETER, f'指令id:{insts_id}, sn:{sn} 参数无效')

    up_file_len = len(files)
    if up_file_len < 1:
        return resp_json(RetCode.INVALID_PARAMETER, "未上传文件")
    else:
        from webapp.utils import save_upfile as save
        fail_info = []
        i = 1
        for fs in files.values():
            succ, file_info = save(fs)
            if succ:
                file_info.setdefault('sn', sn)
                file_info.setdefault('insts_id', insts_id)
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
            i += 1
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


@app.route('/api/postfile/query', methods=['GET'])
def postfile_query():
    return query_by_page(PostFile)


@app.route('/api/postfile/del', methods=['GET'])
def delete():
    args = get_req_args()
    id = args.get('id')
    if not id:
        return resp_json(RetCode.INVALID_PARAMETER, f'id为空')
    rowcount = db.session.execute('delete from post_file where id=:id', {'id': id}).rowcount
    if rowcount != 1:
        return resp_json(RetCode.DB_DEL_ERROR, f'删除上传文件失败，id = {id}')
    return resp_succ()


def update():
    """ 目前业务不支持修改上传文件信息 """
    pass


@app.route('/api/postfile/download', methods=['GET'])
def postfile_dl():
    """ 根据指令id下载对应的上传文件,返回一个zip格式压缩包 """
    args = get_req_args()
    insts_id = args.get('insts_id')
    if not insts_id:
        resp_json(RetCode.INVALID_PARAMETER, f'insts_id:{insts_id}参数无效')

    files = db.session.query(PostFile.path).filter(PostFile.insts_id == int(insts_id)).all()
    if len(files) < 1:
        return resp_json(RetCode.RES_NOT_EXIST, '文件不存在')

    from flask import make_response, send_file, send_from_directory
    from ..utils import zip_file
    paths = []
    import os
    for file in files:
        path = file.path
        if os.path.exists(path):
            paths.append(file.path)

    # name = os.path.basename(zip_path)
    name = get_zip_name()
    zip_path = '/'.join((R_DATA_DIR, name))
    print(f'压缩前，zip文件是否存在？{os.path.exists(zip_path)}')
    zip_file(zip_path, paths)

    zip_fp = open(zip_path, 'rb')
    print(f'压缩后，zip文件是否存在？{os.path.exists(zip_path)}')
    response = make_response(send_file(zip_fp, as_attachment=True, attachment_filename=f'{name}'))
    return response


def save_upfile_info(fileinfo: dict):
    try:
        pf = PostFile(fileinfo)
        db.session.add(pf)
        db.session.commit()
    except Exception as e:
        print(f'保存上传文件信息失败，原因:{e}')
        return False
    return True


def check_insts_valid(id, sn):
    """ 检查指令状态（是否有效）"""
    if not id or not sn:
        return False
    instruction = Instruction.query.filter(Instruction.id == id, Instruction.sn == sn).first()
    if not instruction:
        return False
    return True


def get_zip_name() -> str:
    import datetime
    dt = datetime.datetime.today()
    return dt.strftime('%Y%m%d%H%M%S%f')[0:18] + '.zip'

    # uuid实现
    # import uuid
    # return uuid.uuid1().hex
