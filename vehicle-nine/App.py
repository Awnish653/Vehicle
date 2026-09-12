from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TARGET_URL = "https://www.smcinsurance.com/central/centralcall/CallReqWithHeader"


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "Vehicle API is running",
        "usage": "/vehicle?number=MH14ML9572"
    })


@app.route("/vehicle")
def vehicle():
    number = request.args.get("number", "").strip().upper()

    if not number:
        return jsonify({
            "success": False,
            "error": "Vehicle number is required",
            "example": "/vehicle?number=MH14ML9572"
        }), 400

    payload = {
        "URL": "GetVaahanDetailsByVehicleNo",
        "Props": [number],
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
            data = response.json()
        except ValueError:
            data = {
                "raw_response": response.text
            }

        return jsonify({
            "success": response.ok,
            "vehicle_number": number,
            "http_status": response.status_code,
            "data": data
        }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "error": "Target server timed out"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": "Request failed",
            "details": str(e)
        }), 502


if __name__ == "__main__":
    app.run()
