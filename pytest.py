from flask import Flask, render_template, request
import pymysql
import os
import sys
import random
import string

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


@app.route("/formtest", methods=['GET', 'POST'])
def test():

    # pic.save("static/img666.png")
    # if imageFile.content_type not in contentTypes:
    #     return HttpResponse('图片格式错误','请上传图片格式')
    # save_path = 'static/'+imageFile.name
    # print(save_path)
    # f = open(save_path, 'wb+')
    # f.write(imageFile.read())
    return render_template('formtest.html', data='1')
    # if request.method == 'GET':
    #     return render_template("test.html")
    # else:
    #     info = request.form
    #     # 生成随机字符串，防止图片名字重复
    #     ran_str = ''.join(random.sample(
    #         string.ascii_letters + string.digits, 16))
    #     # 获取图片文件 name = upload
    #     img = request.files.get('upload')
    #     # 定义一个图片存放的位置 存放在static下面
    #     path = basedir+"/static/img/"
    #     # 图片名称 给图片重命名 为了图片名称的唯一性
    #     imgName = ran_str+img.filename
    #     print(img.filename)
    #     # 图片path和名称组成图片的保存路径
    #     file_path = path+imgName
    #     # 保存图片
    #     img.save(file_path)
    #     # 这个是图片的访问路径，需返回前端（可有可无）
    #     url = '/static/img/'+imgName
    #     # 返回图片路径 到前端

    #     conn = pymysql.connect(host="127.0.0.1", port=3306, user='root',
    #                            passwd='011103', charset='utf8', db='my_test')
    #     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #     sql = "insert into tb2(imgurl) values(%s)"
    #     cursor.execute(sql, [url])
    #     conn.commit()
    #     cursor.close()
    #     conn.close()
    #     return render_template("test.html")


if __name__ == "__main__":
    app.run(port=3060)
