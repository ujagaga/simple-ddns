from flask import Flask, redirect, request, abort
from os import urandom, path
import sys

sys.path.insert(0, path.dirname(__file__))

SERVER_SECRET = "qwerty123"
SUBDOMAIN_FILE_PATH = "sdlist.txt"
 
application = Flask(__name__, subdomain_matching=True)
application.config['SERVER_NAME'] = "ocddns.tk"
application.config['SESSION_COOKIE_DOMAIN'] = "ocddns.tk"


def update_subdomain(subdomain, address, operation=''):
    result = 'OK'

    if not path.isfile(SUBDOMAIN_FILE_PATH):
        sf = open(SUBDOMAIN_FILE_PATH, 'w')
        sf.close()

    # An SSD drive can take a lot of read operation, but limited number of writes.
    # So lets first check if we already have everything as needed before we decide to write.
    with open(SUBDOMAIN_FILE_PATH, 'r') as sf:
        lines = sf.readlines()

    line_index = -1
    key = subdomain + '='
    sd_line = key + address

    for i in range(0, len(lines)):
        if lines[i].startswith(key):
            line_index = i
            break

    change_required_flag = False

    if operation.startswith('remove'):
        if line_index < 0:
            result = "Not found"
        else:
            lines.pop(line_index)
            change_required_flag = True

    else:
        if line_index < 0:
            # the subdomain was not found
            lines.append(sd_line)
            change_required_flag = True
            result = 'OK:{0}'.format(address)

        elif not lines[line_index].startswith(sd_line):
            # change is required
            lines[line_index]
            change_required_flag = True

    if change_required_flag:
        with open(SUBDOMAIN_FILE_PATH, 'w') as sf:
            for line in lines:
                line = line.replace('\n', '').replace('\r', '') + '\n'
                sf.write(line)

    return result


def query_subdomain(subdomain):
    result = None

    try:
        with open(SUBDOMAIN_FILE_PATH, 'r') as sf:
            lines = sf.readlines()

        line_index = -1
        key = subdomain + '='

        for i in range(0, len(lines)):
            if lines[i].startswith(key):
                line_index = i
                break

        if line_index > -1:
            result = lines[line_index].replace('\n', '').replace('\r', '').split('=')[1]

    except Exception as e:
        print(e)
        pass

    return result


@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def home(path):
    ret_val = '''
            <h1>Ohana Code DDNS</h1>
            <br><h2>This is a one user, query based updated dynamic dns service.</h2><br><br>
            What you have to know to use it is the server secret key, which is a password like, at least 8 (recomended, but not required) characters long, alphanumeric string. Eg. qwerty123<br><br>
            To add or update a sub-domain, make a get request to something like:<br>
            <strong>https://mysubdomain.thisddnsservice.com/?secret=qwerty123</strong>
            <br><br>
            to remove a sub-domain, make a get request to:<br> 
            <strong>https://mysubdomain.thisddnsservice.com/?secret=qwerty123&op=remove</strong><br><br>    
            '''
    if path != '':
        return ret_val + "<br><br><b>WARNING:</b><p>The page you are looking for ({0}) was not found on this server</p>".format(path), 404
    else:
        return ret_val


@application.route("/", subdomain="<sub>")
def sub_index(sub):
    
    secret = request.args.get("secret")
    op = request.args.get("op")
    if op is None:
        op = ''

    if secret is not None and secret == SERVER_SECRET:
        # Authorized
        result = update_subdomain(sub, request.remote_addr, op)

        return result
    else:
        ip_addr = query_subdomain(sub)

        if ip_addr is None:
            # return abort(404)
            return "<h1>Ohana Code DDNS</h1><p>Sorry, the page you are looking for was not found on this server.</p>", 404
        else:
            redirect_url = request.url.split('://')[0] + '://' + ip_addr
            return redirect(redirect_url)
            
            
application.secret_key = urandom(12)

if __name__ == '__main__':
    application.secret_key = urandom(12)
    application.run()					# for hosting deployment
    # app.run(debug=True, host='0.0.0.0', port=4000)  	# for localhost and debugging
