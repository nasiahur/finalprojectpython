from app import db
import datetime

class Result(db.Model):
	#__tablename__='Result'
	id=db.Column('result_id', db.Integer, primary_key=True)
	tanggal=db.Column(db.String(40))
	nama_file=db.Column(db.String(40))
	hasil_prediksi=db.Column(db.String(10))

	def __init__(self, nama_file, hasil_prediksi):
		now = datetime.datetime.now()
		self.tanggal = now.strftime("%Y-%m-%d %H:%M:%S")
		self.nama_file=nama_file
		self.hasil_prediksi=hasil_prediksi
