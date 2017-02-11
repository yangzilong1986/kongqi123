# coding:utf-8

import importlib


def run_help(f,m):
    '帮助'

    import inspect

    module = importlib.import_module(m)

    title = str(module.__doc__).strip()
    print title
    print '-'*len(title.decode('utf-8'))*2
    print(' python %s  <action>' % (f,))

    pos2 = 0
    for fun in vars(module):
        if fun[0:4] == 'run_':
            pos2 += 1

            print '%d. python %s  %s' % (pos2, f, fun[4:]),
            func = getattr(module, fun)
            doc = func.__doc__
            if doc is not None:

                for arg in inspect.getargspec(func).args:
                    print ' <%s>' % (arg,),
                print '\n   ', doc.strip()
            print
    print
    print


def main(f,mod):
    '入口'
    m = mod
    import sys
    import importlib

    if len(sys.argv) < 2:
        return run_help(f,m)

    action = 'run_' + sys.argv[1]

    args = []
    if len(sys.argv) >= 2:
        args = sys.argv[2:]

    module = importlib.import_module(m)

    if hasattr(module, action):
        return getattr(module, action)(*args)

    print "error action:", m, action
    run_help(f,m)


if __name__ == '__main__':
    main()

