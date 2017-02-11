# coding:utf-8
"""
user forms
"""

import logging

import wtforms
from wtforms import Form, PasswordField, StringField, IntegerField, DecimalField, ValidationError
from wtforms import SubmitField

log = logging.getLogger('web')


class ImgCode(object):
    """
    验证码校验
    """
    field_flags = ('required',)

    def __init__(self, message=None):
        self.message = message
        import re
        self._reg = re.compile(ur'^[a-zA-Z0-9]+$')

    def __call__(self, form, field):
        data = field.data
        if not self._reg.match(data):
            # raise ValidationError(self.message or u"验证码格式错误")
            raise ValidationError(self.message)

        from flask import session
        print '验证码', session['code'], 'post:', data

        if session['code'].lower() != data.lower():
            raise ValidationError(u"验证码错误")


class NameValidater(object):
    """
    中文名校验
    """
    def __init__(self, message=None):
        self.message = message
        import re
        self._reg = re.compile(ur'^[a-zA-Z0-9\u4e00-\u9fa5 \.\-]+$')

    def __call__(self, form, field):
        data = field.data or ""
        if not self._reg.match(data):
            raise ValidationError(self.message or u"不能使用特殊符号")


class PasswordValidater(object):
    """
    密码校验（必须包含大写，小写，字母，特殊符号中三项）
    """
    def __init__(self, message=None):
        self.message = message
        import re
        self._num = re.compile('.*[0-9]+.*')
        self._upper = re.compile('.*[A-Z]+.*')
        self._lower = re.compile('.*[a-z]+.*')
        self._symbol = re.compile('.*[^a-z0-9A-Z]+.*')
    def __call__(self, form, field):
        # data = field.data
        # log.debug('data:%s'%data)
        # count = 0
        # if self._num.match(data):
        #     count += 1
        # if self._upper.match(data):
        #     count += 1
        # if self._lower.match(data):
        #     count += 1
        # if self._symbol.match(data):
        #     count += 1
        # if count < 3:
        #     raise ValidationError(self.message or u"密码强度不匹配,必须是8-18位密码,数字大小写字母以及符号组合")
        pass


class UserLoginForm(Form):
    """
    用户登录表单
    """
    username = StringField(u'用户名', [wtforms.validators.Length(min=5, max=20, message=u'请正确输入用户名'), NameValidater()])
    password = PasswordField(u'密码', [wtforms.validators.Length(min=5, max=20, message=u'请正确输入密码'), PasswordValidater()])

    submit = SubmitField(u'提交')


