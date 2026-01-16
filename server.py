from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    return f"✅ File saved: {file.filename}", 200

@app.route("/list")
def list_photos():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

@app.route("/photos/<filename>")
def get_photo(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)