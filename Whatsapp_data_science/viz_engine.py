import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class WhatsappAnaliziGrafiks:

    def grafik_aylik_dagilim(self, combined_month):
        df_melted = pd.melt(combined_month, id_vars="date", 
        var_name="kullanıcı", value_name="mesaj_sayısı")
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df_melted, x="date", y="mesaj_sayısı", hue="kullanıcı", s=100)
        plt.title("Aylık Mesaj Dağılımı", fontsize=14)
        plt.xlabel("Tarih"); plt.ylabel("Mesaj Sayısı")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def grafik_saatlik_dagilim(self, combined_hour):
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=combined_hour)
        plt.title("Saatlik Mesaj Dağılımı", fontsize=14)
        plt.xlabel("Saat"); plt.ylabel("Mesaj Sayısı")
        plt.xticks(range(0, 24))
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def grafik_dakika_dagilim(self, combined_minute):
        plt.figure(figsize=(12, 6))
        sns.barplot(data=combined_minute)
        plt.title("Dakika Bazlı Dağılım", fontsize=14)
        plt.xlabel("Dakika"); plt.ylabel("Mesaj Sayısı")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()
