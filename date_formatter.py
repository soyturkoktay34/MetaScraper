from datetime import datetime

class DateFormatter:
    def __init__(self):
        # Türkçe ve İngilizce ay isimlerini numaralara çeviren sözlükler
        self.month_number = {
            "Ocak": "01", "January": "01",
            "Şubat": "02", "February": "02",
            "Mart": "03", "March": "03",
            "Nisan": "04", "April": "04",
            "Mayıs": "05", "May": "05",
            "Haziran": "06", "June": "06",
            "Temmuz": "07", "July": "07",
            "Ağustos": "08", "August": "08",
            "Eylül": "09", "September": "09",
            "Ekim": "10", "October": "10",
            "Kasım": "11", "November": "11",
            "Aralık": "12", "December": "12"
        }

        # Türkçe gün isimlerinin İngilizce karşılıkları
        self.day_translation = {
            "Pazartesi": "Monday", "Salı": "Tuesday", "Çarşamba": "Wednesday",
            "Perşembe": "Thursday", "Cuma": "Friday",
            "Cumartesi": "Saturday", "Pazar": "Sunday"
        }

        # Desteklenen tarih formatları
        self.possible_formats = [
            "%d %m %Y %A, %H:%M",  # 26 Nisan 2024 Cuma, 05:36
            "%Y-%m-%dT%H:%M:%S.%fZ",  # 2024-04-13T13:59:56.000Z
            "%d %m %H:%M %Y",  # 02 Mayıs 14:28 2024
            "%Y-%m-%dT%H:%M:%S.%f",  # 2024-05-01T20:37:29.000Z
            "%d.%m.%Y %H:%M",  # 26.10.2005 05:30
            "%d %m %Y %H:%M:%S",  # 16 April 2024 12:10:46
            "%d %m %Y %A, %H:%M"  # 22 Nisan 2024 Pazartesi, 12:55
        ]

    def format_date(self, date_string):
        # Türkçe ay isimlerini numaralarına çevir
        for month, num in self.month_number.items():
            date_string = date_string.replace(month, num)
        # Türkçe gün isimlerini İngilizce karşılıklarıyla değiştir
        for tr_day, en_day in self.day_translation.items():
            date_string = date_string.replace(tr_day, en_day)

        # Varsayılan format hatası
        formatted_date = "no date text"

        # Farklı formatları deneyerek doğru tarihi yakalamaya çalış
        for fmt in self.possible_formats:
            try:
                parsed_date = datetime.strptime(date_string, fmt)
                formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                break
            except ValueError:
                continue

        return formatted_date
    def format_eksi(self, date_string):
        # "~" işaretine göre tarihleri ayır ve ilk tarihi al
        if '~' in date_string:
            date_string = date_string.split('~')[0].strip()

        return self.format_date(date_string)
