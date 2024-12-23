from flask import Flask, render_template, request, send_from_directory, url_for, redirect
import os
from datetime import datetime
from percolation_logic import DisjointSet, generate_percolation_clusters, visualize_clusters, save_network_image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            n = int(request.form['grid_size'])
            p = float(request.form['probability'])
            if 1 <= n <= 500 and 0 <= p <= 1:
                return redirect(url_for('generate_visualization', grid_size=n, probability=p))
            else:
                return render_template('index.html', error="Invalid input parameters.")
        except ValueError:
            return render_template('index.html', error="Please enter valid numbers.")
    return render_template('index.html')

@app.route('/generate/<int:grid_size>/<float:probability>')
def generate_visualization(grid_size, probability):
    disjoint_set = generate_percolation_clusters(grid_size, grid_size, probability)
    image = visualize_clusters(grid_size, grid_size, disjoint_set)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"percolation_{grid_size}_{probability:.2f}_{timestamp}.png"
    image_path = save_network_image(image, filename)
    return render_template('visualization.html', image_name=filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)