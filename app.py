# from common.user.models import db, User
from boto3.dynamodb.conditions import Key
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response,
    session,
)
from werkzeug.security import (generate_password_hash,
                               check_password_hash,)
from common.api.api import (ListS3Buckets,
                            ListS3BucketFiles,
                            DeleteS3BucketFile,
                            UploadS3BucketFile,
                            DownloadS3BucketFile, )
from common.aws.gateways.boto import (_client,
                                      )
from common.aws.gateways.s3 import (get_buckets_list,
                                    _get_s3_resource, )
from common.aws.gateways.session import get_bucket, get_region_name
from common.user.forms import (LoginForm,)
from common.run import create_app
from common.user.forms import (RegisterForm,
                               NewBucketForm, )

from flask_login import (login_user,
                          login_required,
                          logout_user,
                          current_user, )
app, api, cur_env, db, login_manager = create_app()


@login_manager.user_loader
def load_user(usernme):
    print('load_user')
    dynamodb = db.dynamodb
    table = dynamodb.Table('sfigiel-dev-aws-upskill-user')
    user = table.query(KeyConditionExpression=Key('Username').eq(usernme))['Items']
    print(user)
    return user


@app.route('/', methods=['GET', 'POST'])
def index(buckets_list=get_buckets_list()):
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = buckets_list
        return render_template("index.html", buckets=buckets, name='test', cur_env=cur_env)


@app.route('/files')
@login_required
def files():
    buckets = get_bucket()
    summaries = buckets.objects.all()
    try:
        return render_template('files.html', my_bucket=buckets,
                               files=summaries, name='test', cur_env=cur_env)
    except:
        return render_template("index.html", buckets=buckets, name='test', cur_env=cur_env)


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['file']
    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file)

    flash('File uploaded successfully')
    return redirect(url_for('files'))


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
@login_required
def download():
    key = request.form['key']
    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


@app.route('/login2', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        dynamodb = db.dynamodb
        table = dynamodb.Table('sfigiel-dev-aws-upskill-user')
        user = table.query(KeyConditionExpression=Key('Username').eq(form.username.data))['Items'][0]
        if user:
            user['is_active'] = True
            login_user(user)
            if check_password_hash(user['Password'], form.password.data):
                return redirect(url_for('index'))

        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        dynamodb = db.dynamodb
        table = dynamodb.Table('sfigiel-dev-aws-upskill-user')
        user = table.query(KeyConditionExpression=Key('Username').eq(form.username.data))['Items']

        if user:
            flash('User has been created already')
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        response = db.client.put_item(
            TableName=db.table_name,
            Item={
                'Username': {'S': form.username.data},
                'Password': {'S': hashed_password},
                'Email': {'S': form.email.data},
            }
        )
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/create_bucket', methods=['GET', 'POST'])
@login_required
def create_bucket():
    form = NewBucketForm()
    client = _client('s3')
    response = client.list_buckets()

    buckets = (bucket['Name'] for bucket in response['Buckets'])

    if form.validate_on_submit():
        current_region = get_region_name()
        bucket_name = str(form.bucket_name.data)
        s3_resource = _get_s3_resource()

        if '_' in bucket_name:
            flash("""Invalid bucket name""")
            return render_template('create_bucket.html', form=form, name='test', cur_env=cur_env)
        if bucket_name not in buckets:
            s3_resource.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        else:
            flash(f'{bucket_name} already exists :( ')
            return render_template('create_bucket.html', form=form, name='test', cur_env=cur_env)

    else:
        return render_template('create_bucket.html', form=form, name='test', cur_env=cur_env)
    return render_template('create_bucket.html', form=form, name='test', cur_env=cur_env)


@app.route('/logout')
@login_required
def logout():
    # logout_user()
    return redirect(url_for('index'))


api.add_resource(ListS3Buckets,
                 '/list/api/v1.0/buckets')
api.add_resource(ListS3BucketFiles,
                 '/list/api/v1.0/buckets/files')
api.add_resource(DeleteS3BucketFile,
                 '/delete/api/v1.0/file')
api.add_resource(UploadS3BucketFile,
                 '/upload/api/v1.0/file')
api.add_resource(DownloadS3BucketFile,
                 '/download/api/v1.0/file')

if __name__ == '__main__':
    app.run(port=8070, host='localhost',debug=True)
