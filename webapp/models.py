from datetime import datetime
from flask_login import UserMixin
import json
from . import db, login_manager
from .utils import gen_pwd_hash, check_pwd


class User(db.Model, UserMixin):
    """
     用户表
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True, unique=True)
    telno = db.Column(db.String(11), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    pwd_hash = db.Column(db.String(128))

    def __init__(self, name=None, telno=None, password=None) -> None:
        super().__init__()
        self.name = name
        self.telno = telno
        self.setpassword(password)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    insts = db.relationship('Instruction', backref='who', lazy='dynamic')

    def setpassword(self, pwd):
        hash = gen_pwd_hash(pwd)
        self.pwd_hash = hash

    def check_pwd(self, pwd):
        return check_pwd(pwd, self.pwd_hash)

    def __repr__(self) -> str:
        return f'User: {self.name}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Post: {self.body}'


class Instruction(db.Model):
    """
     指令表
    """

    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(20), index=True)

    '''
    最大支持一次指令取7条日志文件（json格式），示例如下：
    content:{
        "type":"log", 【文件类型】
        "dates":["20190912","20191123","20191210"] 【创建日期】
    }
    '''
    content = db.Column(db.String(200))

    # state{0：待执行（初始状态），1：执行成功（日志文件上传成功），2：执行中（过度状态）}
    state = db.Column(db.Integer, index=True, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 用户id，标识是谁发出的指令
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    postfiles = db.relationship('PostFile', backref='who', lazy='dynamic')

    # def __str__(self):
    #     ftuple = (self.id, self.sn, self.content, self.state, self.timestamp, self.user_id)
    #     return 'id":"%d","sn":"%s","content":"%s","state":"%d","timestamp":"%s","user_id":"%d"' % ftuple

    def dict(self) -> dict:
        return {
            "id": self.id,
            "sn": self.sn,
            "content": json.loads(self.content),
            "state": self.state,
            "timestamp": self.timestamp.__str__(),
            "user_id": self.user_id
        }

    def __repr__(self) -> str:
        return f'Instruction: sn:{self.sn}, content:{self.content}'

    def dict_form(self):
        return {
            "id": self.id,
            "sn": self.sn,
            "content": json.loads(self.content),
            "state": self.state,
            "timestamp": self.timestamp.__str__(),
            "user_id": self.user_id
        }


class PostFile(db.Model):
    """
     上传文件表
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    type = db.Column(db.String(10))  # 文件类型，如（txt,doc,img）
    length = db.Column(db.Integer, default=0)  # 文件大小(单位：byte)，理论上支持单文件最大4GB
    path = db.Column(db.String(1000))  # 文件存储路径
    uptime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 上传时间(UTC)
    sn = db.Column(db.String(20), index=True)

    insts_id = db.Column(db.Integer, db.ForeignKey('instruction.id'))  # 指令id

    def __init__(self, info: dict) -> None:
        super().__init__()
        for k, v in info.items():
            self.__setattr__(k, v)

    def __repr__(self) -> str:
        return f'name: {self.name}, length: {self.length}'

    def dict_form(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'length': self.length,
            'path': self.path,
            'uptime': self.uptime.__str__(),
            'sn': self.sn,
            'insts_id': self.insts_id
        }


@login_manager.user_loader
def load_user(id: str):
    return User.query.get(int(id))
