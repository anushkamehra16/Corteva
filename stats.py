from flask import Flask, jsonify, request
import mysql.connector
from dateutil.parser import parse
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
  host="localhost",
  user="<username>",
  password="<password>",
  database="<database>"
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

# Define a route for getting weather data statistics
@app.route('/api/weather/stats')
def get_weather():
  # Get the start and end year parameters from the query string
  start_year = request.args.get('start_year')
  end_year = request.args.get('end_year')

  # Build the SQL query based on the date parameters
  sql = "SELECT year, avg_max_temperature, avg_min_temperature, total_precipitation FROM yearly_weather_stats"
  if start_year and end_year:
    sql += f" WHERE year BETWEEN '{start_year}' AND '{end_year}'"
  elif start_year:
    sql += f" WHERE year >= '{start_year}'"
  elif end_year:
    sql += f" WHERE year <= '{end_year}'"

  # Execute the SQL query and get the results
  cursor = db.cursor()
  cursor.execute(sql)
  results = cursor.fetchall()

  # Convert the results to a list of dictionaries
  data = []
  for row in results:
    year, avg_max_temperature,avg_min_temperature, total_precipitation = row
    data.append({
      'year': year,
      'avg_max_temperature': avg_max_temperature,
      'avg_min_temperature': avg_min_temperature,
      'total_precipitation': total_precipitation
    })

  # Return the data as JSON
  return jsonify(data)

if __name__ == '__main__':
  app.run()
