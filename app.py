from flask import Flask, request, send_file, render_template
import os
import pandas as pd
from pdf_to_excel import generate_excel
from excel_to_ics import (
    generate_ics,
)  # Assuming your modified script logic is in `generate_ics` function

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if not file.filename.endswith(".pdf"):
        return "Invalid file format. Please upload an .pdf file.", 400

    # Save the uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Process the file
    try:
        output_excel = os.path.join(OUTPUT_FOLDER, "calendar.xlsx")
        output_file = os.path.join(OUTPUT_FOLDER, "calendar.ics")
        generate_excel(filepath, output_excel)
        generate_ics(
            output_excel, output_file
        )  # Use your script's function to create the .ics file
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

    # Send the output file to the user
    return send_file(output_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
