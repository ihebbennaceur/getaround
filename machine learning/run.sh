docker run -it\
 -p 4000:4000\
 -v "$(pwd):/home/app"\
 -e APP_URI="s3://mlflow-iheb/artifcat-mlflow/"\
 -e AWS_ACCESS_KEY_ID="AxxxY"\
 -e AWS_SECRET_ACCESS_KEY="Gxxx\
 mlflowiheb python code.py