from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TARGET_URL = "https://www.smcinsurance.com/central/centralcall/CallReqWithHeader"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": True,
        "message": "Vehicle API is running",
        "endpoint": "/api/vehicle"
    })


@app.route("/api/vehicle", methods=["GET", "POST"])
def vehicle():

    if request.method == "GET":
        vehicle_no = request.args.get("number", "").strip().upper()
    else:
        data = request.get_json(silent=True) or {}
        vehicle_no = str(data.get("number", "")).strip().upper()

    if not vehicle_no:
        return jsonify({
            "status": False,
            "error": "Vehicle number is required"
        }), 400

    payload = {
        "URL": "GetVaahanDetailsByVehicleNo",
        "Props": [vehicle_no],
        "Token": ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://www.smcinsurance.com",
        "Referer": "https://www.smcinsurance.com/"
    }

    try:
        response = requests.post(
            TARGET_URL,
            json=payload,
            headers=headers,
            timeout=20
        )

        try:
            result = response.json()
        except ValueError:
            result = {
                "raw_response": response.text
            }

        return jsonify({
            "status": response.ok,
            "vehicle_number": vehicle_no,
            "data": result
        }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            "status": False,
            "error": "Upstream request timed out"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": False,
            "error": "Upstream request failed",
            "details": str(e)
        }), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
      )
