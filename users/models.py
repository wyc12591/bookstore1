from hashlib import sha1

from django.db import models

# Create your models here.
from db.base_model import BaseModel


def get_hash(str):
    """取一个字符串的hash值"""
    sh = sha1()
    sh.update(str.encode('utf8'))
    return sh.hexdigest()


class PassportManager(models.Manager):
    def add_one_passport(self, username, password, email):
        """添加一个账户信息"""
        passport = self.create(username=username, password=get_hash(password), email=email)
        # 返回passport
        return passport

    def get_one_passport(self, username, password):
        """根据用户名密码查找账户的信息"""
        try:
            passport = self.get(username=username, password=get_hash(password))
        except self.models.DoesNotExist:
            # 账户不存在
            passport = None
        return passport


class Passport(BaseModel):
    """用户模型类"""
    username = models.CharField(max_length=20, verbose_name='用户名称')
    password = models.CharField(max_length=40, verbose_name='用户密码')
    email = models.EmailField(verbose_name='用户邮箱')
    is_active = models.BooleanField(default=False, verbose_name='激活状态')

    objects = PassportManager()

    class Meta:
        db_table = 's_user_account'
