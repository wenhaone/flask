from  . import  api
from  flask import  request,jsonify,current_app,session
from ihome.utils.response_code import RET
from ihome import redis_store,db,constants
from ihome.models import User

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash
import re

@api.route("/users",methods=["POST"])
def register():
    """注册
    请求的参数：手机号、短信验证码、密码
    参数格式：json

    """
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")

    #校验参数
    if not  all([mobile,sms_code,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    #判断手机号格式
    if not re.match(r"1[34578]\d{9}",mobile):
        return jsonify(errno=RET.PARAMERR,errmsg="手机号格式不对")
    if password !=password2:
        return jsonify(errno=RET.PARAMERR,errmsg="两次输入密码不一致")
    #从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s"% mobile)
    except Exception as  e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="读取真是验证码失败")

    #判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(errno=RET.DATAERR,errmsg="验证码已失效")

    #判断用户的手机号是否注册过
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     current_app.logger.error(errno=RET.DATAERR,errmsg="手机号已经注册过")
    #
    #保存用户的注册数据到数据库中
    user = User(name=mobile,mobile=mobile)
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        #数据库错误后的回滚
        db.session.rollback()
        #表示手机号出现了重复值，手机号已经注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="手机号已存在")
    except Exception as e :
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据库异常")
    #保存登录状态到session中

    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"]= user.id
    #返回结果
    return jsonify(errno=RET.OK,errmsg="注册成功")

@api.route("/sessions",methods=["POST"])
def login():
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    #校验参数
    #参数完整的校验
    #
    if not all([mobile,password]):
        return jsonify(errno=RET.DATAEXIST,errmsg="数据不完整")
    #手机号格式
    if not re.match(r"1[34578]\d{9}",mobile):
        return jsonify(errno=RET.DATAEXIST,errmsg="手机号格式不对")
    #判断错误次数是否超过限制，如果超过限制，则返回
    #redis记录 “access_nums_请求的ip”：次数
    user_ip = request.remote_addr #用户的IP地址
    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR,errmsg="错误数过多，请稍后重试")
    #从数据库中根据手机号查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.REQERR,errmsg="获取用户信息失败")
    #用数据库的密码与用户填写的密码进行对比验证：
    if user is None or not user.check_password(password):
        #验证失败，记录错误次数，返回信息
        try:
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s"% user_ip,constants.LOGIN_ERROR_FORBID_TIME )
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.DATAERR,errmsg="用户名或者密码错误")
    #如果验证成功
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id

    return  jsonify(errno=RET.OK,errmsg="登陆成功")

@api.route("/session",methods=["GET"])
def check_login():
    """检查登录状态"""
    #尝试从session中获取用户的名字
    name =session.get("name")
    #如果session中数据name名字存在，则表示用户已登录
    if name is not None:
        return jsonify(error=RET.OK,errmsg="true",data={"name":name})
    else:
        return jsonify(error=RET.SESSIONERR,errmsg="false")

@api.route("/session",methods=["DELETE"])
def logout():
    session.clear()
    return jsonify(error=RET.OK,errmsg="OK")



