from flask import Flask, jsonify, request
import mysql.connector
from dateutil.parser import parse
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ashes1122",
  database="BayerCrop"
)

# Define Swagger documentation parameters
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Weather Data API'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

# Define a route for getting weather data
@app.route('/api/weather')
def get_weather():
  # Get the start and end date parameters from the query string
  start_date = request.args.get('start_date')
  end_date = request.args.get('end_date')

  # Parse the dates
  start_date = parse(start_date).date() if start_date else None
  end_date = parse(end_date).date() if end_date else None

  # Build the SQL query based on the date parameters
  sql = "SELECT weather_date, max_temp, min_temp, precipitation FROM weather"
  if start_date and end_date:
    sql += f" WHERE weather_date BETWEEN '{start_date}' AND '{end_date}'"
  elif start_date:
    sql += f" WHERE weather_date >= '{start_date}'"
  elif end_date:
    sql += f" WHERE weather_date <= '{end_date}'"

  # Execute the SQL query and get the results
  cursor = db.cursor()
  cursor.execute(sql)
  results = cursor.fetchall()

  # Convert the results to a list of dictionaries
  data = []
  for row in results:
    weather_date, max_temp,min_temp, precipitation = row
    data.append({
      'date': weather_date.strftime('%Y-%m-%d'),
      'max_temp': max_temp,
      'min_temp': min_temp,
      'precipitation': precipitation
    })

  # Return the data as JSON
  return jsonify(data)

if __name__ == '__main__':
  app.run()
