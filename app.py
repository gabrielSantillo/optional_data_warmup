import secrets
from flask import Flask, request, make_response
from dbhelpers import run_statement
from apihelpers import check_data_sent
from dbcreds import production_mode
import json

app = Flask(__name__)

@app.patch('/api/client')
def patch_client():
    client_info = run_statement('CALL get_client(?)', [
                                request.headers.get('token')])

    update_info_client = check_data_sent(request.json, [
        'email', 'password', 'bio', 'image_url'], client_info[0])

    results = run_statement('CALL update_info_client(?,?,?,?,?)',
                            [update_info_client['email'], update_info_client['password'],
                             update_info_client['bio'], update_info_client['image_url'], request.headers.get('token')])

    if (type(results) == list and results[0][0] == 1):
        return make_response(json.dumps(results[0][0], default=str), 200)
    elif (type(results) == list and results[0][0] == 0):
        return make_response(json.dumps("Bad request."), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)

##############################################################################################################

if (production_mode):
    print("Running in Production Mode")
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)