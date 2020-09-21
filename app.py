from flask import Flask, render_template, request ,escape,session,redirect,url_for,g
import pyrebase
import json


firebaseConfig = {
    'apiKey': "AIzaSyAdvb-K6YEK95EbsvLMEavSpOiasbv5snQ",
    'authDomain': "giswebsite-9631a.firebaseapp.com",
    'databaseURL': "https://giswebsite-9631a.firebaseio.com",
    'projectId': "giswebsite-9631a",
    'storageBucket': "giswebsite-9631a.appspot.com",
    'messagingSenderId': "374608218035",
    'appId': "1:374608218035:web:01d0faa031b38bd5c32dc6",
    'measurementId': "G-RNVDGF2V0L"
  };
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
def sets():
    hell={}
    hell['projects'] = []
    sets =db.child("Projects").get()
    for i in sets:
        if i.val() != None:
            s1 = json.dumps(i.val())
            y=json.loads(s1)
            hell["projects"].append({
                'name':y["name"],
                'id':y["id"],
                'url':y["img"],
                'about':y["About"]
            })
    return hell["projects"]
    json.dumps(hell, indent=4)
                
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='NikolozGIS', password='Sandro17!'))


def GetHappy():
    information=db.child("Costumers").child("Experience").child("Happy").get()
    for i in information.each():
        HappyUsers=i.val();
    return HappyUsers
def GetProjects():
    information=db.child("Costumers").child("Experience").child("Projects").get()
    for i in information.each():
        projectsDone=i.val();
    return projectsDone
def GetYears():
    information=db.child("Costumers").child("Experience").child("Years").get()
    for i in information.each():
        yearsDone=i.val();
    return yearsDone
def GetEmail():
    information=db.child("ContactInfo").child("Email").get()
    for i in information.each():
        email=i.val();
    return email           
def GetPhoneNumber():
    information=db.child("ContactInfo").child("Phone_Number").get()
    for i in information.each():
        phone_number=i.val();
    return phone_number

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route("/")
def Menu():
    return render_template("index.html",the_title="Georgian Intergrated System"
                           ,email=GetEmail(),phone_number=GetPhoneNumber()
                           ,happyUsers=GetHappy(),projectsDone=GetProjects(),yearsDone=GetYears())

@app.route("/about")
def About():
    return render_template("projects.html",the_title="Georgian Intergrated System",email=GetEmail(),sets=sets(),phone_number=GetPhoneNumber())

@app.route("/contact")
def Contact():
    return render_template("contact.html",the_title="Georgian Intergrated System",email=GetEmail(),phone_number=GetPhoneNumber())

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method=="POST":
        session.pop('user_id', None)
        username = request.form["username"]
        password = request.form["password"]
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('admin'))
        
        return redirect(url_for('adminlogin'))

    return render_template("admin.html")    

@app.route("/admin")
def admin():
    if not g.user:
        return redirect(url_for('adminlogin'))
    return render_template("adminfull.html")

if __name__ == "__main__":
    from elsa import cli
    cli(app, base_url='https://example.com')
    app.run()