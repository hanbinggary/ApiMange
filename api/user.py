#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/4  上午10:16

from schema import user
from sanic import Blueprint
from core.status import FAIL
from core.response import resp_json
from core.token import generate_token

import models

from .base import GenericAPIView

bp = Blueprint('user', url_prefix='/api/user')


class RegisterView(GenericAPIView):
    """
    注册试图
    """
    model = models.UserInfo
    schema_class = user.RegisterSchema

    async def post(self, request):
        username = request.json.get("username", None)
        password = request.json.get("password", "")
        email = request.json.get("email", "")

        register_user = await models.UserInfo.filter(username=username).first()
        register_email = await models.UserInfo.filter(email=email).first()
        if register_user or register_email:
            return resp_json(FAIL, msg="用户已经存在")

        context = {
            "username": username,
            "password": password,
            "email": email
        }

        await models.UserInfo.create(**context)
        return resp_json(msg="用户注册成功！", body=context)


class LoginView(GenericAPIView):
    """
    登录
    """
    model = models.UserInfo
    schema_class = user.LoginSchema

    async def post(self, request):
        username = request.json.get("username", None)
        password = request.json.get("password", "")

        if not username and not password:
            return resp_json(FAIL, msg="用户名密码错误")

        user_obj = await models.UserInfo.filter(username=username).first()

        if username != user_obj.username:
            return resp_json(FAIL, msg="用户不存在")
        if password != user_obj.password:
            return resp_json(FAIL, msg="密码错误！")
        token = generate_token(username)
        body = {
            "username": username,
            "password": password,
            "token": token,
        }
        return resp_json(body=body)


bp.add_route(LoginView.as_view(), "/login/")
bp.add_route(RegisterView.as_view(), "/register/")
