from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

app = Flask(__name__)

# Membaca data dari file Excel
file_path = 'br.xls'  # Sesuaikan dengan path file Anda
data = pd.read_excel(file_path)

# Fitur dan target
features = ['sqft', 'Bedrooms', 'Baths', 'Age', 'Occupancy', 'Pool', 'Style', 'Fireplace', 'Waterfront', 'DOM']
target = 'price'

X = data[features]
y = data[target]

# Membuat dan melatih model
model = DecisionTreeRegressor(random_state=42)
model.fit(X, y)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    content = request.form
    try:
        # Mengonversi nilai input menjadi tipe data numerik
        sqft = float(content['sqft'])
        bedrooms = float(content['bedrooms'])
        baths = float(content['baths'])
        age = float(content['age'])
        occupancy = float(content['occupancy']) 
        pool = float(content['pool'])  
        style = float(content['style'])  
        fireplace = float(content['fireplace'])  

        # Memastikan nilai waterfront tidak kosong sebelum konversi
        waterfront = content.get('waterfront')
        if waterfront and waterfront.strip():  # Memeriksa jika nilai tidak kosong atau hanya whitespace
            waterfront = float(waterfront)
        else:
            # Memberikan nilai default jika waterfront tidak valid
            waterfront = 0.0  # Atau berikan nilai default lainnya yang sesuai dengan konteks aplikasi

        dom = float(content['dom'])  

        # Membuat prediksi dengan nilai numerik yang telah dikonversi
        prediction = model.predict([[sqft, bedrooms, baths, age, occupancy, pool, style, fireplace, waterfront, dom]])

        # Mengembalikan hasil prediksi ke halaman web
        return render_template('index.html', prediction=prediction[0])

    except (KeyError, ValueError) as e:
        return "Kunci yang diperlukan tidak ditemukan atau terjadi kesalahan dalam data yang dikirimkan.", 400





if __name__ == '__main__':
    app.run(debug=True)
