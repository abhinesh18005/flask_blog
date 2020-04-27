from flask import render_template,url_for,Flask
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


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]





@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/categories")
def categories():
    cursor.execute("select * from categories;")
    category = []
    results = cursor.fetchall()
    for row in results:
        Id = row[0]
        name = row[1]
        description = row[2]
        category.append({'id':Id,'name':name,'description':description})
    return render_template('categories.html', category=category,title='Categories')


@app.route("/employees")
def employees():
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
    cursor.execute("select * from owners;")
    owner_list = {}
    results = cursor.fetchall()
    for row in results:
        owner_list[row[0]] = row[1]
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
    cursor.execute("select * from products_to_sell;")
    results = cursor.fetchall()
    product_list = {}
    for row in results:
        product_list[row[0]]=row

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
    cursor.execute("select * from products_to_rent;")
    results = cursor.fetchall()
    product_list = {}
    for row in results:
        product_list[row[0]]=row

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
    app.run()
