import base64
from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("data/sales.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Products (
                    product_id TEXT PRIMARY KEY,
                    product_name TEXT,
                    category TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT,
                    sales_amount REAL,
                    units_sold INTEGER,
                    region TEXT,
                    customer_age INTEGER,
                    FOREIGN KEY(product_id) REFERENCES Products(product_id)
                )''')
    conn.commit()
    conn.close()

# Route: Home Page (displaying statistics and chart)
@app.route("/")
def index():
    conn = sqlite3.connect("data/sales.db")
    df = pd.read_sql_query("SELECT * FROM Sales", conn)
    conn.close()

    if df.empty:
        stats = {
            "sales_mean": None,
            "sales_median": None,
            "sales_std": None,
            "units_mean": None,
            "age_mean": None
        }
        chart_img = None
    else:
        stats = {
            "sales_mean": df["sales_amount"].mean(),
            "sales_median": df["sales_amount"].median(),
            "sales_std": df["sales_amount"].std(),
            "units_mean": df["units_sold"].mean(),
            "age_mean": df["customer_age"].mean()
        }
        
        # Generate chart
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(df["sales_amount"], kde=True, ax=ax)
        ax.set_title("Sales Amount Distribution")
        plt.tight_layout()

        # Save chart to a BytesIO object and convert to base64
        output = io.BytesIO()
        plt.savefig(output, format="png")
        output.seek(0)
        chart_img = base64.b64encode(output.getvalue()).decode('utf-8')  # Convert to base64 string

    return render_template("index.html", stats=stats, chart_img=chart_img)

# Route: Handle Form Submission
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    product_id = data["product_id"]
    product_name = data["product_name"]
    category = data["category"]
    sales_amount = data["sales_amount"]
    units_sold = data["units_sold"]
    region = data["region"]
    customer_age = data["customer_age"]

    conn = sqlite3.connect("data/sales.db")
    c = conn.cursor()

    # Insert Product Data
    c.execute("INSERT OR IGNORE INTO Products (product_id, product_name, category) VALUES (?, ?, ?)",
              (product_id, product_name, category))

    # Insert Sales Data
    c.execute('''INSERT INTO Sales (product_id, sales_amount, units_sold, region, customer_age) 
                 VALUES (?, ?, ?, ?, ?)''',
              (product_id, sales_amount, units_sold, region, customer_age))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data saved successfully!"})

# Route: Generate Statistics (for AJAX)
@app.route("/stats")
def stats():
    conn = sqlite3.connect("data/sales.db")
    df = pd.read_sql_query("SELECT * FROM Sales", conn)
    conn.close()

    if df.empty:
        return jsonify({"message": "No data available for analysis."})

    stats = {
        "sales_mean": df["sales_amount"].mean(),
        "sales_median": df["sales_amount"].median(),
        "sales_std": df["sales_amount"].std(),
        "units_mean": df["units_sold"].mean(),
        "age_mean": df["customer_age"].mean()
    }
    return jsonify(stats)

# Route: Generate Chart (for AJAX)
@app.route("/chart")
def chart():
    conn = sqlite3.connect("data/sales.db")
    df = pd.read_sql_query("SELECT * FROM Sales", conn)
    conn.close()

    if df.empty:
        return "No data for visualization."

    # Generate chart
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(df["sales_amount"], kde=True, ax=ax)
    ax.set_title("Sales Amount Distribution")
    plt.tight_layout()

    output = io.BytesIO()
    plt.savefig(output, format="png")
    output.seek(0)
    return send_file(output, mimetype="image/png")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
