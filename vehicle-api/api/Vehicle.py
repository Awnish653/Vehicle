import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TARGET_URL = (
    "https://www.smcinsurance.com/"
    "central/centralcall/CallReqWithHeader"
)


@app.route("/", methods=["GET", "POST"])
@app.route("/api/vehicle", methods=["GET", "POST"])
def vehicle():

    # -----------------------------
    # GET request
    # -----------------------------
    if request.method == "GET":
        vehicle_number = request.args.get(
            "number",
            ""
        ).strip().upper()

    # -----------------------------
    # POST request
    # -----------------------------
    else:
        body = request.get_json(
            silent=True
        ) or {}

        vehicle_number = str(
            body.get("number", "")
        ).strip().upper()

    # -----------------------------
    # Validate vehicle number
    # -----------------------------
    if not vehicle_number:
        return jsonify({
            "success": False,
            "error": "Vehicle number is required",
            "example": "/api/vehicle?number=MH14ML9572"
        }), 400

    # -----------------------------
    # Request payload
    # -----------------------------
    payload = {
        "URL": "GetVaahanDetailsByVehicleNo",
        "Props": [
            vehicle_number
        ],
        "Token": ""
    }

    # -----------------------------
    # Headers
    # -----------------------------
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

        # -----------------------------
        # Try JSON response
        # -----------------------------
        try:
            result = response.json()

        except (ValueError, json.JSONDecodeError):
            result = {
                "raw_response": response.text
            }

        # -----------------------------
        # Return response
        # -----------------------------
        return jsonify({
            "success": response.ok,
            "vehicle_number": vehicle_number,
            "http_status": response.status_code,
            "data": result
        }), response.status_code

    except requests.exceptions.Timeout:

        return jsonify({
            "success": False,
            "vehicle_number": vehicle_number,
            "error": "Target server timed out"
        }), 504

    except requests.exceptions.RequestException as error:

        return jsonify({
            "success": False,
            "vehicle_number": vehicle_number,
            "error": "Request failed",
            "details": str(error)
        }), 502

    except Exception as error:

        return jsonify({
            "success": False,
            "vehicle_number": vehicle_number,
            "error": "Internal server error",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run()
