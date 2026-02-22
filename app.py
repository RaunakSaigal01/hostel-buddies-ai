from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Load data once
df = pd.read_excel("Cleaned_Room_AI.xlsx")

# GPA mapping
def get_gpa_range(gpa):
    if gpa >= 9.5:
        return "9.5+"
    elif 9 <= gpa < 9.5:
        return "9-9.5"
    elif 8.5 <= gpa < 9:
        return "8.5-9"
    elif 8 <= gpa < 8.5:
        return "8+"
    elif 7 <= gpa < 8:
        return "7+"
    elif 6 <= gpa < 7:
        return "6+"
    elif 1<= gpa <6:
            return "<6"
    else:
        return "0"

@app.route("/check-availability", methods=["POST"])
def check_availability():
    data = request.json
    year = str(data.get("year")).strip()
    gpa = float(data.get("gpa"))
    block = str(data.get("block")).strip()

    gpa_range = get_gpa_range(gpa)

    # Filter data
    filtered = df[
        (df["Year"].astype(str).str.strip() == year) &
        (df["GPA Range"] == gpa_range) &
        (df["Block"].astype(str).str.strip() == block)
    ]

    if filtered.empty:
        return jsonify({
            "success": False,
            "message": f"No data found for GPA less than 1."
        })

    # Prepare results
    results = []
    for _, row in filtered.iterrows():
        results.append({
            "room": row["Room"],
            "chances": f"{int(round(row['Availability'] * 100))}%"
        })

    return jsonify({
        "success": True,
        "year": year,
        "gpa_range": gpa_range,
        "block": block,
        "results": results
    })



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
