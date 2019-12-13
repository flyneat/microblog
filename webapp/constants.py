import os

DEFAULT_LIMIT = 10
DEFAULT_PAGE = 1

# APP_BASE_DIR = os.getcwd()
# DATA_DIR = APP_BASE_DIR + '/webapp/data'
DATA_DIR = './webapp/data'
# POST_FILE_DIR = APP_BASE_DIR + '/webapp/data/post_file'
POST_FILE_DIR = './webapp/data/post_file'

''' 默认的文件类型分类 '''
FILE_TYPE_MAP = {
    'doc': ('txt', 'pdf', 'doc', 'docx', 'xlsx', 'ppt'),
    'img': ('png', 'jpg', 'jpeg', 'gif'),
    'audio': ('mp3',),
    'video': ('mp4', 'flv', 'avi'),
    'log': ('log',)
}

class RetCode:
    """
    返回给客户端Json字符串retCode和retMsg定义：
        retCode                   retMsg
          0                    请求处理成功
         1XX                   客户端异常
         2XX                   服务器异常
         3XX                      超时
    ---------------------------------------------------
         100：未知异常，无法处理
         101：上传参数为空
         102：资源不存在

    ---------------------------------------------------
         200：未知异常，无法处理
         201：数据库【添加】操作出错
         202：数据库【删除】操作出错
         203：数据库【更新】操作出错
         204：数据库【查询】操作出错
         205：Json序列化异常
         206：Json反序列化异常
    """
    OK = 0

    CLIENT_EXCEPTION = 100
    EMPTY_ARG = 101
    RES_NOT_EXIST = 102
    ValueError = 103

    SERVER_EXCEPTION = 200
    DB_ADD_ERROR = 201
    DB_DEL_ERROR = 202
    DB_UPD_ERROR = 203
    DB_QUERY_ERROR = 204
    JSON_ENCODE_ERROR = 205
    JSON_DECODE_ERROR = 206
    FILE_SAVE_ERROR = 207
