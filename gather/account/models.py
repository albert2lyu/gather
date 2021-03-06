#!/usr/bin/python
#-*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """ 用户注册信息"""
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    username = models.CharField('用户名', max_length=30, unique=True)
    nickname = models.CharField('昵称', max_length=30, null=True, blank=True)
    email = models.EmailField('email', max_length=100, null=True, blank=True)
    is_mail_verified = models.BooleanField('是否已经通过验证', default=False)
    mail_verified_date = models.DateTimeField('邮箱通过验证时间', blank=True, null=True)

    big_photo = models.ImageField(upload_to='head/%Y/%m/%d', blank=True, null=True)

    created = models.DateTimeField('创建时间', auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息列表'

    def __unicode__(self):
        return self.username

    def get_mask_username(self):
        # 用户名保密
        return self.username[:3] + "******" + '.com'

    def get_mask_email(self):
        # 邮箱保密
        try:
            return self.email[:3] + '****' + self.email[self.email.find('@'):]
        except:
            return None

    def is_special_care(self, care=None):
        """ 是否特别关心该用户"""
        result = SpecialCare.objects.filter(user=self.user, care=care, is_valid=True).exists()
        return result if result else False

    def is_self_action(self, obj_modal=None, obj_id=None):
        """ 是否是自己的状态"""
        return obj_modal.objects.filter(user=self.user, pk=obj_id).exists()

    def get_owner_photo(self):
        """ 获取状态所有者的头像"""
        try:
            return self.big_photo.url
        except:
            return '/static/images/default_head.png'


class LoginLog(models.Model):
    """ 用户登录信息"""
    username = models.CharField('用户名', max_length=30, blank=True, null=True, default='guest')
    login_ip = models.CharField('登录IP', max_length=40, blank=True, null=True)
    is_succ = models.BooleanField('登录是否成功', default=False)
    fail_reason = models.CharField('登录失败原因', max_length=100, blank=True, null=True)
    login_time = models.DateTimeField('登录时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户登录记录'
        verbose_name_plural = '用户登录记录列表'


class ClickLog(models.Model):
    """ 游客, 用户点击信息"""
    username = models.CharField('用户名', max_length=30, blank=True, null=True, default='guest')
    click_url = models.CharField('点击url', max_length=100, blank=True, null=True)
    remote_ip = models.CharField('来源ip', max_length=20, blank=True, null=True)
    click_time = models.DateTimeField('点击时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户点击信息'
        verbose_name_plural = '用户点击信息列表'


class SpecialCare(models.Model):
    """ 特别关心对应关系"""
    user = models.ForeignKey(User)
    care = models.ForeignKey(User, related_name='cares')

    is_valid = models.BooleanField('是否有效', default=False)

    created = models.DateTimeField('创建时间', auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '特别关心信息'
        verbose_name_plural = '特别关心列表'
