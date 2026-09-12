from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Vehicle API is running",
        "developer": "Awnish",
        "endpoints": {
            "vehicle": "/api/vehicle?number=MH14ML9572"
        }
    })


@app.route("/api", methods=["GET"])
def api_home():
    return jsonify({
        "success": True,
        "message": "Vehicle API endpoint is working"
    })


if __name__ == "__main__":
    app.run()        "Token": ""
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
