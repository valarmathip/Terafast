#!flask/bin/python
from flask import Flask, jsonify
from stats import Rest_Services

app = Flask(__name__)

@app.route('/get_total_stats/<int:startTime>/<int:endTime>/', methods=['GET'])
def get_total_stats(startTime,endTime):
    print "Calling get_total_status with ", startTime, endTime
    resultDict=rest.get_total_stats(startTime, endTime)
    return jsonify(resultDict),201

if __name__ == '__main__':
        rest = Rest_Services('10.6.3.5','root','','flowmon','/home/mravi/dbloader/tf_users.csv')
        app.run(host='10.6.3.5', port=8000,debug=True)
