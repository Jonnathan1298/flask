from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources=r"/*")
try:
	connection = pymysql.connect(host='monorail.proxy.rlwy.net',
                             port= 15272,
                             user='root',
                             password='RJMuFPwhlZPrJpgJpQLkCLJHjDfCJVap',
                             db='railway')
	print("Conexión correcta")
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)

cur = connection.cursor()






@app.route('/')
def state_server():
   return 'Server processing'

@app.route('/get-tickets', methods=['GET'])
def get_tickets():
      if request.method == 'GET':
         cur.execute("SELECT  * FROM tickets")
         result = cur.fetchall()
         return  jsonify(result)

@app.route('/insert-tickets', methods = ['POST'])
def insertTickets():
   if request.method == 'POST':
      data = request.json
      cur.execute("""
               INSERT INTO TICKETS(REGISTRATION, CODE_SPACE, ZONE, SQUARE, VEHICLE, HOURS, DATE_ENTRY, DATE_DEPARTURE, PRICE, ID) 
	            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
               (data['registration'],data['code'],data['zone'],data['square'],data['tyteVehicle'],data['hours'],data['entry'],data['departure'],data['price'],data['idOfficial'])
               )
      connection.commit()
      connection.close()
      print(data['entry'])
      return jsonify(data)

@app.route('/get-number-ticket')
def getNumberTicket():
      cur.execute("SELECT  COUNT(*) FROM TICKETS")
      result = cur.fetchall()
      return  jsonify(result)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=1998, debug=True)
