import mysql.connector
from mysql.connector import errorcode
import chart_studio.plotly as py
import pandas as pd
import plotly.express as px

config = {
  'host':'dbms-proj-server.mysql.database.azure.com',
  'user':'dbmsproj@dbms-proj-server',
  'password':'Dbmspr0j3ct75',
  'database':'antique_store'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

cursor.execute("select * from user;")
results = cursor.fetchall()
df = pd.DataFrame(results)
columns = []
for cd in cursor.description:
    columns.append(cd[0])
df.columns = columns
fig = px.pie(df, names='Country', title='Registered Users by Country')
#fig.show()
py.plot(fig, filename = 'Users_per_country', auto_open=False)

fig = px.histogram(df, x="DateAdded", 
                   histfunc='count', 
                   title='Users Registered by Date', 
                   labels={'count':'Number of users registered on that day'}, 
                   color="Gender",
                   nbins = 40
                  )
#fig.show()


py.plot(fig, filename = 'Registered_Users_per_date', auto_open=False)

fig = px.histogram(df, x="DateAdded", 
                   histfunc='count', 
                   title='Total Number of Users', 
                   color="Gender",
                   nbins = 40,
                   cumulative=True
                  )
#fig.show()
py.plot(fig, filename = 'Total Number of Users', auto_open=False)

cursor.execute("select * from owners;")
results = cursor.fetchall()
df = pd.DataFrame(results)
columns = []
for cd in cursor.description:
    columns.append(cd[0])
df.columns = columns
fig = px.histogram(df, x="Stars", 
                   histfunc='count', 
                   title='Number of Sellers by Stars', 
                   nbins = 20)
#fig.show()
py.plot(fig, filename = 'Number of Sellers by Stars', auto_open=False)

cursor.execute("select Gender,SessionID  " + 
               "from sessions,user " + 
               "where user.UserID=sessions.UserID"
               ";")
results = cursor.fetchall()
df = pd.DataFrame(results)
columns = []
for cd in cursor.description:
    columns.append(cd[0])
df.columns = columns
fig = px.histogram(df, x="SessionID", 
                   histfunc='count', 
                   title='Number of ACTIVE Users by date', 
                   color="Gender",
                   nbins = 40)
#fig.show()
py.plot(fig, filename = 'Number of ACTIVE Users by date', auto_open=False)

config = {
  'host':'dbms-proj-server.mysql.database.azure.com',
  'user':'dbmsproj@dbms-proj-server',
  'password':'Dbmspr0j3ct75',
  'database':'antique_store'
}
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

cursor.execute("select * from orders")
results = cursor.fetchall()
df = pd.DataFrame(results)
columns = []
for cd in cursor.description:
    columns.append(cd[0])
df.columns = columns
fig = px.pie(df, values='AmtPaid', names='PaymentMode', title='Amount Paid by several Payment Modes')
#fig.show()
py.plot(fig, filename = 'Payment Mode', auto_open=False)

fig = px.histogram(df, x="SessionID", 
                   y="AmtPaid", 
                   histfunc='sum',
                   nbins=40,
                   color = 'PaymentMode',
                   title='Revenue Generated per Month by different payment modes')
#fig.show()
py.plot(fig, filename = 'Revenue Generated per Month', auto_open=False)

cursor.execute("select * " + 
               "from products,categories " + 
               "where products.CategoryID=categories.CategoryID"
               ";")
results = cursor.fetchall()
df = pd.DataFrame(results)
columns = []
for cd in cursor.description:
    columns.append(cd[0])
df.columns = columns
fig = px.histogram(df, x="Stars", 
                   histfunc='count',
                   nbins=10,
                   color = 'CategoryName',
                   title='Distribution of Stars by Categories')
#fig.show()
py.plot(fig, filename = 'Distribution of Stars by Categories', auto_open=False)

fig = px.pie(df, names='CategoryName', title='Distribution of products as per Categories')
#fig.show()
py.plot(fig, filename = 'Distribution of products as per Categories', auto_open=False)

config = {
  'host':'dbms-proj-server.mysql.database.azure.com',
  'user':'dbmsproj@dbms-proj-server',
  'password':'Dbmspr0j3ct75',
  'database':'antique_store'
}
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

cursor.execute("select * " + 
               "from orderdetails,orders,products,categories " + 
               "where orderdetails.OrderID=orders.OrderID and products.PID=orderdetails.PID and products.CategoryID=categories.CategoryID"
               ";")
results = cursor.fetchall()
df = pd.DataFrame(results)
columns = []
for cd in cursor.description:
    columns.append(cd[0])
df.columns = columns
fig = px.pie(df, values='Price', names='CategoryName', title='Revenue by Category')
#fig.show()
py.plot(fig, filename = 'Revenue by Category', auto_open=False)

fig = px.histogram(df, x="SessionID", 
                   y="Price", 
                   histfunc='sum',
                   nbins=40,
                   color = 'CategoryName',
                   title='Revenue Generated per Month by Category')
#fig.show()
py.plot(fig, filename = 'Revenue Generated per Month by Categor', auto_open=False)

fig = px.histogram(df, x="SessionID", 
                   y="Price", 
                   histfunc='sum',
                   nbins=40,
                   color = 'type',
                   title='Revenue Generated per Month (sold vs rented)')
#fig.show()
py.plot(fig, filename = 'Revenue Generated per Month (sold vs rented)', auto_open=False)

fig = px.pie(df, values='Price', names='type', title='Total Revenue by type (rented vs sold)')
#fig.show()
py.plot(fig, filename = 'Total Revenue by type (rented vs sold)', auto_open=False)