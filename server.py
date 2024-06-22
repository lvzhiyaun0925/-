import subprocess
from flask import Flask, request, redirect, url_for, send_file
import os
import shutil
import pickle

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # 上传文件的保存路径
path: str = os.getcwd() + '/uploads/'
user_list = []
try:
    os.mkdir('uploads')
except FileExistsError:
    pass

try:
    with open('data.pkl', 'rb') as f:
        try:
            user_list = pickle.load(f)
            print(user_list)
        except EOFError:
            pass

except FileNotFoundError:
    open('data.pkl', 'w').close()
except pickle.UnpicklingError:
    print("Error unpickling the data.")


@app.route('/')
def upload_form():
    if request.remote_addr not in user_list:
        user_list.append(request.remote_addr)
        print(f'来自{request.remote_addr}的新用户')
        with open('data.pkl', 'wb') as file:
            pickle.dump(user_list, file)
    return path


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file.save(path+file.filename)
        return redirect(url_for('upload_success', filename=file.filename))


@app.route('/download/<filename>')
def download_file(filename):
    file_path = path+filename
    return send_file(file_path, as_attachment=True)


@app.route('/mkdir/<dirname>')
def mkdir(dirname):
    os.mkdir(path+dirname)
    return 'OK'


@app.route('/cd/')
def cd():
    global path
    dirname = request.args.get('dirpath')

    old_path = path
    path = os.path.abspath(os.path.join(path, dirname)) + '/'
    if not os.path.exists(path):
        path = old_path
        return '没有那个目录！'
    return 'OK'


@app.route('/ls')
def ls():
    return str(os.listdir(path))


@app.route('/rm/<filename>')
def rm(filename):
    if os.path.isdir(path+filename):
        shutil.rmtree(path+filename)
    else:
        os.remove(path+filename)

    return 'OK'


@app.route('/show/<filename>')
def show(filename):
    with open(path+filename, 'r') as file:
        return file.read()


@app.route('/system/')
def system():
    if request.args.get('password') != 'helloworld':
        return '密码错误'
    command = request.args.get('code')
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        output = result.stdout
        error = result.stderr
        if error:
            return f"错误: {error}"
        return output
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.stderr}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
