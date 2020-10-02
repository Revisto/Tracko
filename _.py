from flask import Flask, render_template, request,redirect, url_for, session, abort,flash
from flask_recaptcha import ReCaptcha
import requests
import json
from _C_ import *

app = Flask(__name__, template_folder="html",static_folder="static")
app.secret_key = b'_5M=ALmV7d*knY^#'
app.config.update({'RECAPTCHA_ENABLED': True,
                   'RECAPTCHA_DATA_ATTRS' : {'theme': 'dark'},
                   'RECAPTCHA_SITE_KEY':
                       '6Lej5tIZAAAAABScYu3BfpdhU_4oSB-NuSwnYv2_',
                   'RECAPTCHA_SECRET_KEY':
                       '6Lej5tIZAAAAAII7crOoMJmtibX-K5TLAmzzdx-Z'})
recaptcha = ReCaptcha(app=app)

@app.route('/')
def index():
    if session.get('logged_in'):
        if (AllCards(session["Username"]))=='':return render_template('index.html',CardsNone="True",Name=session["Username"])
        else:return render_template('index.html',Cards=AllCards(session["Username"]),Name=session["Username"],Remove='True')
    else:
    	return render_template('index.html',Preview="True")

@app.route('/faq')
def Faq():
    if session.get('logged_in'):
        if (AllCards(session["Username"]))=='':return render_template('faq.html',CardsNone="True",Name=session["Username"])
        else:return render_template('faq.html',Cards=AllCards(session["Username"]),Name=session["Username"],Remove='True')
    else:
    	return render_template('faq.html',Preview="True")


@app.route('/Update',methods=['post', 'get'])
def Updater():
    if not session.get('logged_in'):
    	return redirect("/SignIn")
    return render_template('Update.html',Series=AllSeriesSelectCode(session["Username"]))

@app.route('/AddMedia',methods=['post', 'get'])
def Adder():
    if not session.get('logged_in'):
    	return redirect("/SignIn")
    return render_template('AddMedia.html')

@app.route('/DeleteShow',methods=['post', 'get'])
def Deleter():
    if not session.get('logged_in'):
    	return redirect("/SignIn")
    return render_template('Delete.html',Series=AllSeriesSelectCode(session["Username"]))


@app.route('/SignUp',methods=['post', 'get'])
def SignUp():
    
    return render_template('signup.html')

@app.route('/SignIn',methods=['post', 'get'])
def SignIn():
    return render_template('signin.html')

@app.route('/SignOut')
def LogOut():
    del session['logged_in']
    return redirect("/")

@app.route('/Update_Media', methods=['POST'])
def handle_Update():
    Warnings=''
    Name = request.form.get('medianame') 
    if Name==None:
       try:return render_template('Update.html',Series=AllSeriesSelectCode(session["Username"]),NoMedia="True")
       except:return render_template('Update.html',Series=AllSeriesSelectCode(session["Username"]),NoSignUp="True")

    Season = request.form.get('season') 
    Episode = request.form.get('episode')  
    Min = request.form.get('min')  
    Sec = request.form.get('sec')  
    List=[Name,Season,Episode,Min,Sec]
    List_=['Name','Season','Episode','Min','Sec']
    if not((Season!='' and Episode!='' and Min!='' and Sec!='') or (Episode!='' and Min!='' and Sec!='') or (Min!='' and Sec!='') or (Sec!='')):
        Warnings+='Please Be Careful About Hereditary method. '
    if Name=='': Warnings +='You Must Choose a Series. '
    
    if Warnings!='':
        return render_template('Update.html',Series=AllSeriesSelectCode(session["Username"]),message=Warnings)
    
    UpdateData(Name,Season,Episode,Min,Sec,session["Username"])
    print (Name,Season,Episode,Min,Sec)
    return redirect('/')

@app.route('/DeleteForm', methods=['POST'])
def handle_Delete():
    Warnings=''
    Name = request.form.get('medianame') 
    if Name==None:
       try:return render_template('Delete.html',Series=AllSeriesSelectCode(session["Username"]),NoMedia="True")
       except:return render_template('Delete.html',Series=AllSeriesSelectCode(session["Username"]),NoSignUp="True")

    if Name=='': Warnings +='You Must Choose a Series. '
    
    if Warnings!='':
        return render_template('Delete.html',Series=AllSeriesSelectCode(session["Username"]),message=Warnings)
    
    DeleteShow(session["Username"],Name)

    return redirect('/')

@app.route('/AddMedia_Add', methods=['POST'])
def handle_Add():
    Warnings=''
    Name = request.form.get('MediaName') 
    for m in (ReadData())[session["Username"].lower()]:
        if m['Name']==Name:
            Warnings+='The Name Already exists. '   
            break
    genere = request.form.get('genere') 
    Secoundgenere = request.form.get('genere2')  
    score = request.form.get('score')  
    description = request.form.get('description') 
    description=description.replace('"', '')
    description=description.replace("'", '')
    description=description.replace(chr(92), '')
    f = request.files['upload']
    List=[f.filename,Name,genere,Secoundgenere,score,description]
    List_=[f.filename,'Name','genere','Secound genere','score','description']
    for i in range(len(List)):
        if List[i]=='':
            if i==0: Warnings+='You Must Upload Cover Picture. '
            else: Warnings+=List_[i].title()+' Can Not Be Empty. '
    if Warnings!='':
        return render_template('AddMedia.html',message=Warnings)
    
    try:f.save('static/img/Media/'+session["Username"].lower()+'/'+Name.replace(' ', '_')+'.jpg')
    except: mkdir('static/img/Media/'+session["Username"].lower());f.save('static/img/Media/'+session["Username"].lower()+'/'+Name.replace(' ', '_')+'.jpg')
    Resize('static/img/Media/'+session["Username"].lower()+'/'+Name.replace(' ', '_')+'.jpg')
    AddData('/static//img/Media/'+session["Username"].lower()+'/'+Name.replace(' ', '_')+'.jpg',Name,genere,Secoundgenere,score,description,session["Username"])
    return redirect('/')

@app.route('/SignInForm', methods=['POST'])
def SignInForm():
    r = requests.post('https://www.google.com/recaptcha/api/siteverify',
        data = {'secret' :
                '6Lej5tIZAAAAAII7crOoMJmtibX-K5TLAmzzdx-Z',
                'response' :
                request.form['g-recaptcha-response']})

    google_response = json.loads(r.text)
    print('JSON: ', google_response)

    if google_response['success']:
        print('SUCCESS')
        pass
    else:
        print('FAILED')
        return render_template("signin.html",message="Recaptcha failed. ")
    
    
    try:
        db=ReadDB()
        if (db[(request.form['Username']).lower()])[0]==request.form['Password']:
            session['logged_in'] = True
            session["Username"] = request.form['Username']
        else:
            raise Exception("Not Match")
    except: return render_template("signin.html",message="The username or the password is incorrect")
	
    return redirect("/")
    
@app.route('/SignUpForm', methods=['POST'])
def SignUpForm():
    r = requests.post('https://www.google.com/recaptcha/api/siteverify',
        data = {'secret' :
                '6Lej5tIZAAAAAII7crOoMJmtibX-K5TLAmzzdx-Z',
                'response' :
                request.form['g-recaptcha-response']})

    google_response = json.loads(r.text)
    print('JSON: ', google_response)

    if google_response['success']:
        print('SUCCESS')
        pass
    else:
        print('FAILED')
        return render_template("signup.html",message="Recaptcha failed. ")
    
    
    
    if len(request.form['Password'])<8:
        return render_template("signup.html",message="The password should be at least 8 characters")
        
    db=ReadDB()
    InputEmail=((request.form['Email']).replace('.','')).lower()
    for l in db:
        if db[l][1]==InputEmail:
            return render_template("signup.html",message="The email is already taken")
        
    if (request.form['Username']).lower() not in db:
        session['logged_in'] = True
        session["Username"] = request.form['Username']
        AddToDB((request.form['Username']).lower(),(request.form['Password']),((request.form['Email']).replace('.','')).lower())

    else:
        return render_template("signup.html",message="The username is already taken")


    return redirect("/")
    
    
 
 
if __name__ == '__main__':
    app.run(port=8525, debug=True)
