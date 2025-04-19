from flask import Flask, request, jsonify
import os
import hashlib
import requests

app = Flask(__name__)
SECRET_KEY = "c0nc3rt-secret"

def is_license_valid(provided_key):
    expected = hashlib.sha256(("valid-client-" + SECRET_KEY).encode()).hexdigest()
    return provided_key == expected

@app.route("/", methods=["POST"])
def concert_alert_proxy():
    license_key = os.getenv("LICENSE_KEY")
    if not license_key or not is_license_valid(license_key):
        return jsonify({"error": "Clé de licence invalide ou manquante."}), 403

    data = request.json
    message = data.get("message", "🎟️ Nouvelle alerte de concert")

    pushover_token = os.getenv("PUSHOVER_TOKEN")
    pushover_user = os.getenv("PUSHOVER_USER")
    if pushover_token and pushover_user:
        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": pushover_token,
            "user": pushover_user,
            "message": message
        })

    discord_url = os.getenv("DISCORD_WEBHOOK_URL")
    if discord_url:
        requests.post(discord_url, json={"content": message})

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)