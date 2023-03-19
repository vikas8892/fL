from flask import Flask, render_template, redirect, request, url_for
import pymysql as pm

app=Flask(__name__)

@app.route('/')     # home page of contact website
def home():
    return render_template('index.html')

@app.route('/all_contact')      # it retrieves all details from the table and then displays it
def all_contact():
    db=pm.Connect(host='localhost',user='root',password='1234',database='phone')
    cur=db.cursor()
    cur.execute('select * from contactlist')
    datalist=cur.fetchall()
    return render_template('all_contact.html',datalist=datalist)

@app.route('/deletecontact')    # takes you to a page to detelte user details
def deletecontact():
    return render_template('deletecontact.html')

@app.route('/deleting', methods=['POST'])   # code to delete user name & no. from table
def deleting():
    delcont=request.form['delcont']
    db=pm.Connect(host='localhost',user='root',password='1234',database='phone')
    cur=db.cursor()
    cur.execute(f"delete from contactlist where name='{delcont}'")
    db.commit()
    return redirect(url_for('deletecontact'))

@app.route('/details')      # takes you to a page to receive user details
def details():
    return render_template('details.html')

@app.route('/entry',methods=['POST'])       # saves user details into database. used as 'Create new contact'
def entry():
    try:
        PersonName=request.form['PersonName']
        PersonName=PersonName.strip()
        PhoneNumber=int(request.form['PhoneNumber'])
        db=pm.Connect(host='localhost',user='root',password='1234',database='phone')
        cur=db.cursor()
        cur.execute(f"select * from contactlist where name ='{PersonName}'")
        if cur.fetchall():
            return f'The name already exist. Please enter new name.'
        else:
            cur.execute(f"insert into contactlist (name, phoneno) values('{PersonName}',{PhoneNumber})")
            db.commit()
    except Exception as e:
        return f'Please give details carefully. The error is {e}'
    return redirect(url_for('details'))

@app.route('/updatecontact')   # it takes us to update page
def updatecontact():
    return render_template('updatecontact.html')

@app.route('/doupdate', methods=['POST'])       # it updates both name and phone number
def doupdate():
    try:
        correctno=int(request.form['CorrectNumber'])
        PersonName=request.form['PersonName']
        correctname=request.form['CorrectName']
        db=pm.Connect(host='localhost',user='root',password='1234',database='phone')
        cur=db.cursor()
        if correctname!=' ':
            cur.execute(f"update contactlist set name='{correctname}' where name='{PersonName}'")
            db.commit()
        if correctno!=' ':
            cur.execute(f"update contactlist set phoneno={correctno} where name='{PersonName}'")
            db.commit()
    except ValueError:
        return f'You have not mentioned whose name to be changed/ entered a number/ entered alphabets in phone no.'
    return redirect(url_for('updatecontact'))

@app.route('/dosearch', methods=['POST'])   # used to take value user, then send the value to search function below
def dosearch():
    searchname=request.form['srchnm']
    searchname=searchname.strip()
    return redirect(url_for('search',name=searchname))

@app.route('/search/<name>')    # searches value in database and returns both name and number
def search(name):
    db=pm.Connect(host='localhost',user='root',password='1234',database='phone')
    cur=db.cursor()
    cur.execute(f"select * from contactlist where name='{name}'")
    datalist=cur.fetchall()
    return render_template('all_contact.html',datalist=datalist)

if __name__=='__main__':    
    app.run(debug=True)
