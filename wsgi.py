from api.index import app
import os

PORT = os.getenv("PORT", "5000")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)