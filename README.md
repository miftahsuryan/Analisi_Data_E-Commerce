# Proyek Analisis Data E-Commerce ✨

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data penjualan e-commerce dari berbagai kategori produk dan lokasi pemesanan. Dengan menggunakan dataset publik, proyek ini memberikan wawasan mengenai penjualan berdasarkan kategori produk dan analisis pemesanan berdasarkan lokasi (kota dan negara bagian).

## Setup Environment - Visual Studio Code dengan Jupyter Notebook

### 1. Install Visual Studio Code (VS Code)
- Unduh dan install [Visual Studio Code](https://code.visualstudio.com/).
- Install ekstensi **Python** dan **Jupyter** di VS Code.

### 2. Install Python 3.12.0
- Download Python 3.12.0 di [python.org](https://www.python.org/downloads/release/python-3120/).
- Pastikan Python terinstal dengan menjalankan perintah:
```
python --version
```

### 3. Install Dependencies
- Install Jupyter dan pustaka lainnya menggunakan pip:
```
pip install jupyter
pip install -r requirements.txt
```

### 4. Pilih Python Interpreter
- Tekan **Ctrl+Shift+P** dan pilih **Python: Select Interpreter**. Pilih interpreter yang ada di virtual environment (`./venv/bin/python` atau `.\venv\Scripts\python.exe`).

### 5. Menjalankan Jupyter Notebook
- Buka file `.ipynb` di VS Code dan pilih kernel **Python** yang sesuai.
- Jalankan sel-sel di notebook untuk melakukan analisis dan visualisasi.

### 6. Menjalankan Aplikasi Streamlit
- Untuk menjalankan aplikasi Streamlit dari terminal Jupyter Notebook, gunakan perintah berikut:
```python
!streamlit run dashboard.py
```

### 7. Persyaratan
Proyek ini membutuhkan beberapa pustaka Python yang tercantum dalam requirements.txt, antara lain:
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Folium
- Streamlit

Untuk menginstal semua dependensi, jalankan:
```
pip install -r requirements.txt
```