import pandas as pd
import re
from transformers import pipeline

# 1. Load Model IndoBERT
print("Sedang memuat model IndoBERT... (Tunggu sebentar)")
nlp = pipeline("sentiment-analysis", model="indobenchmark/indobert-base-p2")

# 2. Fungsi Cleaning Teks
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower() # Case folding
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Hapus angka & simbol
    text = re.sub(r'\s+', ' ', text).strip() # Hapus spasi berlebih
    return text

# 3. Load Data
file_input = "Database_Gabungan_Lengkap.xlsx - Sheet1.csv"
df = pd.read_excel("Database_Gabungan_Lengkap.xlsx")

print("Sedang membersihkan data...")
df['Isi_Ulasan_Clean'] = df['Isi Ulasan'].apply(clean_text)

# 4. Proses Sentimen (Hanya untuk baris yang ada ulasannya)
def get_sentiment(text):
    if text == "":
        return "Netral"
    try:
        result = nlp(text[:512])[0] # Limit 512 karakter
        label = result['label']
        # Pemetaan label IndoBERT base p2
        if label == "LABEL_0": return "Negatif"
        if label == "LABEL_1": return "Netral"
        return "Positif"
    except:
        return "Netral"

print("Sedang menganalisis sentimen... (Proses ini memakan waktu)")
df['Sentimen'] = df['Isi_Ulasan_Clean'].apply(get_sentiment)

# 5. Simpan Hasil
df.to_excel("Hasil_Sentimen_Final.xlsx", index=False)
print("Selesai! File 'Hasil_Sentimen_Final.xlsx' telah dibuat.")