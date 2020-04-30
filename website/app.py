from flask import Flask, render_template, flash, request, jsonify, url_for, redirect
import mysql.connector
from mysql.connector import errorcode
from forms import QueryForm
import difflib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AkDODUStAGmDbLWkYcgFDw'


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

all_table_names = []
def fill_all_table_names():
    global all_table_names
    all_table_names = []
    try:
        cursor.execute("show tables;")
    except:
        re_connect()
        cursor.execute("show tables;")
    results = cursor.fetchall()
    for i in results:
        all_table_names.append(i[0])

def get_column_names(table_name):
    query = "SHOW COLUMNS FROM antique_store." + table_name + ";"
    try:
        cursor.execute(query)
    except:
        re_connect()
        cursor.execute(query)

    column_names = []
    results = cursor.fetchall()
    for i in results:
        column_names.append(i[0])
    return column_names




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
    c3 = c3.replace("'","")
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


@app.route("/users/profile/<list_id>")
def userdetails(list_id):
    try:
        cursor.execute("select * from user where userid = '" + list_id +"';")
    except:
        re_connect()
        cursor.execute("select * from user where userid = '" + list_id +"';")
    
    row = cursor.fetchone()
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
    results = {'userid':userid,'name':name,'address':address,'city':city,'country':country,'contactno':contactno,'emailid':emailid,'pincode':pincode,'date_added':date_added,'last_active':last_active,'dob':dob,'gender':gender}
    return render_template('user_profile.html', pro=results,title='User Profile: '+name)

@app.route("/users/Country/<name>")
def userbycountry(name):
    try:
        cursor.execute("select * from user where country = '" + name +"';")
    except:
        re_connect()
        cursor.execute("select * from user where country = '" + name +"';")
    
    user_list = []
    results = cursor.fetchall()
    cname = name
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
    return render_template('user_by_country.html', user_list=user_list,title='Search by: '+cname,country=cname)


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

@app.route("/runquery", methods=['GET','POST'])
def runquery():
    form = QueryForm()
    query_results = []
    columns = []
    if form.validate_on_submit():
        try:
            s = str(form.query.data)
            s = s.strip()
            if s.find(';') == -1:
                raise Exception("Semicolon (;) missing")
            if s.find(';') != len(s)-1:
                raise Exception("Multiple queries not allowed")
            try:
                cursor.execute(form.query.data)
            except:
                re_connect()
                cursor.execute(form.query.data)
            results = cursor.fetchall()
            columns = cursor.column_names
            query_results = results
        except Exception as e:
            if ("Table" in str(e)) and ("doesn't exist" in str(e)):
                # means has to suggest table also...
                if all_table_names==[]:
                    fill_all_table_names()
                last_index = str(e).find("' doesn't")
                first_index = str(e).find("'antique_store")
                suggestion = difflib.get_close_matches(str(e)[first_index+15:last_index], all_table_names)
                #print('Error: ' + str(e) + "\n Do you mean: " + str(suggestion))
                if(suggestion==[]):
                    message = 'Error: ' + str(e) + "... NO table found in the database with similar name "
                else:
                    message = 'Error: ' + str(e) + "... Do you mean: " + str(suggestion)
                flash(message,'danger')

            elif "Unknown column" in str(e):
                first_index = 16 + str(e).find("Unknown column")
                last_index = str(e).find("' in 'field list'")
                column_name_inserted = str(e)[first_index: last_index]
                q = str(form.query.data)
                table_name = q[q.find("from")+5:-1]
                column_names = get_column_names(table_name)
                #print(column_names)
                #print(column_name_inserted)
                suggestion = difflib.get_close_matches(column_name_inserted, column_names)
                if(suggestion==[]):
                    message = 'Error: ' + str(e) + "...... NO column found in the table with similar name "
                else:
                    message = 'Error: ' + str(e) + "...... Do you mean: " + str(suggestion)
                flash(message,'danger')


            else:
                flash('Error: ' + str(e),'danger')
        else:
            flash('Query run successfully!', 'success')
    # if request.method == 'POST':
    #     if request.form['export_btn'] == "export to csv":
    #         si = StringIO.StringIO()
    #         cw = csv.writer(si)
    #         cw.writerow([columns])
    #         cw.writerows(query_results)
    #         response = make_response(si.getvalue())
    #         response.headers['Content-Disposition'] = 'attachment; filename=report.csv'
    #         response.headers["Content-type"] = "text/csv"
    #         return response
    return render_template('runquery.html', form=form, columns=columns, query_results=query_results, title='Run query')



@app.route("/exit")
def exit():
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('exit.html')



if __name__=="__main__":
    app.run(debug=True)
