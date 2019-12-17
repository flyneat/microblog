from webapp import app, db
from webapp.models import Instruction
from webapp.constants import *
from webapp.utils import json, get_req_data, resp_json, resp_succ, get_req_args, get_http_method, get_req_json
from datetime import datetime


# todo: 增加身份认证机制，保护api不被未经权限地访问


@app.route('/api/instruction/add', methods=['POST'])
def add_instruction():
    req_json = get_req_json()
    sn = req_json.get('sn')
    if not sn:
        return resp_json(RetCode.EMPTY_ARG, 'sn为空')
    user_id = req_json.get('user_id')
    if not user_id:
        return resp_json(RetCode.EMPTY_ARG, 'user_id为空')
    content = req_json.get('content')
    if not content:
        return resp_json(RetCode.EMPTY_ARG, 'content为空')

    try:
        insts = Instruction(sn=sn, user_id=user_id, content=json.dumps(content))
        db.session.add(insts)
        db.session.commit()
    except Exception as e:
        print(f'添加指令失败，原因：{e}')
        return resp_json(RetCode.DB_ADD_ERROR, '添加指令失败')
    else:
        return resp_succ()


@app.route('/api/instruction/del', methods=['POST'])
def delete_instruction():
    # todo: 后面优化删除逻辑，目前只使用id作为删除条件
    req_json = get_req_json()
    id = req_json.get('id')
    if not id:
        return resp_json(RetCode.EMPTY_ARG, 'id为空')
    try:
        result = db.session.execute('delete from instruction where id=:id', {'id': id})
        db.session.commit()
        if result.rowcount != 1:
            return resp_json(RetCode.RES_NOT_EXIST, '指令不存在')
    except Exception as e:
        print(f'删除指令（id = {id}）出现异常，原因：{e}')
        return resp_json(RetCode.DB_DEL_ERROR, '删除指令失败')
    else:
        return resp_succ()


@app.route('/api/instruction/upd', methods=['POST'])
def update_instruction():
    # 手动更新指令接口，只允许更新state = 0(待执行)状态的指令
    try:
        json_data = get_req_json()
    except json.decoder.JSONDecodeError as error:
        print(f'json序列化异常，原因:【{error}】')
        return resp_json(RetCode.JSON_ENCODE_ERROR, 'json序列化异常')

    id = json_data.get('id')
    if not id:
        return resp_json(RetCode.EMPTY_ARG, 'id为空')
    upd = []
    params = {}
    sn = json_data.get('sn')
    content = json_data.get('content')
    user_id = json_data.get('user_id')
    print(f'user_id = {user_id}')
    if not sn and not content and not user_id:
        return resp_json(RetCode.EMPTY_ARG, 'sn,content,user_id为空')
    else:
        if sn:
            upd.append('sn=:sn')
            params.setdefault('sn', sn)
        if content:
            upd.append('content=:content')
            params.setdefault('content', json.dumps(content, ensure_ascii=False))
        if user_id:
            upd.append('user_id=:user_id')
            params.setdefault('user_id', user_id)
    upd.append('timestamp=:upd_time WHERE id=:id AND state = 0')
    upd_time = datetime.utcnow()  # 记录修改时间
    params.setdefault('upd_time', upd_time)
    params.setdefault('id', id)
    upd_sql = 'UPDATE instruction SET ' + ','.join(upd)

    try:
        result = db.session.execute(upd_sql, params)
        db.session.commit()
        if result.rowcount != 1:
            return resp_json(RetCode.RES_NOT_EXIST, '指令不存在')
    except Exception as e:
        print(f'更新指令（id = {id}）出现异常，原因：{e}')
        return resp_json(RetCode.DB_UPD_ERROR, '更新指令失败')
    else:
        return resp_succ()


from ..utils import query_by_page
@app.route('/api/instruction/query', methods=['GET', 'POST'])
def query_instruction():
    http_method = get_http_method().upper()
    if http_method == 'GET':
        # 默认分页查询
        return query_by_page(Instruction)
    else:
        # todo: 条件查询
        return resp_json(RetCode.OK, '条件查询功能待实现')

