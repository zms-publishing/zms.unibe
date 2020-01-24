from flask import Flask, request, redirect, render_template
from flask_zodb import ZODB, List

app = Flask(__name__)
app.config['ZODB_STORAGE'] = 'zeo://zeo-zodb-storage:9100'

db = ZODB(app)


@app.before_request
def set_db_defaults():
    if 'entries' not in db:
        db['entries'] = List()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db['entries'].append(request.form['message'])
        return redirect('/')
    else:
        message = db.get('entries', 'Be the first to shout!')
        return render_template('index.html', message=message)


@app.route('/show')
def show_entries():
    #zmsobj = db['entries']
    zmsobj = db['Application']['myzmsx']['content']
    #zmsobj = db['Application']['unibe']['content']
    print(zmsobj)
    print(zmsobj.getMetaobjIds())
    print(zmsobj.attr('title'))
    output = []
    nodes = zmsobj.getTreeNodes(meta_types=['ZMSDocument', 'ZMSTextarea', 'ZMSGraphic', 'LgBootstrapSlide'])
    for node in nodes:
        title = node.attr('title', REQUEST={'lang': 'ger'})
        output.append(title)

        from Products.zms._blobfields import MyBlob
        titleimg = node.attr('titleimage', REQUEST={'lang': 'eng'})
        if isinstance(titleimg, MyBlob):
            output.append(titleimg.getHref(REQUEST={'lang': 'eng'}))
        img = node.attr('img', REQUEST={'lang': 'ger'})
        if isinstance(img, MyBlob):
            output.append(img.getHref(REQUEST={'lang': 'ger'}))
        image = node.attr('image', REQUEST={'lang': 'ger'})
        if isinstance(image, MyBlob):
            output.append(image.getHref(REQUEST={'lang': 'ger'}))

    return render_template('show_entries.html', entries=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
