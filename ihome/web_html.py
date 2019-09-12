from flask import Blueprint,current_app,make_response
from flask_wtf import csrf
html = Blueprint("web_html",__name__)

#127.0.0.1:5000/
#127.0.0.1:5000/index.html
#127.0.0.1:5000/register.html


@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    """提供html文件"""
    #如果 html_file_name 为null  表示访问的是"/",请求的是主页


    if not html_file_name:
        html_file_name = "index.html"
    #如果资源名不是favicon.ico
    if html_file_name != "favicon.ico":
        html_file_name = "html/"+html_file_name

    #创建一个csrf_token值
    csrf_token = csrf.generate_csrf()

    #flask提供的返回静态文件的方法
    #make_response 设置响应对象
    resp = make_response(current_app.send_static_file(html_file_name))
    #设置cookie值  没设置有效期就是 有效期是浏览器关闭前
    resp.set_cookie("csrf_token",csrf_token)
    return resp