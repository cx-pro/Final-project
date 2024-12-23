from app import app
from app import http_server


if __name__ == "__main__":
    print("running")
    http_server.serve_forever()
    app.run("0.0.0.0", port=3000, debug=True)
