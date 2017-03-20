# coding:utf-8
from web.www import create_app
from web.www.views import app

# app = create_app()


def run_www(port=5000):
    port = int(port)
    app.run('0.0.0.0', port=port, debug=True)
    '''
    try:

    except Exception, e:
        print e.message
    '''


if __name__ == '__main__':
    from web.runhelp import main

    main(__file__, __name__)
