# 家庭云盘.py
import requests
import os

print("-家庭云盘v1.0.0正式版-")
ip = 'http://192.168.18.29:5000'

while True:
    try:
        user_input = input(requests.get(ip+'/').text[:-1]+'>')
    except requests.exceptions.ConnectionError as e:
        print('无法连接服务器:{}'.format(e))
        exit(e)

    except (KeyboardInterrupt, EOFError):
        exit(0)

    if user_input == '':
        continue

    if user_input[0:6] != 'system':
        user_input = user_input.split()

    try:
        if user_input[0] == 'mkdir':
            print(requests.get(ip+'/mkdir/'+user_input[1]).text)

        elif user_input[0] == 'cd':
            print(requests.get(ip+'/cd/?dirpath='+user_input[1]).text)

        elif user_input[0] == 'ls':
            print(requests.get(ip+'/ls').text)

        elif user_input[0] == 'dl':
            response = requests.get(ip+'/download/'+user_input[1])
            with open(user_input[1], 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

        elif user_input[0] == 'up':
            with open(user_input[1], 'rb') as file:
                files = {'file': (user_input[1], file)}
                response = requests.post(ip + '/upload', files=files)

        elif user_input[0] == 'rm':
            print(requests.get(ip + '/rm/' + user_input[1]).text)

        elif user_input[0] == 'show':
            if user_input[1] == '-c':
                print(requests.get(ip + '/show/' + user_input[2]).text)
            elif user_input[1] == '-w':
                import webbrowser
                webbrowser.open_new(ip + '/show/' + user_input[2])
                del webbrowser
            else:
                print('参数错误')

        elif user_input[0] == 'cls':
            os.system('clear')

        elif user_input[0:6] == 'system':
            password = input('password:')
            print(requests.get(ip + '/system/?password={}&code={}'.format(password, user_input[7:])).text)

        elif user_input[0] == 'exit':
            raise SystemExit(0)

        elif user_input[0] == 'help':
            print('-帮助-\n'
                  'cd（返回上一级目录：cd ...）、ls、rm、exit都是linux命令的简化版（没有额外参数）的命令，可以自行参照linux的帮助文档\n'
                  'show: 用于在线预览文本文档内容，show <mode> <filename>，mode：-c在终端输出文件内容，-w文件内容转到浏览器打开\n'
                  'up: 用于上传文件，up <filename>\n'
                  'dl: 用于下载服务器上的文件，dl <filename（不支持路径，必须cd）>\n'
                  'cls: 等于clear命令，清屏\nsystem: 执行系统命令，默认密码为123456，system <command>，比如说，你可以使用zip命令来压缩'
                  '，system zip -r uploads/dev.zip uploads/dev')

        else:
            print('没有名为{}的命令'.format(user_input[0]))

    except IndexError:
        print('语法错误')

    except Exception as e:
        print('未知错误:{}'.format(e))
