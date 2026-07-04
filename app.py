print("Скрипт запущен!")
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import cv2
from datetime import datetime
from model_loader import ParkingDetector
from database import init_db, save_request, get_history
from report_generator import generate_pdf_report

app = Flask(__name__)
CORS(app)

init_db()
detector = ParkingDetector()

STATIC_DIR = 'static'
os.makedirs(STATIC_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    filename = file.filename
    image_bytes = file.read()

    result = detector.detect(image_bytes)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(STATIC_DIR, f'result_{timestamp}.jpg')
    cv2.imwrite(output_path, result['annotated_image'])

    save_request(
        filename=filename,
        vehicle_count=result['count'],
        vehicles_list=result['vehicles'],
        image_path=output_path
    )

    return jsonify({
        'count': result['count'],
        'vehicles': result['vehicles'],
        'image_url': f'/static/result_{timestamp}.jpg'
    })

@app.route('/history', methods=['GET'])
def history():
    rows = get_history()
    history_list = []
    for row in rows:
        history_list.append({
            'timestamp': row[0],
            'filename': row[1],
            'count': row[2],
            'vehicles': row[3],
            'image_url': f"/{row[4]}" if row[4] else None
        })
    return jsonify(history_list)

@app.route('/report', methods=['GET'])
def download_report():
    rows = get_history(limit=100)
    pdf_path = generate_pdf_report(rows)
    return send_file(pdf_path, as_attachment=True, download_name='parking_report.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000
    , debug=True)