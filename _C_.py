from importlib import reload
from os.path import dirname, basename, isfile, join
import glob
import csv
import sys
from os import mkdir
import Data 
import PIL
from PIL import Image

Card='''
	<div class="col-6 col-sm-12 col-lg-6">
		<div class="card card--list">
			<div class="row">
				<div class="col-12 col-sm-4">
					<div class="card__cover">
						<img src="{Pic}" alt="">
						<a href="#" class="card__play">
							<i class="icon ion-ios-play"></i>
						</a>
					</div>
				</div>

				<div class="col-12 col-sm-8">
					<div class="card__content">
						<h3 class="card__title"><a href="#">{Name}</a></h3>
						<span class="card__category">
							<a href="#">{genere}</a>
							<a href="#">{Secoundgenere}</a>
						</span>

						<div class="card__wrap">
	 						<span class="card__rate"><i class="icon ion-ios-star"></i>{score}</span>

							<ul class="card__list">
								<li>S{Season}</li>
								<li>E{Episode}</li>
								<li>{Min}:{Sec}</li>
							</ul>
						</div>

						<div class="card__description">
							<p>{description}</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>			
	'''

SingleOption='''
	<option >{Name}</option>
 
	'''

def Resize(path):
    baseheight = 350
    img = Image.open(path)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save(path)


def DeleteShow(Username,name):
    D=(ReadData())
    D=D[Username.lower()]
    
    for x in range (len(D)):
        if D[x]['Name']==name:
            D.remove(D[x])
            break 

    Dict=(ReadData())
    Dict[Username.lower()]=D
    ReplaceData(Dict)
    
def ReadDB():
    with open('db.csv', 'r') as f:
        db={}
        for l in list(csv.reader(f)):
            db[l[0]]=[l[1],l[2]]
    return db


def AddToDB(username,password,email):
    with open('db.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([username,password,email])
        


def ReadData():
    reload(Data)
    All= Data.Media
    return All

def ReplaceData(Dict):
    with open('Data.py','w') as f:
        f.write('Media='+str(Dict))
        f.close()

def AddData(Pic,Name,genere,Secoundgenere,score,description,Username):
    D=(ReadData())
    try: D=D[Username.lower()]
    except: D=(ReadData()); D[Username.lower()]=[]; ReplaceData(D); D=(ReadData())[Username.lower()]
    
    D.insert(0,{
        'Pic':Pic,
        'Name':Name,
        'genere':genere,
        'Secoundgenere':Secoundgenere,
        'score':score,
        'description':description,
        'Season':'01',
        'Episode':'01',
        'Min':'00',
        'Sec':'00',
    })
    Dict=(ReadData())
    Dict[Username.lower()]=D
    ReplaceData(Dict)

def UpdateData(Name,Season,Episode,Min,Sec,Username):
    D=(ReadData())[Username.lower()]
    for Media in range (len(D)):
        if D[Media]['Name']==Name:
            if Season!='':
                D[Media]['Season']=Season
            if Episode!='':
                D[Media]['Episode']=Episode
            if Min!='':
                D[Media]['Min']=Min
            if Sec!='':
                D[Media]['Sec']=Sec

            break
        
    Dict=(ReadData())
    Dict[Username.lower()]=D
    ReplaceData(Dict)
    

def AllSeriesSelectCode(username):
    Code=''
    D=(ReadData())[username.lower()]
    for Media in range (len(D)):
        Code+=SingleOption.format(Name=D[Media]['Name'])

    return Code

def AllCards(Username):
    Code=''
    D=(ReadData())
    try: D=D[Username.lower()]
    except: D[Username.lower()]=[]; ReplaceData(D); D=(ReadData())[Username.lower()]
    
    for Media in range (len(D)):
        MediaDetail=D[Media]
        Code+=Card.format( 
    
            Pic=MediaDetail['Pic'],
            Name=MediaDetail['Name'],
            genere=MediaDetail['genere'],
            Secoundgenere=MediaDetail['Secoundgenere'],
            score=MediaDetail['score'],
            Season=MediaDetail['Season'],
            Episode=MediaDetail['Episode'],
            Min=MediaDetail['Min'],
            Sec=MediaDetail['Sec'],
            description=MediaDetail['description'],
        )
    return Code
 