from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

TARGET_URL = "https://www.smcinsurance.com/central/centralcall/CallReqWithHeader"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Vehicle API is running",
        "usage": "/vehicle?number=MH14ML9572"
    })


@app.route("/vehicle", methods=["GET"])
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

        # First try to parse the upstream response as JSON
        try:
            data = response.json()
        except ValueError:
            data = response.text

        # Sometimes upstream returns JSON as a STRING.
        # Convert that string back into a real JSON object.
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except (json.JSONDecodeError, TypeError):
                pass

        # Return the COMPLETE upstream response
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
    app.run()        "User-Agent": "Mozilla/5.0",
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

        # Get the complete response
        try:
            data = response.json()
        except ValueError:
            data = {
                "raw_response": response.text
            }

        # If upstream returned JSON inside a string,
        # decode it so the complete response becomes proper JSON.
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except (json.JSONDecodeError, TypeError):
                pass

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
