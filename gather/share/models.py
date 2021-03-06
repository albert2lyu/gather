#!/usr/bin/python
#-*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Share(models.Model):
    """ 分享信息"""
    user = models.ForeignKey(User, related_name='shares')

    title = models.CharField('标题', max_length=250)
    photo = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField('分享的简介信息', blank=True, null=True)
    read_sum = models.IntegerField('点击次数', default=0)
    xsize = models.IntegerField('x长度', default=0)
    ysize = models.IntegerField('y长度', default=0)
   
    created = models.DateTimeField('创建时间', auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '分享信息'
        verbose_name_plural = '分享信息列表'

    def is_read(self):
        """ 是否已阅读"""
        return IsRead.objects.filter(share=self, is_active=True).exists()

    def can_show_desc(self):
        """ 能否显示简介"""
        if '<img' in self.content:
            return False
        else:
            return True

    def resize_photo(self):
        """ 重新设置展示大小"""
        if self.xsize > 600:
            return (600, 600 * self.ysize / self.xsize)

    def is_scroll(self):
        """ 是否需要滚轮"""
        if self.xsize > self.ysize:
            return False
        else:
            return True

    def article_short(self):
        return self.short(10)

    def image_short(self):
        return self.short(30)

    def short(self, length=10):
        if len(self.title) > length:
            return u"{}...".format(self.title[:length])
        else:
            return self.title

    def photo_url(self):
        return "http://7xkqb1.com1.z0.glb.clouddn.com/{}".format(self.photo)


class IsRead(models.Model):
    """ 是否已阅读"""
    user = models.ForeignKey(User, related_name='is_reads')
    share = models.ForeignKey(Share, related_name='shares')

    is_active = models.BooleanField('是否有效', default=False)

    created = models.DateTimeField('创建时间', auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '已查看信息'
        verbose_name_plural = '已查看信息列表'


class ip_proxy(models.Model):
    """ 代理IP"""
    ip = models.CharField('ip', max_length=250)
    port = models.IntegerField('端口', max_length=250)
    status = models.BooleanField('ip状态', max_length=250)
    succ_count = models.IntegerField('成功次数', max_length=250)
    fail_count = models.IntegerField('失败次数', max_length=250)
    created = models.DateTimeField('创建时间', null=True)

    class Meta:
        db_table = 'ip_proxy'

