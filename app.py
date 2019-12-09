from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET
from filters import datetimeformat, file_type

s3 = boto3.client(
	's3',
	aws_access_key_id=S3_KEY,
	aws_secret_access_key=S3_SECRET
	)

app = Flask(__name__)
Bootstrap(app)
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type
app.secret_key ='secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin1234@guestbook-1.ch4uderhegxd.us-east-1.rds.amazonaws.com/commentdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config.from_object("config")

db = SQLAlchemy(app)

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	comment = db.Column(db.String(1000))

@app.route('/')
def index():

	result = Comments.query.all()

	return render_template('index.html', result=result)

@app.route('/sign')
def sign():

	s3_resource = boto3.resource('s3')
	my_bucket = s3_resource.Bucket(S3_BUCKET)
	summaries = my_bucket.objects.all()

	return render_template('sign.html', my_bucket=my_bucket, files=summaries)

@app.route('/process', methods=['POST'])
def process():
	name = request.form['name']
	comment = request.form['comment']
	
	
	signature = Comments(name=name, comment=comment)
	db.session.add(signature)
	db.session.commit()

	return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']

	s3_resource = boto3.resource('s3')
	my_bucket = s3_resource.Bucket(S3_BUCKET)
	my_bucket.Object(file.filename).put(Body=file)

	flash('File/s uploaded successfully')

	return redirect(url_for('sign'))

@app.route('/delete', methods=['POST'])
def delete():

	key = request.form['key']

	s3_resource = boto3.resource('s3')
	my_bucket = s3_resource.Bucket(S3_BUCKET)
	my_bucket.Object(key).delete()

	flash('File deleted successfully')

	return redirect(url_for('files'))

@app.route('/download', methods=['POST'])
def download():
	key = request.form['key']

	s3_resource = boto3.resource('s3')
	my_bucket = s3_resource.Bucket(S3_BUCKET)

	file_obj = my_bucket.Object(key).get()

	return Response(
		file_obj['Body'].read(),
		mimetype='text/plain',
		headers={"Content-Disposition": "attachment;filename={}.format(key)"}
		)

@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/files')
def files():
	s3_resource = boto3.resource('s3')
	my_bucket = s3_resource.Bucket(S3_BUCKET)
	summaries = my_bucket.objects.all()

	return render_template('files.html', my_bucket=my_bucket, files=summaries)

if __name__=='__main__':
    app.run(debug=True)