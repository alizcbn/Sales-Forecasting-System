import pandas as pd
import matplotlib.pyplot as plt
import os

# Excel'den veri oku
df = pd.read_excel("satislar.xlsx")

# Tarih sütununu datetime yap
df["Tarih"] = pd.to_datetime(df["Tarih"])

# Ürün bazında günlük satış toplamı
pivot = df.pivot_table(index="Tarih", columns="Ürün Adı", values="Satış Adedi", aggfunc="sum")

# Toplam gelir hesapla
toplam_gelir = df["Gelir (₺)"].sum()
print(f"Toplam gelir: {toplam_gelir:.2f} ₺")

# En çok satan ürün
toplam_satis = df.groupby("Ürün Adı")["Satış Adedi"].sum()
en_cok_satan = toplam_satis.idxmax()
print(f"En çok satan ürün: {en_cok_satan}")

# Günlük satış grafiği
plt.figure(figsize=(10,6))
pivot.plot(marker='o')
plt.title("Günlük Satış Adedi (Ürün Bazında)")
plt.ylabel("Satış Adedi")
plt.xlabel("Tarih")
plt.grid(True)
plt.legend(title="Ürün")
plt.tight_layout()
plt.show()

# Basit Tahmin: 7 günlük hareketli ortalama ile gelecek 7 günü tahmin et
tahmin_gun_sayisi = 7
tahminler = {}

for urun in pivot.columns:
    son_7_gun_ortalama = pivot[urun].tail(7).mean()
    tahminler[urun] = [son_7_gun_ortalama] * tahmin_gun_sayisi

tahmin_tarihleri = pd.date_range(start=pivot.index[-1] + pd.Timedelta(days=1), periods=tahmin_gun_sayisi)
tahmin_df = pd.DataFrame(tahminler, index=tahmin_tarihleri)

print("\n7 Günlük Satış Tahmini (adet):")
print(tahmin_df)

# Tahmin grafiği (son 30 gün + tahmin)
plt.figure(figsize=(10,6))
for urun in pivot.columns:
    plt.plot(pivot.index, pivot[urun], marker='o', label=f"{urun} - Geçmiş")
    plt.plot(tahmin_df.index, tahmin_df[urun], marker='x', linestyle='--', label=f"{urun} - Tahmin")

plt.title("Satış Adedi: Geçmiş ve Tahmin")
plt.ylabel("Satış Adedi")
plt.xlabel("Tarih")
plt.legend()
plt.grid(True)
plt.tight_layout()

# docs klasörü yoksa oluştur
if not os.path.exists("docs"):
    os.makedirs("docs")

plt.savefig("docs/satis-grafik.png")
plt.show()
