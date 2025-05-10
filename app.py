from flask import Flask, jsonify, render_template
from google.cloud import bigquery
import os

app = Flask(__name__)

# Initialize BigQuery Client
project_id = os.environ.get("GCP_PROJECT_ID", "sound-essence-458113-d7")
client = bigquery.Client(project=project_id)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/revenue-by-category")
def revenue_by_category():
    query = """
    SELECT 
      product_category,
      gender,
      SUM(total_sales) AS total_revenue
    FROM 
      `sound-essence-458113-d7.thelook.ProductBasedRevenue`
    GROUP BY 
      product_category, gender
    ORDER BY 
      total_revenue DESC
    LIMIT 10
    """
    results = client.query(query).result()
    data = [dict(row) for row in results]
    return jsonify(data)

@app.route("/shipping-delay")
def shipping_delay():
    query = """
    SELECT 
      state,
      ROUND(AVG(avg_shipping_days), 2) AS avg_days_to_ship
    FROM 
      `sound-essence-458113-d7.thelook.shippingDelayAnalysisByState`
    GROUP BY 
      state
    ORDER BY 
      avg_days_to_ship DESC
    LIMIT 10
    """
    results = client.query(query).result()
    data = [dict(row) for row in results]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
