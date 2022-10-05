import json
from flask import Flask, render_template, request
import pymysql
import datetime
import hashlib


def softdog(pwd):
    SALE = pwd[:4]
    md = hashlib.md5(pwd.encode())
    # md.hexdigest()
    md_sale = hashlib.md5((pwd+SALE).encode())
    str(pwd).join(SALE)
    return md_sale.hexdigest()


myhost = "127.0.0.1"
myport = 3306
myuser = 'root'
mypasswd = '011103'
mydb = 'treehole'


def gettime():
    d = datetime.datetime.today()
    year_t = d.strftime('%Y')
    month_t = d.strftime('%m')
    day_t = d.strftime('%d')
    hour_t = d.strftime('%H')
    minute_t = d.strftime('%M')
    second_t = d.strftime('%S')
    mes = year_t+month_t+day_t+hour_t+minute_t+second_t
    return mes


def gettime2():
    d = datetime.datetime.today()
    year_t = d.strftime('%Y')
    month_t = d.strftime('%m')
    day_t = d.strftime('%d')
    hour_t = d.strftime('%H')
    minute_t = d.strftime('%M')

    mes = year_t+'-'+month_t+'-'+day_t+' '+hour_t+':'+minute_t
    return mes


app = Flask(__name__)

level_list = ['0', '普通', '中级', '高级', '铜牌', '银牌', '金牌', '王牌']
level_dict = {'1': '普通', '2': '中级', '3': '高级',
              '4': '铜牌', '5': '银牌', '6': '金牌', '7': '王牌'}


@app.route('/index')
def index():
    conn = pymysql.connect(host="127.0.0.1", port=myport, user=myuser,
                           passwd=mypasswd, charset='utf8', db=mydb)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from clerk_info")
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    data_list_new = [value for value in data_list if value['isnew'] == '1']
    data_list_t_girl = []
    data_list_t_boy = []
    for data in data_list:
        if data['sexy'] == '男':
            data_list_t_boy.append(data)
        elif data['sexy'] == '女':
            data_list_t_girl.append(data)

    data_list_t_boy = sorted(
        data_list_t_boy, key=lambda x: (int(x['level'])), reverse=1)
    data_list_t_girl = sorted(
        data_list_t_girl, key=lambda x: (int(x['level'])), reverse=1)
    boy_len = len(data_list_t_boy)
    girl_len = len(data_list_t_girl)
    null_dict = {'imgurl': ''}
    if boy_len < 3:
        for i in range(3-boy_len):
            data_list_t_boy.append(null_dict)
    elif boy_len > 3:
        data_list_t_boy = data_list_t_boy[:3]

    if girl_len < 3:
        for i in range(3-girl_len):
            data_list_t_girl.append(null_dict)
    elif boy_len > 3:
        data_list_t_boy = data_list_t_boy[:3]

    data_list_b = sorted(data_list, key=lambda x: (
        int(x['level'])+int(x['isonline'])*10), reverse=1)
    print(data_list_b)
    # print(data_list_t_boy)
    # print(data_list_t_girl)
    return render_template('test.html', data_list_new=data_list_new, data_list_t_boy=json.dumps(data_list_t_boy), data_list_t_girl=json.dumps(data_list_t_girl), data_list_b=data_list_b, level_dict=level_dict)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        info = request.form
        username = info.get('username')
        sexy = info.get('sexy')
        age = info.get('age')
        wxid = info.get('wxid')
        tel = info.get('tel')
        area = info.get('area')

        img1 = request.files.get('inimg1')
        img2 = request.files.get('inimg2')
        img3 = request.files.get('inimg3')
        img4 = request.files.get('inimg4')

        aptime = gettime()
        aptime2 = gettime2()
        mdtime = softdog(aptime)
        imgurl = mdtime
        img1.save("static/images/apply/"+mdtime+"-1.jpg")
        img2.save("static/images/apply/"+mdtime+"-2.jpg")
        img3.save("static/images/apply/"+mdtime+"-3.jpg")
        img4.save("static/images/apply/"+mdtime+"-4.jpg")
        # file = info.get('file')
        introduction = info.get('introduction')

        conn = pymysql.connect(host=myhost, port=myport, user=myuser,
                               passwd=mypasswd, charset='utf8', db=mydb)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into apply_info(username,sexy,age,wxid,tel,area,introduction,aptime,imgurl,aptime2) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, [username, sexy, age,
                       wxid, tel, area, introduction, aptime, imgurl, aptime2])
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("register.html")


@app.route('/check')
def check():
    conn = pymysql.connect(host=myhost, port=myport, user=myuser,
                           passwd=mypasswd, charset='utf8', db=mydb)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from apply_info")
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('check.html', data_list=data_list)


@app.route('/check_detail')
def check_detail():
    info = request.args
    print(info)
    id = int(info.get('id'))-1
    conn = pymysql.connect(host=myhost, port=myport, user=myuser,
                           passwd=mypasswd, charset='utf8', db=mydb)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from apply_info")
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    print(data_list[id])
    return render_template('check_detail.html', data_list=data_list[id])


@app.route('/check_success', methods=['GET', 'POST'])
def check_success():
    if request.method == 'POST':
        isclerk = request.form.get('isclerk')
        id = int(request.form.get('id'))
        if isclerk in ["1", "2"]:
            info = request.form
            conn = pymysql.connect(host=myhost, port=myport, user=myuser,
                                   passwd=mypasswd, charset='utf8', db=mydb)

            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(
                "update apply_info set isclerk=%s where id=%s", [isclerk, str(id)])
            conn.commit()

            if isclerk == "1":
                cursor.execute("select * from apply_info")
                data_list = cursor.fetchall()

                data_list = data_list[id-1]
                username = data_list['username']
                wxid = data_list['wxid']
                sexy = data_list['sexy']
                age = data_list['age']
                tel = data_list['tel']
                area = data_list['area']
                imgurl = data_list['imgurl']
                retime = gettime()
                sql = "insert into clerk_info(username,wxid,sexy,age,tel,retime,area,imgurl) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(
                    sql, [username, wxid, sexy, age, tel, retime, area, imgurl])
                conn.commit()
                cursor.close()
                conn.close()
                for i in range(1, 5):
                    from_path = 'static/images/apply/'+imgurl+'-'+str(i)+'.jpg'
                    to_path = 'static/images/clerk/'+imgurl+'-'+str(i)+'.jpg'
                    f1 = open(from_path, 'rb')
                    temp_data = f1.read()
                    f1.close()
                    f2 = open(to_path, 'wb')
                    f2.write(temp_data)
                    f2.close()
        return render_template('check_success.html', isclerk=isclerk)


@app.route("/setprice")
def setprice():
    conn = pymysql.connect(host=myhost, port=myport, user=myuser,
                           passwd=mypasswd, charset='utf8', db=mydb)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('select * from price')
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    type_list = ['w30min', 'w60min', 'w1day', 'w7day', 'w1month', 'y30min',
                 'y60min', 'y1day', 'y7day', 'y1month', 'm1day', 'm3day', 'm7day']
    return render_template("setprice.html", data_list=data_list, type_list=type_list)


@app.route("/setprice_success", methods=['GET', 'POST'])
def setprice_success():
    if request.method == 'POST':
        info = request.form
        conn = pymysql.connect(host=myhost, port=myport, user=myuser,
                               passwd=mypasswd, charset='utf8', db=mydb)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        for i in range(1, 8):

            w1 = info.get(str(i)+'w30min')
            w2 = info.get(str(i)+'w60min')
            w3 = info.get(str(i)+'w1day')
            w4 = info.get(str(i)+'w7day')
            w5 = info.get(str(i)+'w1month')
            y1 = info.get(str(i)+'y30min')
            y2 = info.get(str(i)+'y60min')
            y3 = info.get(str(i)+'y1day')
            y4 = info.get(str(i)+'y7day')
            y5 = info.get(str(i)+'y1month')
            m1 = info.get(str(i)+'m1day')
            m2 = info.get(str(i)+'m3day')
            m3 = info.get(str(i)+'m7day')

            sql = "update price set w30min=%s,w60min=%s,w1day=%s,w7day=%s,w1month=%s,y30min=%s,y60min=%s,y1day=%s,y7day=%s,y1month=%s,m1day=%s,m3day=%s,m7day=%s where level=%s"
            cursor.execute(
                sql, [w1, w2, w3, w4, w5, y1, y2, y3, y4, y5, m1, m2, m3, str(i)])
            conn.commit()
        cursor.close()
        conn.close()
        return render_template("setprice_success.html")


@app.route('/setclerk')
def setclerk():
    conn = pymysql.connect(host="127.0.0.1", port=myport, user=myuser,
                           passwd=mypasswd, charset='utf8', db=mydb)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from clerk_info")
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    type_list = ['id', 'username', 'level', 'isonline', 'isnew', 'wxid', 'sexy', 'age',
                 'tel', 'area', 'retime', 'service', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5']
    return render_template('setclerk.html', data_list=json.dumps(data_list), type_list=json.dumps(type_list))


@app.route("/setclerk_success", methods=['GET', 'POST'])
def setclerk_success():
    if request.method == 'POST':
        info = request.form
        conn = pymysql.connect(host=myhost, port=myport, user=myuser,
                               passwd=mypasswd, charset='utf8', db=mydb)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        num = int(info.get('num'))
        for i in range(1, num+1):
            id = info.get(str(i)+'id')

            username = info.get(str(i)+'username')
            level = info.get(str(i)+'level')
            isonline = info.get(str(i)+'isonline')
            isnew = info.get(str(i)+'isnew')
            wxid = info.get(str(i)+'wxid')
            sexy = info.get(str(i)+'sexy')
            age = info.get(str(i)+'age')
            tel = info.get(str(i)+'tel')
            area = info.get(str(i)+'area')
            retime = info.get(str(i)+'retime')
            service = info.get(str(i)+'service')
            tag1 = info.get(str(i)+'tag1')
            tag2 = info.get(str(i)+'tag2')
            tag3 = info.get(str(i)+'tag3')
            tag4 = info.get(str(i)+'tag4')
            tag5 = info.get(str(i)+'tag5')
            # print([username, level, isonline, isnew, wxid, sexy, age, tel,
            #       area, retime, service, tag1, tag2, tag3, tag4, tag5, id])
            sql = "update clerk_info set username=%s,level=%s,isonline=%s,isnew=%s,wxid=%s,sexy=%s,age=%s,tel=%s,area=%s,retime=%s,service=%s,tag1=%s,tag2=%s,tag3=%s,tag4=%s,tag5=%s where id=%s"
            cursor.execute(
                sql, [username, level, isonline, isnew, wxid, sexy, age, tel, area, retime, service, tag1, tag2, tag3, tag4, tag5, id])
            conn.commit()
        cursor.close()
        conn.close()
        return render_template("setclerk_success.html")


@app.route('/test_detail')
def test_detail():
    id = int(request.args.get('id'))

    conn = pymysql.connect(host="127.0.0.1", port=myport, user=myuser,
                           passwd=mypasswd, charset='utf8', db=mydb)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from clerk_info")
    data_list = cursor.fetchall()
    data_dict = data_list[id-1]

    cursor.execute("select * from price")
    price_list = cursor.fetchall()
    price_dict = price_list[int(data_dict['level'])-1]
    cursor.close()
    conn.close()

    return render_template('test_detail.html', data_dict=data_dict, price_dict=price_dict)


if __name__ == "__main__":
    app.run(port=3070)
