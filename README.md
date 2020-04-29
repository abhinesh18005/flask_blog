# dbms project - ANTIQUE STORE (A Team project)

Here, we have created the database for an online antique store and host it on azure.
Also, we have created a dashboard for visulaizing the data in the form of graphs and dashboard allows the user to run the queries easily and efficiently (using the GUI)

URL of the website - https://antique-store-dashboard.herokuapp.com/

# How to install it on your PC's

Just follow the below steps in order to run this web app offline on your computer.

1. Clone the repository on the system.
2. Open the terminal and go to the destination of the cloned file.
3. Type "cd website" in the terminal.
4. Enter "pip install -r requirements.txt"
5. Run "python app.py" from your terminal.

Here you go, the application is running on your terminal. <br>
Just open the displayed URL (on terminal) on your web browser.

# Features

Website - https://antique-store-dashboard.herokuapp.com/ main page looks something like the below image.

<img width="1440" alt="Screenshot 2020-04-29 at 11 39 29 PM" src="https://user-images.githubusercontent.com/43913398/80631217-09e38800-8a73-11ea-9614-b5ae9c3cb205.png">

<br>

We have the following tabs:
1. Home: displays several <Strong>graphical representation of the data.</Strong>
2. Categories: displays categories table of the database.
3. Users: displays Users table of the database.
4. Employees: displays Employees table of the database.
5. Sessions: displays Sessions table of the database.
6. Select: <Strong>allows to write queries in interactive manner </Strong> (allows to select table and attributes with the help of GUI) and has features like =, >, < and sort-by.

<img width="1440" alt="Screenshot 2020-04-29 at 11 49 12 PM" src="https://user-images.githubusercontent.com/43913398/80631881-0b618000-8a74-11ea-9246-4e398a20ceb2.png">


# Technology Stack ...

1. PYTHON is the man programming language that this web app is built on. We are using sql-connector-python to connect our database with the python and run the queries in python.

2. Cascading style sheets (CSS) and bootstrap has also been used for the frontend.

# Files STRUCTURE

Brief description of role of each file in the repo.
<ul>
 <li> <Strong> Others </Strong> : responsible for creating all the iframes for all the graphs used in the website.
     <br>
 
 
 <li> <Strong> website </Strong> <br>
  Contains the full website that has been hosted on heroku - https://antique-store-dashboard.herokuapp.com/
    <ol>
      <li><Strong> static - </Strong> contains images of data analysis</li>
      <li><Strong> templates - </Strong> contains .html file</li>
      <li><Strong> venv - </Strong> for creating virtual env named "venv"</li>
      <li><Strong> Procfile - </Strong> so heroku can detect that it's an app</li>
      <li><Strong> app.py - </Strong> for setting up flask (backend) </li>
      <li><Strong> requirements.txt - </Strong> contains names of all the dependencies required to rub the app</li>
     
   </ol> </li> <br>
   
 <li> <Strong> README.md </Strong></li>
 <li> <Strong>  database_doc.pdf</Strong>: Information regarding the database modelling</li>
</ul>

# Database
All the information regarding the database is present @ database_doc.pdf  
