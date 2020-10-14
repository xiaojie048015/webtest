#coding=utf-8
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
import time,json
import os
from flask import  request
app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF','xmind'])

@app.route('/', methods=['GET', 'POST'])
def home():
    return (render_template('index.html'))

@app.route('/signin', methods=['GET'])
def signin_form():
    return (render_template('loginpage.html'))

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='15902127953' and request.form['password']=='123456':
        return (render_template('welcomepage.html',username=request.form['username']))
    return (render_template('loginpage.html',message='用户名验证失败'))


# 用于测试上传，稍后用到
@app.route('/test/upload')
def upload_test():
    return render_template('upload.html')


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/api/huace/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['huace']  # 从表单的file字段获取文件，myfile为该表单的name值
    print(request.headers)
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        print('这是什么类型%s'%fname)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        return jsonify({"errno": "000", "success": "true", })
    else:
        return jsonify({"errno": "1001", "errmsg": "false"})

@app.route('/api/huace/login', methods=['POST'], strict_slashes=False)
def api_login():

        data=request.get_json()
        print('<Request> url= {url}, body= {body}'.format(url=request.url, body=json.dumps(data, ensure_ascii=False)))
        if data["username"]=="admin" and data["password"]=='123456':
            #return jsonify({"code": '000', "msg": "登录成功", "token":'werdzfgfdgdg',"info":{"name":"admin","age":"18"},"logintime":""})
            return  jsonify({
                          "httpstatus": 200,
                          "adress": {
                            "city": "changsha"
                          },
                            "info": {
                            "name": "admin",
                            "age":18
                          },
                          "msg": "success",
                          "token": "huacetest"
                        })
        else:
            return jsonify({"code": '001', "msg": "用户名或密码错误", })


@app.route('/api/huace/userList', methods=['GET'], strict_slashes=False)
def api_user():
        token = request.headers.get('Token')
        if token=='huacetest':
            return jsonify({"code": '000', "data": [{"name":"admin"},{"city":"changsha"}] })
        else:
            return jsonify({"code": '001', "msg": "用户未登录无权限访问", })


@app.route('/api/huace/userViplist', methods=['GET'], strict_slashes=False)
def api_vipuser():
        token = request.headers.get('Token')
        if token=='huacetest':
            return jsonify({"code": '000', "data": [{"name":"admin"},{"city":"changsha"}] })
        else:
            return jsonify({"code": '001', "msg": "用户未登录无权限访问", })


@app.route('/api/huace/userInfo', methods=['POST'], strict_slashes=False)
def api_userinfo():
        res=request.form.get('userid')
        if res:
            return jsonify({"code": '000', "data": [{"name":"admin"},{"userid":"001"}] })
@app.route('/api/huace/userDelete', methods=['DELETE'], strict_slashes=False)
def api_delate():
        return jsonify({"code": '000', "data": [{"name":"admin"},{"userid":"001"}] })

@app.route('/api/huace/demo', methods=['GET'], strict_slashes=False)
def api_demo():
        data=request.args.get('limit')
        if data=='1':
            return jsonify({"httpstatus": 200, "data": [{"from":"huace","name":"hello,zhiyilaoshi"}] })

        elif data=='2':
            return jsonify({"httpstatus": 200, "data": [{"from":"huace","name":"hello,zhiyilaoshi"},{"from":"huace","name":"hello,diandianlaoshi"}] })
        else:
            return jsonify({"httpstatus": 200, "data": [{"from":"huace","name":"hello,zhiyilaoshi"},{"from":"huace","name":"hello,diandianlaoshi"},{"from":"huace","name":"hello,zimolaoshi"}] })


# Base Auth认证  ["Basic","YWRtaW46YWRtaW4xMjM="]
import base64
@app.route('/api/huace/auth', methods=['GET', 'POST'])
def post_auth():
    if request.method == 'POST':
        auth = request.headers.get("Authorization")
        print(auth)
        if auth is None:
            return jsonify({"code": 10101, "message": "Authorization None"})
        else:
            auth = auth.split()
            auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
            print('加密',auth_parts)
            userid, password = auth_parts[0], auth_parts[2]
            if userid == "" or password == "":
                return jsonify({"code": 10102, "message": "Authorization null"})

            if userid == "admin" and password == "huace123456":
                data = request.get_json()
                if data["username"] == "admin" and data["password"] == '123456':

                    return jsonify({"code": 10200, "message": "Authorization success!","data":data})
                else:
                    return jsonify({"code": '001', "msg": "用户名或密码错误", })
            else:
                return jsonify({"code": 10103, "message": "Authorization fail!"})
    else:
        return jsonify({"code": 10101, "message": "request method error"})


if __name__ == '__main__':
    app.run(debug=True)


