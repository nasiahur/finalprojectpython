from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
import pickle
from keras.models import load_model
import tensorflow as tf

app=Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

app.config.from_object('config')
db=SQLAlchemy(app)

#model_knn=pickle.load(open('app/model_klasifikasi/model_color_knn.sav', 'rb'))
model_cnn=load_model('app/model_klasifikasi/modelcnn.h5')
graph = tf.get_default_graph()

from app import views,models
