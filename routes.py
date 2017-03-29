# RESTful API using FLASK & MYSQLDB
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import MySQLdb

app = Flask(__name__)
api = Api(app)
db = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='mel',
    db='berpesan')
cursor = db.cursor()

class SMS(Resource):
    def get(self):
        try:
            query = 'SELECT ts.id_trend, ts.sms_content, ts.jlh_laporan, ' \
                    'COUNT(id_trend_sms) AS jlh_comment ' \
                    'FROM trending_sms ts ' \
                    'LEFT JOIN trending_sms_comment tsc ' \
                    'ON ts.id_trend = tsc.id_trend_sms ' \
                    'GROUP BY ts.id_trend ' \
                    'ORDER BY jlh_laporan DESC ' \
                    'LIMIT 10'
            cursor.execute(query)
            data = cursor.fetchall()
            sms = []
            for i in data:
                result = {
                    'id_tren_spam': i[0],
                    'konten_spam': i[1],
                    'jlh_laporan': i[2],
                    'jlh_komentar': i[3]
                }
                sms.append(result)
            return jsonify(trending_spam=sms)

        except Exception as e:
            return {'error': str(e)}

class User(Resource):
    def get(self):
        try:
            username = request.args.get('username')
            password = request.args.get('password_hash')
            query = 'SELECT username ' \
                    'FROM user ' \
                    'WHERE username = %s AND password_hash = %s '
            cursor.execute(query, (username, password))
            data = cursor.fetchall()

            if username in data:
                result = {
                    'message': 'log in successful'
                }

            return jsonify(message=result)

        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            username = request.args.get('username')
            password = request.args.get('password')
            query = 'INSERT INTO user (username, password_hash) ' \
                    'VALUES (%s,%s)'
            cursor.execute(query, (username, password))
            db.commit()
            return {'createUser': 'OK'}, 201

        except Exception as e:
            return {'error': str(e)}

class Comments(Resource):
    def get(self):
        try:
            id_spam_trend = request.args.get('id_spam_trend')
            query = 'SELECT ts.id_trend, username, sms_comment, created_at ' \
                    'FROM trending_sms ts JOIN trending_sms_comment tsc ' \
                    'ON ts.id_trend = tsc.id_trend_sms ' \
                    'JOIN user u ' \
                    'ON tsc.created_by = u.id ' \
                    'WHERE tsc.id_trend_sms = %s'
            cursor.execute(query, id_spam_trend)
            data = cursor.fetchall()
            comment = []
            for i in data:
                result = {
                    'id_tren_sms': i[0],
                    'username': i[1],
                    'sms_comment': i[2],
                    'created_at': i[3]
                }
                comment.append(result)
            return jsonify(comments=comment)

        except Exception as e:
            return {'errorGetComment': str(e)}

    def post(self):
        try:
            id_trend = request.args.get('id_trend_sms')
            created_by = request.args.get('created_by')
            comment = request.args.get('sms_comment')
            query = 'INSERT INTO trending_sms_comment (id_trend_sms, created_by, sms_comment, created_at) ' \
                    'VALUES (%s, %s, %s, NOW())'
            cursor.execute(query, (id_trend, created_by, comment))
            db.commit()
            return {'createComment': 'OK'}, 201

        except Exception as e:
            return {'errorCreateComment': str(e)}

# API ENDPOINTS
api.add_resource(Comments, '/berpesan/comment', endpoint='comment')
api.add_resource(SMS, '/berpesan/spamtrend', endpoint='spamtrend')
api.add_resource(User, '/berpesan/user', endpoint='user')


if __name__ == '__main__':
  app.run(debug=True, port=5005)