from flask import Flask, request, send_file, render_template, json
import requests
import base64
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html', flag=False, errorflag=False)

    elif request.method == 'POST':
        patient_id = request.form.get('patientId')
        task = request.form.get('task')
        try:
            headers = {'content-type': 'application/json'}
            fhir_url = 'http://gt-apps.hdap.gatech.edu/gt-fhir/fhir/DocumentReference?patient=%s' % (patient_id)
            response = requests.get(fhir_url, headers=headers)
            data = response.json()

            if data['resourceType'] == 'Bundle':
                if data['total'] == 0:
                    error = "No documents for this patient"
                    return render_template('index.html', error=error, flag=False, errorflag=True)
                else:
                    reports = []
                    for entry in data['entry']:
                            content = entry['resource']['content']
                            for attachment in content:
                                report_text = base64.b64decode(attachment['attachment']['data']).decode('utf-8')
                                reports.append(report_text)


            # Constructing ClarityNLPaaS request
            payload = dict()
            payload['reports'] = reports
            url = 'http://localhost:5000/job/%s' %(task)
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            data = response.json()
            return render_template('index.html', json=data, flag=True, errorflag=False)
        except:
            error = "Internal Server Error"
            return render_template('index.html', error=error, flag=False, errorflag=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, threaded=True)
