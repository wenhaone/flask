
from . import  api
from  ihome.utils.captcha.captcha import  captcha
from ihome import redis_store
from ihome import constants
from ihome import db
from ihome.models import User
from flask import current_app,jsonify,make_response,request
from ihome.utils.response_code import RET
from  ihome.libs.yuntongxun.sms import  CCP
import random
#127.0.0.1/api/v1.0/image_codes
#127.0.0.1/api/v1.0/image_codes/<image_code_id>

@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return: 正常返回：验证码图片 错误返回json
    """
    #获取参数
    #检验参数
    #业务逻辑处理
    #生成图片验证码，
    #名字 真实文本 图片数据
    name,text,image_data = captcha.generate_captcha()
    # 将验证码真实值保存到redis中
    #redis 是键值对数据库:字符串 键值对  列表 哈希 set 都是字符串
    #image_code : {"":""} 哈希：hset:{"":""} hget("image_code","id1")
    #选用字符串作为维护记录""
    #设置有效期 "image_code_编号1"："真实值"
    # redis_store.set("image_code_%s" % image_code_id,text)
    # redis_store.expire("image_code_%s" % image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES)
    #上面两步融合成一步
    try:
        redis_store.setex("image_code_%s" % image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        #记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="保存图片验证码信息失败")
    #返回值 返回图片  默认是：html/text
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
# GET /api/v1.0/sms_codes/<>?image_code=xxx&image_code
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""
    #获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    #校验参数是否完整
    if not all([image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    #业务逻辑处理
    #从redis中取出真是的图片验证码
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="redis lost connect")
    #判断图片验证码是否过期
    if real_image_code is None:
        return jsonify(errno=RET.NODATA,errmsg="图片验证码失效")
    #删除图片验证码，防止用户用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
    #与用户填写的值进行对比
    if real_image_code.decode('utf-8').lower() != image_code.lower():

        return jsonify(errno=RET.DATAERR,errmsg="图片验证码错误")
    #判断手机号是否发送过短信，在60s内有没有记录，如果有，则不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR,errmsg="请求过于频繁")
    #判断手机号是否存在，
    #db.session  如果不存在 django异常  flask返回none
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e :
        current_app.logger.error(e)
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST,errmsg="手机号已存在")
    #如果手机号不存在，则生成短信验证码
    sms_code = "%06d"% random.randint(0,999999)

    #保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s"% mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
    #保存发送给这个手机号的记录，防止用户在60s内再次发出短信的操作
        redis_store.setex("send_sms_code_%s"%mobile,constants.SEND_SMS_CODE_INTERVAL,1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="保存短信验证码异常")
    #发送短信
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile,[sms_code,int(constants.SMS_CODE_REDIS_EXPIRES/60) ],1)
    except Exception as  e:
        current_app.logger.error(e)
        print(e)
        return jsonify(errno=RET.THIRDERR, errmsg="发送短信验证码失败")
    if result == 0:
        return  jsonify(errno= RET.OK,errmsg="发送成功")
    else:
        return  jsonify(errno= RET.THIRDERR,errmeg="云通讯炸了")
    #返回值

