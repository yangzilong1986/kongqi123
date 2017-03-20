#!/usr/bin/env python
# coding:utf-8

import os
from web.www.views import app
from flask_script import Manager, Shell

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

# 通过配置创建 app
# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def deploy():
    """Run deployment tasks."""
    pass


if __name__ == '__main__':
    manager.run()
