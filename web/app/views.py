from app import app, db, model_cnn, graph
from flask import Flask, redirect, request, render_template, flash, url_for,session
from werkzeug import secure_filename
import random
import imutils
import numpy as np
import cv2
import keras
import tensorflow as tf
from .models import Result

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
	return render_template('index.html', title='Selamat datang!',error="")


@app.route('/uploader',methods=['GET','POST'])
def uploader():
    allowed_ext=['png','jpg','jpeg','PNG','JPG','JPEG']
    if request.method == 'POST':
        if request.files['file'].filename != '':
            if request.files['file'].filename.split(".")[-1] in allowed_ext:
                f = request.files['file']
                f.save('app/static/img/'+secure_filename(f.filename))
                imagePath = 'app/static/img/'+secure_filename(f.filename)
                image = cv2.imread(imagePath)
                image = cv2.resize(image, (28,28))
                gambar = np.reshape(image, [1, 28, 28, 3])
			
                gambar = gambar.astype('float32')
                gambar = gambar/255.0
                tf.reset_default_graph()
                global graph
                with graph.as_default():
                    a = model_cnn.predict_classes(gambar, batch_size=32) 
				
                if a==0:
                    a='Fire'
                elif a==1:
                    a='Grass'
                elif a==2:
                    a='Water'
				
                result=Result(secure_filename(f.filename), a)
                db.create_all()
                db.session.add(result)
                db.session.commit()
				
                session['hasil'] = a
                session['filename'] = secure_filename(f.filename)
            #return features
                return redirect(url_for('classification_result'))
            else:
                error = "Allowed Extension only : png, jpg and jpeg"
        else:
            error = "No Selected files. Upload your Pokemon's Image!"
    return render_template('index.html',error=error)

	
@app.route('/uploader_',methods=['GET','POST'])
def uploader_():
    if request.method == 'POST':
        if request.files['file'].filename != '':
            f = request.files['file']
            f.save('app/static/img/'+secure_filename(f.filename))
            imagePath = 'app/static/img/'+secure_filename(f.filename)
            image = cv2.imread(imagePath)
            bins=(8, 8, 8)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
            hist = cv2.normalize(hist, hist)

            features = np.array(hist.flatten())
    		
            session['result'] = str(model_knn.predict(features))
            #graph = tf.get_default_graph()
            #return features
            return redirect(url_for('classification_result'))
        else:
            error = "No Selected files. Upload your Pokemon's photo!"
    return render_template('index.html',error=error)

	
@app.route('/classification_result',methods=['GET','POST'])
def classification_result():
    #result = session.get('result',None).replace('[','').replace(']','')
    hasil = session.get('hasil',None)
    filename = session.get('filename',None)
    #return redirect(url_for('dashboard'))
    return render_template('classification_result.html', hasil=hasil, filename=filename)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    #Result.query.delete()
    #for i in db.session.query(Result):
    #    db.session.delete(i)
    #    db.session.commit()		
    return render_template('dashboard.html', query=db.session.query(Result))
