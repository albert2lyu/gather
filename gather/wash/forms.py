#!/usr/bin/python
#!-*- coding: utf-8 -*-

import datetime
import logging

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login

from account.models import LoginLog
from wash.models import WashUserProfile, VerifyCode, WashType, Discount
from utils import gen_info_msg, gen_photo_name
from qn import Qiniu

LOGIN_LOG = logging.getLogger('login')
INFO_LOG = logging.getLogger('info')


class RegistForm(forms.Form):
    """ 注册登录表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(RegistForm, self).__init__(*args, **kwargs)
        self._request = request

    phone = forms.CharField(label='手机号', max_length=11, widget=forms.TextInput(attrs={'placeholder': '请输入手机号', 'class': 'form-control'}), error_messages={'required': '请输入手机号'})
    code = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=False), error_messages={'required': '请输入验证码'})

    def clean_phone(self):

        phone = self.cleaned_data['phone']
        try:
            int(phone)
            if len(phone) != 11:
                raise ValueError
        except ValueError:
            raise forms.ValidationError('手机号格式错误')

        return self.cleaned_data['phone']

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            int(code)
            if len(code) != 4:
                raise ValueError
        except ValueError:
            raise forms.ValidationError('验证码格式错误!')

        return self.cleaned_data['code']

    def clean(self):
        if self.errors:
            return
        phone = self.cleaned_data['phone']
        code = self.cleaned_data['code']
        if not VerifyCode.code_expire(phone):
            if VerifyCode.code_valid(phone, code):
                if not WashUserProfile.objects.filter(phone=phone).exists():
                    user, created = User.objects.get_or_create(username=phone)
                    user.set_password("111111")
                    user.save()
                    WashUserProfile(user=user, phone=phone, is_phone_verified=True,
                                    phone_verified_date=datetime.datetime.now()).save()
            else:
                raise forms.ValidationError('验证码输入错误!')
        else:
            raise forms.ValidationError('验证码已过期,请重新获取!')

        return self.cleaned_data


class WashTypeForm(forms.ModelForm):
    """ 洗刷添加表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(WashTypeForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = WashType
        fields = ('name', 'new_price', 'old_price', 'mark', 'measure', 'belong')

    name = forms.CharField(label='名称', widget=forms.TextInput(attrs={'placeholder': '请输入名称'}), error_messages={'required': '请输入名称'})
    new_price = forms.CharField(label='现价', widget=forms.TextInput(attrs={'placeholder': '请输入现价'}), error_messages={'required': '请输入名称'})
    old_price = forms.CharField(label='旧价', widget=forms.TextInput(attrs={'placeholder': '请输入旧价'}), error_messages={'required': '请输入名称'})
    mark = forms.CharField(label='备注', initial='')
    measure = forms.ChoiceField(label=u'单位', choices=WashType.MEASURE, widget=forms.RadioSelect())
    belong = forms.ChoiceField(label=u'所属', choices=WashType.WASH_TYPE, widget=forms.RadioSelect())

    def clean(self):
        return self.cleaned_data

    def save(self, commit=True):
        m = super(WashTypeForm, self).save(commit=False)
        try:
            q = Qiniu()
            local_file = self._request.FILES['photo'].file
            image_name = gen_photo_name() + "." + self._request.FILES['photo']._name.encode('utf-8').split(".")[-1]
            q.upload_stream(image_name, local_file)
        except KeyError:
            image_name = m.photo

        m.photo = image_name
        m.save()


class DiscountForm(forms.ModelForm):
    """ 优惠券添加表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = Discount
        fields = ('name', 'price', 'begin', 'end', 'wash_type', 'discount_type')

    name = forms.CharField(label='名称', widget=forms.TextInput(attrs={'placeholder': '请输入名称'}), error_messages={'required': '请输入名称'})
    price = forms.CharField(label='优惠规格', widget=forms.TextInput(attrs={'placeholder': '输入优惠价格或者折扣'}), error_messages={'required': '请输入名称'})
    begin = forms.CharField(label='开始时间')
    begin = forms.CharField(label='结束时间')
    wash_type = forms.ChoiceField(label=u'优惠对象', choices=WashType.WASH_TYPE, widget=forms.RadioSelect())
    discount_type = forms.ChoiceField(label=u'优惠类型', choices=Discount.DISCOUNT_TYPE, widget=forms.RadioSelect())
