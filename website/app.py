from flask import Flask, render_template, request, jsonify, url_for, redirect
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)



config = {
  'host':'dbms-proj-server.mysql.database.azure.com',
  'user':'dbmsproj@dbms-proj-server',
  'password':'Dbmspr0j3ct75',
  'database':'antique_store'
}   

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def re_connect():
    global config, conn, cursor
    config = {
        'host':'dbms-proj-server.mysql.database.azure.com',
        'user':'dbmsproj@dbms-proj-server',
        'password':'Dbmspr0j3ct75',
        'database':'antique_store'
    }   

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("reconnecting to the database")


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/refresh")
def refresh():
    import refresh_graphs
    return render_template('refresh.html')


@app.route("/categories")
def categories():

    try:
        cursor.execute("select * from categories;")
    except:
        re_connect()
        cursor.execute("select * from categories;")

    category = []
    results = cursor.fetchall()
    for row in results:
        Id = row[0]
        name = row[1]
        description = row[2]
        category.append({'id':Id,'name':name,'description':description})
    return render_template('categories.html', category=category,title='Categories')


@app.route("/select", methods = ['GET', 'POST'])
def select():
    if request.method == 'POST':
        id = request.form.get('input')
        return redirect(url_for('table', id=id))

    try:
        cursor.execute("show tables;")
    except:
        re_connect()
        cursor.execute("show tables;")

    tables = []
    results = cursor.fetchall()
    for row in results:
        tables.append({'name':row[0]})
    return render_template('select.html', tables=tables,title='Tables')


@app.route("/table/<id>",methods = ['GET', 'POST'])
def table(id):
    if request.method == 'POST':
        id2 = ""
        c1 = ""
        c2 = ""
        c3 = ""
        c4 = ""
        c5 = ""
        for v in request.form:
            #print(v,request.form[v])
            if(v=='1'):
                c1 = request.form[v]
            elif(v=='2'):
                c2 = request.form[v]
            elif(v=='3'):
                c3 = request.form[v]
            elif(v=='4'):
                c4 = request.form[v]
            elif(v=='5'):
                c5 = request.form[v]
            else:
                id2+=v+","
        if(c3==""):
            c3='3'
        id2 = id2[:len(id2)-1]
        #print(c1,c2,c3)
        return redirect(url_for('last',id1=id,id2=id2,c1=c1,c2=c2,c3=c3,c4=c4,c5=c5))

    try:
        cursor.execute("show columns from "+id+";")
    except:
        re_connect()
        cursor.execute("show columns from "+id+";")
        
    columns = []
    results = cursor.fetchall()
    columns2 = [{"name": "="},{"name": ">"},{"name": "<"}]
    for row in results:
        columns.append({'name':row[0]})
    return render_template('table.html', columns=columns,id=id,columns2=columns2)


@app.route("/last/<id1>/<id2>/<c1>/<c2>/<c3>/<c4>/<c5>")
def last(id1,id2,c1,c2,c3,c4,c5):
    #print(id2)
    #print(c1,c2,c3,"hhhhhh")
    c3="'"+c3+"'"

    if(c1=='Select attributes:'):
        if(c4=='Select attributes:'):
            try:
                cursor.execute("select "+id2+" from "+id1+";")
            except:
                re_connect()
                cursor.execute("select "+id2+" from "+id1+";")
        else:
            try:
                cursor.execute("select "+id2+" from "+id1+" order by "+c4+" "+c5+";")
            except:
                re_connect()
                cursor.execute("select "+id2+" from "+id1+" order by "+c4+" "+c5+";")
    else:
        if(c4=='Select attributes:'):
            try:
                cursor.execute("select "+id2+" from "+id1+" where "+c1+c2+c3+";")
            except:
                re_connect()
                cursor.execute("select "+id2+" from "+id1+" where "+c1+c2+c3+";")
        else:
            try:
                cursor.execute("select "+id2+" from "+id1+" where "+c1+c2+c3+" order by "+c4+" "+c5+";")
            except:
                re_connect()
                cursor.execute("select "+id2+" from "+id1+" where "+c1+c2+c3+" order by "+c4+" "+c5+";")

    id2  = id2.split(",")
    attributes = ""
    n = len(id2)
    #print(id2,id1,id2[0])
    attributes+=id2[0]
    for i in range(1,n):
        #print(id2[i])
        attributes+=","+id2[i]
    #print("select "+attributes+" from "+id1+";")
    
    
    columns = []
    results = cursor.fetchall()
    for row in results:
        dic = {}
        for i in range(n):
            dic[id2[i]] = row[i]
            #print(id2[i],row[i],i)
        columns.append(dic)
    return render_template('last.html',dates=columns,columns=id2,headline=id1)


@app.route("/employees")
def employees():
    try:
        cursor.execute("select * from employees;")
    except:
        re_connect()
        cursor.execute("select * from employees;")
    
    employees_list = []
    results = cursor.fetchall()
    for row in results:
        name = row[1]
        dob = row[2]
        salary = row[3]
        employees_list.append({'name':name,'dob':dob,'salary':salary})
    return render_template('employees.html', employees_list=employees_list,title='Employees')


@app.route("/sessions")
def sessions():
    try:
        cursor.execute("select * from sessions;")
    except:
        re_connect()
        cursor.execute("select * from sessions;")
    
    sessions_list = []
    results = cursor.fetchall()
    for row in results:
        sessionsID = row[0]
        userID = row[1]
        sessions_list.append({'sessionsID':sessionsID,'userID':userID})
    return render_template('sessions.html', sessions_list=sessions_list,title='Sessions')



@app.route("/users")
def users():
    try:
        cursor.execute("select * from user;")
    except:
        re_connect()
        cursor.execute("select * from user;")
    
    user_list = []
    results = cursor.fetchall()
    for row in results:
        userid = row[0]
        name = row[1]
        address = row[2]
        city = row[3]
        country = row[4]
        contactno = row[5]
        emailid = row[6]
        pincode = row[7]
        date_added = row[8]
        last_active = row[9]
        dob = row[10]
        gender = row[11]
        user_list.append({'userid':userid,'name':name,'address':address,'city':city,'country':country,'contactno':contactno,'emailid':emailid,'pincode':pincode,'date_added':date_added,'last_active':last_active,'dob':dob,'gender':gender})

    return render_template('users.html', user_list=user_list,title='Users')

@app.route("/users/owners")
def owners():
    try:
        cursor.execute("select * from owners;")
    except:
        re_connect()
        cursor.execute("select * from owners;")

    
    owner_list = {}
    results = cursor.fetchall()
    for row in results:
        owner_list[row[0]] = row[1]
    try:
        cursor.execute("select * from user;")
    except:
        re_connect()
        cursor.execute("select * from user;")
    user_list = []
    results = cursor.fetchall()
    for row in results:
        userid = row[0]
        name = row[1]
        address = row[2]
        city = row[3]
        country = row[4]
        contactno = row[5]
        emailid = row[6]
        pincode = row[7]
        date_added = row[8]
        last_active = row[9]
        dob = row[10]
        gender = row[11]
        if(userid in owner_list):
            user_list.append({'userid':userid,'name':name,'address':address,'city':city,'country':country,'contactno':contactno,'emailid':emailid,'pincode':pincode,'date_added':date_added,'last_active':last_active,'dob':dob,'gender':gender,'stars':owner_list[userid]})

    return render_template('owners.html', user_list=user_list,title='Owners')




@app.route("/categories/products/<list_id>")
def products(list_id):
    try:
        cursor.execute("select * from products where CategoryID='"+list_id+"';")
    except:
        re_connect()
        cursor.execute("select * from products where CategoryID='"+list_id+"';")
    
    product_list = []
    results = cursor.fetchall()
    for row in results:
        pid = row[0]
        userid = row[1]
        categoryid = row[2]
        name = row[3]
        stars = row[4]
        location = row[5]
        city = row[6]
        country = row[7]
        date_added = row[9]
        product_list.append({'pid':pid,'userid':userid,'categoryid':categoryid,'name':name,'stars':stars,'location':location,'city':city,'country':country,'date_added':date_added})

    return render_template('products.html', product_list=product_list,title='Products')


@app.route("/categories/products_to_sell/<list_id>")
def products_to_sell(list_id):
    try:
        cursor.execute("select * from products_to_sell;")
    except:
        re_connect()
        cursor.execute("select * from products_to_sell;")
    
    results = cursor.fetchall()
    product_list = {}
    for row in results:
        product_list[row[0]]=row

    try:
        cursor.execute("select * from products where CategoryID='"+list_id+"';")
    except:
        re_connect()
        cursor.execute("select * from products where CategoryID='"+list_id+"';")
    results = cursor.fetchall()
    product_sell_list = []
    for row in results:
        pid = row[0]
        userid = row[1]
        categoryid = row[2]
        name = row[3]
        stars = row[4]
        location = row[5]
        city = row[6]
        country = row[7]
        date_added = row[9]
        if(pid in product_list):
            product_sell_list.append({'pid':pid,'userid':userid,'categoryid':categoryid,'name':name,'stars':stars,'location':location,'city':city,'country':country,'date_added':date_added,'price':product_list[pid]})

    return render_template('products_to_sell.html', product_sell_list=product_sell_list,title='Products_to_sell')


@app.route("/categories/products_to_rent/<list_id>")
def products_to_rent(list_id):
    try:
        cursor.execute("select * from products_to_rent;")
    except:
        re_connect()
        cursor.execute("select * from products_to_rent;")
    
    results = cursor.fetchall()
    product_list = {}
    for row in results:
        product_list[row[0]]=row

    try:
        cursor.execute("select * from products where CategoryID='"+list_id+"';")
    except:
        re_connect()
        cursor.execute("select * from products where CategoryID='"+list_id+"';")
    results = cursor.fetchall()
    product_rent_list = []
    for row in results:
        pid = row[0]
        userid = row[1]
        categoryid = row[2]
        name = row[3]
        stars = row[4]
        location = row[5]
        city = row[6]
        country = row[7]
        date_added = row[9]
        if(pid in product_list):
            product_rent_list.append({'pid':pid,'userid':userid,'categoryid':categoryid,'name':name,'stars':stars,'location':location,'city':city,'country':country,'date_added':date_added,'rentpriceperday':product_list[pid][1],'minrentdays':product_list[pid][2],'maxrentdays':product_list[pid][3],'availablefrom':product_list[pid][4],'availabletill':product_list[pid][5]})

    return render_template('products_to_rent.html', product_rent_list=product_rent_list,title='Products_to_rent')


@app.route("/exit")
def exit():
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('exit.html')

if __name__=="__main__":
    app.run(debug=True)
