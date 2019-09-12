from  . import  api
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from flask import  g,current_app,jsonify,request

@api.route("/users/avatar",methods=["POST"])
@login_required
def set_user_avatar():
    user_id = g.user_id

    image_file= request.files.get("avatar")

    if image_file is None:
        return jsonify(errno=RET.THIRDERR,errmsg="未上传图片")
    image_data =  image_file.read()
    #暂时保存到本地
    image_data.save()


