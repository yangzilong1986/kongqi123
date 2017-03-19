# coding:utf-8


def run_www(port=8000):
    port = int(port)
    from web.www.views import create_app
    app = create_app()
    app.run('0.0.0.0', port=port, debug=True)
    '''
    try:

    except Exception, e:
        print e.message
    '''


if __name__ == '__main__':
    from web.runhelp import main

    main(__file__, __name__)
