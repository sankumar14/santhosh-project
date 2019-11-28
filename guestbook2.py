from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET

s3 = boto3.client(
	's3',
	aws_access_key_id=S3_KEY,
	aws_secret_access_key=S3_SECRET
	)

app = Flask(__name__)
# Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin1234@guestbook-1.ch4uderhegxd.us-east-1.rds.amazonaws.com/commentdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object("config")

db = SQLAlchemy(app)

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	comment = db.Column(db.String(1000))
	attachment = db.Column(db.String(1000))

@app.route('/')
def index():
	result = Comments.query.all()

	return render_template('index.html', result=result)

@app.route('/sign')
def sign():
	return render_template('sign.html')


	signature = Comments(name=name, comment=comment)
	db.session.add(signature)
	db.session.commit()
	
	return redirect(url_for('index'))

@app.route('/process', methods=['POST'])
def process():
	name = request.form['name']
	comment = request.form['comment']
	# attachment = request.form['attachment']
def upload_file_to_s3(file, bucket_name, acl="public-read"):

			try:

				s3.upload_fileobj(
					file,
					bucket_name,
					file.filename,
					ExtraArgs={
						"Acl": acl,
						"ContentType": file.content_type

					}
				)
			
			except Exception as e:
				print("Something Happened: ", e)
				return e

			return "{}{}".format(app.config["S3_LOCATION"], file.filename)	

# @app.route('/files')
# def files():
# 	s3_resource = boto3.reource('s3')
# 	my_bucket = s3_resource.Bucket(S3_BUCKET)
# 	summaries = my_bucket.objects.all()

# 	return render_template('files.html', my_bucket=my_bucket, files=summaries)

# @app.route('/home', methods=['GET','POST'])
# def home():
#     links = ['https://www.youtube.com','https://www.spotify.com']
#     return render_template ('index.html', links=links)  

if __name__=='__main__':
    app.run(debug=True)