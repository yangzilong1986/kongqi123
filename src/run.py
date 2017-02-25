# coding:utf-8


def run_www():
    from web.www.views import app
    app.run('0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    from web.runhelp import main

    main(__file__, __name__)
