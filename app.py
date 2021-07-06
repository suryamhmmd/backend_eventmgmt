from flask import Flask, flash, render_template, json, request, redirect, url_for, session, send_from_directory
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mysqldb import MySQL,MySQLdb
from datetime import tzinfo, timedelta, datetime
import pandas as pd
import numpy as np
import mysql.connector
import random as rd
from random import randint
import matplotlib.pyplot as plt
from controller.first import cal_fitness, selection, crossover, mutation, optimize

app = Flask(__name__)
app.config['SECRET_KEY'] = '^A%DJAJU^JJ123'
app.config['MYSQL_HOST'] = 'haloryan.com'
app.config['MYSQL_USER'] = 'u6049187_surya'
app.config['MYSQL_PASSWORD'] = 'surya'
app.config['MYSQL_DB'] = 'u6049187_surya'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
json = FlaskJSON(app)

class FixedOffset(tzinfo):
    def __init__(self, offset):
        self.__offset = timedelta(hours=offset)
        self.__dst = timedelta(hours=offset-1)
        self.__name = ''

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return self.__dst

dt = datetime.now(FixedOffset(7))
tglnow = dt.strftime("%d")
blnnow = dt.strftime("%m")
thnow = dt.strftime("%Y")
datenow = tglnow+"/"+blnnow+"/"+thnow
timenow = dt.strftime("%X")
daynow = dt.strftime("%A")

@app.route('/')
def main():
    data = {
        'Apps':'Event management by Surya',
        'Version':'1.0.0',
        'Time':dt
    }
    return json_response(error=0,data=data)


@app.route('/divisi', methods=["GET","POST"])
def divisi():
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM divisi")
            data = curl.fetchall()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/divisi/detail/<path:id>', methods=["GET","POST"])
def detail_divisi(id):
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM divisi WHERE id=%s", (id,))
            data = curl.fetchone()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/item', methods=["GET","POST"])
def item():
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM item")
            data = curl.fetchall()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/item/divisi/<path:divisi>', methods=["GET","POST"])
def item_divisi(divisi):
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM item WHERE divisi=%s", (divisi,))
            data = curl.fetchall()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/item/detail/<path:id>', methods=["GET","POST"])
def detail_item(id):
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM item WHERE id=%s", (id,))
            data = curl.fetchone()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/event', methods=["GET","POST"])
def event():
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM event")
            data = curl.fetchall()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/event/detail/<path:id>', methods=["GET","POST"])
def detail_event(id):
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM event WHERE id=%s", (id,))
            data = curl.fetchone()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/event/create', methods=["GET","POST"])
def create_event():
    try:
        if request.method == 'POST':
            idu = request.json['idu']
            nama = request.json['nama']
            penyelenggara = request.json['penyelenggara']
            tgl_mulai = request.json['tgl_mulai']
            tgl_selesai = request.json['tgl_selesai']
            tempat = request.json['tempat']
            inorout = request.json['inorout']
            target = request.json['target']
            budget = request.json['budget']
            if idu and nama and penyelenggara and tgl_mulai and tgl_selesai and tempat and inorout and target and budget:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO event (idu, nama, penyelenggara, tgl_mulai, tgl_selesai, tempat, inorout, target, budget) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                        idu, nama, penyelenggara, tgl_mulai, tgl_selesai, tempat, inorout, target, budget
                    )
                )
                mysql.connection.commit()
                return json_response(error=0,message='Success. Event has been created')
            else:
                return json_response(error=1,message='Data must be fullfilled')
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/set-budget/<path:ide>', methods=["GET","POST"])
def set_budget(ide):
    try:
        if request.method == 'POST':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM event WHERE id=%s", (ide,))
            res_event = curl.fetchone()
            curl.close()
            if res_event:
                curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                curl.execute("SELECT * FROM divisi")
                res_divisi = curl.fetchall()
                curl.close()

                data = request.json['data']
                if len(data) == len(res_divisi):
                    if sum(data) == 100:
                        for i in range(len(data)):
                            idd = res_divisi[i]['id']
                            idu = res_event['idu']
                            budget = (int(data[i])/100)*int(res_event['budget'])
                            persentase = data[i]

                            cur = mysql.connection.cursor()
                            cur.execute("INSERT INTO budget (idu, ide, idd, budget, persentase) VALUES (%s, %s, %s, %s, %s)", (
                                idu, ide, idd, budget, persentase
                            ))
                            mysql.connection.commit()

                        return json_response(error=0,message='Success')
                    else:
                        return json_response(error=1,message='Jumlah persentase tidak 100%')
                else:
                    return json_response(error=1,message='Jumlah divisi tidak sama')
            else:
                return json_response(error=1,message='Event not found')
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))
    

@app.route('/generate/<path:ide>', methods=["GET","POST"])
def generate(ide):
    # try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM event WHERE id=%s", (ide,))
            res_event = curl.fetchone()
            curl.close()

            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM budget WHERE ide=%s", (ide,))
            res_budget = curl.fetchall()
            curl.close()

            if res_event:
                num_generations = 50
                solutions_per_pop = 10
                inout = res_event['inorout']

                res_si = []
                for i in range(len(res_budget)):
                    if res_event['inorout'] == 2:
                        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        curl.execute(
                            "SELECT * FROM item WHERE divisi="+str(i+1)+"")
                        res = curl.fetchall()
                        curl.close()
                    else:
                        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        curl.execute(
                            "SELECT * FROM item WHERE divisi="+str(i+1)+" AND in_or_outdoor="+str(inout)+" OR divisi="+str(i+1)+" AND in_or_outdoor=2")
                        res = curl.fetchall()
                        curl.close()

                    df_res = pd.DataFrame(res)
                    df_res = df_res.rename(columns = {0:'id', 1:'inout', 2:'item kategori', 3:'divisi', 4:'item', 5:'jumlah', 6:'satuan', 7:'harga', 8:'total_harga',9:'value'})

                    item_number = df_res['id']
                    weight = df_res['total_harga']
                    value = df_res['value']
                    knapsack_threshold = res_budget[i]['budget']

                    pop_size = (solutions_per_pop, len(df_res))
                    initial_population = np.random.randint(2, size = pop_size)
                    initial_population = initial_population.astype(int)

                    parameters, fitness_history = optimize(weight, value, initial_population, pop_size, num_generations, knapsack_threshold)

                    selected_items = item_number * parameters[0]
                    
                    arr_si = []
                    for j in range(len(selected_items)):
                        if int(1*selected_items[j]) > 0:
                            arr_si.append(int(selected_items[j]))

                    res_si.append(arr_si)

                item_fix = []
                for i in range(len(res_si)):
                    susun_ulang_kategori = []
                    susun_ulang_item = []
                    for j in range(len(res_si[i])):
                        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        curl.execute(
                            "SELECT * FROM item WHERE id="+str(res_si[i][j])+"")
                        res_divisi = curl.fetchall()
                        curl.close()
                        if res_divisi[0]['item_kategori'] not in susun_ulang_kategori:
                            susun_ulang_kategori.append(res_divisi[0]['item_kategori'])
                            item = [res_divisi[0]['id'],res_divisi[0]['divisi'],res_divisi[0]['item'],res_divisi[0]['total_harga']]
                            susun_ulang_item.append(item)
                    item_fix.append(susun_ulang_item)
                
                flat_item = []
                for i in range(len(item_fix)):
                    for j in range(len(item_fix[i])):
                        flat_item.append(item_fix[i][j])
                    
                return json_response(error=0,data=flat_item,message='Success')
            else:
                return json_response(error=1,message='Event not found')
        else:
            return json_response(error=1,message='Method not supported')
    # except Exception as e:
    #     return json_response(error=1,message=str(e))


@app.route('/budget', methods=["GET","POST"])
def budget():
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM budget")
            data = curl.fetchall()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/budget/event/<path:ide>', methods=["GET","POST"])
def budget_event(ide):
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM budget WHERE ide=%s", (ide,))
            data = curl.fetchall()
            curl.close()
            return json_response(error=0,data=data)
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))



#Seting budget per divisi
#Create model
#DropItem
#SaveToRAB


@app.route('/budget/create/<path:ide>', methods=["GET","POST"])
def create_budget_event(ide):
    try:
        if request.method == 'GET':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute(
                "SELECT * FROM event WHERE id=%s", (ide,))
            event = curl.fetchone()
            curl.close()
            if event:
                return json_response(error=1,message='Event ditemukan')
            else:
                return json_response(error=1,message='Event tidak ditemukan')
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/login', methods=["GET","POST"])
def login():
    try:
        if request.method == 'POST':
            email = request.json['email']
            password = request.json['password']
            if email and password:
                curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                curl.execute(
                    "SELECT * FROM user WHERE email=%s AND password=%s", (email, password))
                user = curl.fetchone()
                curl.close()
                if user:
                    return json_response(error=0,data=user)
                else:
                    return json_response(error=1,message='Ooops. User not found')
            else:
                return json_response(error=1,message='Email and password required')
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))


@app.route('/register', methods=["GET","POST"])
def register():
    try:
        if request.method == 'POST':
            nama = request.json['nama']
            email = request.json['email']
            password = request.json['password']
            if nama and email and password:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO user (nama, email, password) VALUES (%s, %s, %s)", (
                    nama, email, password
                ))
                mysql.connection.commit()
                return json_response(error=0,message='Success. User has been created')
            else:
                return json_response(error=1,message='Name, email and password required')
        else:
            return json_response(error=1,message='Method not supported')
    except Exception as e:
        return json_response(error=1,message=str(e))
    

if __name__ == "__main__":
    app.run(debug=True)