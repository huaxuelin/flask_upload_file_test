#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __Time__    : 2018/8/10
# __Author__  : "郁唯"

from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
import time
import os
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['pdf','docx','txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 用于测试上传，稍后用到
@app.route('/')
def upload_test():
    return render_template('upload.html')


# 上传文件
@app.route('/', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        token = base64.b64encode(new_filename.encode())
        print(token)

        return jsonify({"errno": 0, "errmsg": "上传成功", "token": token.decode()})
    else:
        return jsonify({"errno": 1001, "errmsg": "上传失败"})


if __name__ == '__main__':
    # app.run(debug=True)
    app.run("0.0.0.0",80,debug=True)
    # app.run("0.0.0.0",80,debug=True)