from webapp import app, db
from webapp.models import User, Post, Instruction, PostFile

host = 'localhost'
port = 5000


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Instruction': Instruction, 'PostFile': PostFile}


if __name__ == '__main__':
    app.run(host, port)
