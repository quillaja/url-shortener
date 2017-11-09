import json
from flask import Flask, request, abort, redirect, render_template
from model import Link

app = Flask(__name__)


def get_link_info(key: str) -> dict:
    result = Link.select().where(Link.key == key)
    if len(result) == 0:
        return None

    lnk = result[0]
    dtfmt = '%Y-%m-%dT%H:%M'

    output = {
        'url': lnk.url,
        'key': lnk.key,
        'clicked': lnk.clicked,
        'modified': lnk.modified.strftime(dtfmt),
        'created': lnk.created.strftime(dtfmt)
    }

    return output


#################################################################
# Does back-end api work.
# Can be accessed through html-based client or programattically.
#################################################################


@app.route('/api/urls', methods=['POST'])
def do_new():
    '''
    Used to get new shortened urls.
    New url is to be POSTed with JSON body '{"url": <url>}'.
    If everything is correct, a JSON response is sent with the url and key.
    '''

    if request.method == 'POST':  # <--- Needed?
        data = json.loads(request.data)
        if 'url' in data:
            url = data['url']
            result = Link.select().where(Link.url == url)
            if len(result) == 0:
                lnk = Link.create(url=url)
                key = lnk.key
            else:
                key = result[0].key

            return json.dumps({'key': key, 'url': url})

    abort(404)


@app.route('/api/urls/<string:key>', methods=['GET'])
def do_link_info(key):
    output = get_link_info(key)
    if output is None:
        abort(404)

    return json.dumps(output)


#########################################################################
# Takes care of website front-end using templates
#########################################################################


@app.route('/', methods=['GET'])
def do_landing_page():
    return render_template('landing-page.html')


@app.route('/urls/<string:key>', methods=['GET'])
def do_link_info_page(key):
    return render_template('info-page.html', output=get_link_info(key))


#########################################################################
# Does redirect... half front-end, half api
#########################################################################


@app.route('/<string:key>', methods=['GET'])
def do_redirect(key):
    '''
    Redirects to the url linked with the given key.
    '''

    result = Link.select().where(Link.key == key)

    if len(result) == 0:
        abort(404)

    lnk = result[0]
    lnk.clicked += 1  # increment number of times this link has been used
    lnk.save()

    return redirect(lnk.url)
