import pandas as pd
import re
import sys
from collections import Counter
import hakaretler
import sevgi_sozcukleri
import stop_words
import warnings
import viz_engine
warnings.filterwarnings("ignore", category=UserWarning)


class WhatsappAnalizi:
    def __init__(self, txt_file):
        sys.stdout.reconfigure(encoding="utf-8")
        # Display ayarları
        pd.set_option("display.max.columns", None)
        pd.set_option("display.max.rows", None)
        pd.set_option("display.max_colwidth", None)
        pd.set_option("display.width", 5000)
        pd.set_option("display.expand_frame_repr", False)

        self.txt_file = txt_file
        with open(self.txt_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        self.pattern1 = re.compile(r"(\d{1,2}\.\d{1,2}\.\d{4}) (\d{1,2}:\d{2}) - ([^:]+): (.+)")
        self.pattern2 = re.compile(r"\[(\d{1,2}\.\d{1,2}\.\d{4}) (\d{2}:\d{2}:\d{2})\] (.*?): (.+)")

        self.data = []
        for line in lines:
            match = self.pattern1.match(line) or self.pattern2.match(line)
            if match:
                date, time, sender, message = match.groups()
                self.data.append({
                    "date": date,
                    "time": time,
                    "sender": sender,
                    "message": message
                })
        self.df = pd.DataFrame(self.data)

    def df_by_choice(self,choice=("user","dev")):
        names = []
        with open(f"{self.txt_file}","r",encoding="utf-8") as file:
            this_file = file.readlines()

        for i in this_file:
            match = self.pattern1.match(i) or self.pattern2.match(i)
            if match:
                _, _, sender, _ = match.groups()
                names.append(sender)

        df_list = []
        name_list = []

        for name in set(names):
            print(name)
            df_list.append(self.User1(f"{name}",choice))
            name_list.append(name)

        if choice == "user":
            self.axis = 0
        if choice == "dev":
            self.axis = 1

        new_df = pd.DataFrame()

        if choice == "user":
            new_df = pd.concat(df_list,axis=0)
            end_df = new_df.T
            end_df.columns = name_list
            return end_df

        new_df = pd.DataFrame()

        if choice == "dev":
            all_dates = pd.date_range(start="2023-10-01", end="2025-04-01", freq="MS")
            combined_month = pd.DataFrame({"date": all_dates})

            all_hours = [f"{h:02d}:00" for h in range(24)]
            combined_hour = pd.DataFrame({"date": all_hours})

            all_minutes = [f"{m:02d}" for m in range(60)]
            combined_minute = pd.DataFrame({"date": all_minutes})

            for i in range(len(df_list)):
                month_df = df_list[i][0].copy()
                hour_df = df_list[i][1].copy()
                minute_df = df_list[i][2].copy()

                user_name = df_list[i][0].columns[1]  # ay df'inde kullanıcı adı sütunu

                month_df["date"] = pd.to_datetime(month_df["date"], format="%m.%Y")
                hour_df = hour_df.rename(columns={"count": user_name})
                minute_df = minute_df.rename(columns={"count": user_name})

                combined_month = pd.merge(combined_month, month_df, on="date", how="left")
                combined_hour = pd.merge(combined_hour, hour_df, on="date", how="left")
                combined_minute = pd.merge(combined_minute, minute_df, on="date", how="left")


            combined_month["date"] = combined_month["date"].dt.strftime("%Y-%m-%d")
            combined_month = combined_month.fillna(0)
            combined_hour = combined_hour.fillna(0)
            combined_minute = combined_minute.fillna(0)

            print("\n== Aylık Dağılım ==")
        
            return {
                "month": combined_month,
                "hour": combined_hour,
                "minute": combined_minute
            }


    def User1(self, user: str,type="user"):
        #type user, dev
        user_df = self.df[self.df["sender"] == user].reset_index(drop=True)

        total_message = self.total_message(user_df)

        # Zaman analizleri
        chat_by_month = self.chat_parser_by_time(user_df["date"], "month")
        self.fav_time_month = Counter(chat_by_month).most_common()

        chat_by_hour = self.chat_parser_by_time(user_df["time"], "hour")
        self.fav_time_hour = Counter(chat_by_hour).most_common() 

        chat_by_minute = self.chat_parser_by_time(user_df["time"], "minute")
        self.fav_time_minute = Counter(chat_by_minute).most_common()

        # En çok kelime
        top_words = self.chat_analiz("search_word_all", df=user_df)
        fav_word, fav_word_count = top_words[0] if top_words else (None, 0)

        # Küfür ve sevgi
        fav_offensive_word = self.chat_analiz("search_word_list", hakaretler.kelimeler, user_df).iloc[0] if not self.chat_analiz("search_word_list", hakaretler.kelimeler, user_df).empty else None
        fav_lovely_word = self.chat_analiz("search_word_list", sevgi_sozcukleri.kelimeler, user_df).iloc[0] if not self.chat_analiz("search_word_list", sevgi_sozcukleri.kelimeler, user_df).empty else None


        if type == "user":
            return pd.DataFrame([{
                "fav_word": (fav_word,fav_word_count),
                "fav_offensive_word": (fav_offensive_word["kelime"],fav_offensive_word["frekans"]),
                "fav_lovely_word": (fav_lovely_word["kelime"],fav_lovely_word["frekans"]),
                "by_month": (self.fav_time_month[0][0],self.fav_time_month[0][1]) if self.fav_time_month else (None,None),
                "by_hour": (self.fav_time_hour[0][0],self.fav_time_hour[0][1]) if self.fav_time_hour else (None,None),
                "by_minute": (self.fav_time_minute[0][0],self.fav_time_minute[0][1]) if self.fav_time_minute else (None,None),
                "total_message": total_message
            }])
        if type == "dev":
            return [
                pd.DataFrame(self.fav_time_month,columns=(["date",f"{user_df["sender"][0]}"])),
                pd.DataFrame(self.fav_time_hour,columns=(["date","count"])),
                pd.DataFrame(self.fav_time_minute,columns=(["date","count"]))
            ]

    def total_message(self, df):
        text = " ".join(df["message"].dropna().str.lower())
        cleaned = self.clean_message(text)
        words = [w for w in cleaned.split() if w not in stop_words.liste]
        return len(words)

    def chat_analiz(self, method, analiz_list=None, df=None):
        if not isinstance(df, pd.DataFrame):
            df = self.df

        def search_word_list(analiz_list, df):
            kelime_kumesi = [w.lower() for w in analiz_list]
            target_words = []

            def check_message(msg):
                words = self.clean_message(msg).split()
                for word in words:
                    if word in kelime_kumesi:
                        target_words.append(word)
                return bool(set(words) & set(kelime_kumesi))

            df["analiz"] = df["message"].apply(check_message)
            word_counts = Counter(target_words).most_common()
            return pd.DataFrame(word_counts, columns=["kelime", "frekans"])

        def search_word_all(df):
            text = " ".join(df["message"].dropna().str.lower())
            cleaned = self.clean_message(text)
            words = [w for w in cleaned.split() if w not in stop_words.liste]
            return Counter(words).most_common(3)

        if method == "search_word_list":
            return search_word_list(analiz_list, df)
        elif method == "search_word_all":
            return search_word_all(df)
        else:
            raise ValueError("Geçersiz method!")

    def chat_parser_by_time(self, series, olcek):
        formats = {
            "month": "%m.%Y",
            "hour": "%H:00",
            "minute": "%M"
        }

        if olcek not in formats:
            print("Geçersiz ölçek.")
            return []

        try:
            parsed = pd.to_datetime(series, errors='coerce', dayfirst=True)
            return parsed.dt.strftime(formats[olcek]).dropna().tolist()
        except Exception as e:
            print("Hata:", e)
            return []

    def clean_message(self, msg):
        msg = msg.lower()
        msg = re.sub(r"http\S+|www\S+", "", msg)   # link sil
        msg = re.sub(r"[^\w\s]", "", msg)          # noktalama sil
        msg = re.sub(r"\d+", "", msg)              # sayı sil
        return msg.strip()
    
# === Ana çalıştırma alanı ===
your_chat = "chat.txt"
if __name__ == "__main__":
    obj = WhatsappAnalizi(your_chat)
    ret = obj.df_by_choice("dev") 
    gobj = viz_engine.WhatsappAnaliziGrafiks()
    gobj.grafik_aylik_dagilim(ret["month"])