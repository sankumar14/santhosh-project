import os

S3_BUCKET                 = os.environ.get("S3_BUCKET")
S3_KEY                    = os.environ.get("S3_KEY")
S3_SECRET                 = os.environ.get("S3_SECRET")
S3_LOCATION               = 'http://sanbook.s3-us-east-1.amazonaws.com/'.format(sanbook)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 5000