# ::: interlink

## ::: interlink.formulator

## ::: interlink.templeton

## ::: interlink.safeHaven

## ::: interlink.toolkit

``` python
templates = os.path.dirname(__file__) + '/templates/'
templetonBP = Blueprint('templeton', __name__, url_prefix='/', template_folder=templates)
@templetonBP.errorhandler(404)
@templetonBP.errorhandler(500)
@templetonBP.route('/guide/<page>')
@templetonBP.route('/interlink/')
@templetonBP.route('/loginRequired/', methods=['GET', 'POST'])
@templetonBP.route('/login/', methods=['GET', 'POST'])
@templetonBP.route('/register/', methods=['GET', 'POST'])
@templetonBP.route('/reports/<db>/<page>')
@templetonBP.route('/forms/<db>/<page>', methods=['GET', 'POST'])
@templetonBP.route('/admin/<db>')
```
