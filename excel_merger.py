import pandas as pd

class ExcelMerger:
    def __init__(self, main_file):
        # Ana Excel dosyasını yükle
        self.main_df = pd.read_excel(main_file)
        self.main_columns = set(self.main_df.columns)

    def merge(self, additional_file):
        # Ek veriyi yükle
        additional_df = pd.read_excel(additional_file)

        # Ortak sütunları al ve olmayan sütunları göz ardı et
        common_columns = list(self.main_columns.intersection(set(additional_df.columns)))

        # Ortak sütunlardan yeni verileri ekle
        new_data = additional_df[common_columns]

        # Yeni verileri ana veriye ekle
        self.main_df = pd.concat([self.main_df, new_data], ignore_index=True)

    def save(self, output_file):
        # Güncellenmiş DataFrame'i kaydet
        self.main_df.to_excel(output_file, index=False)

# Sınıfı kullanmak için örnek:
if __name__ == "__main__":
    main_file = "main_data.xlsx"
    additional_file = "additional_data.xlsx"
    output_file = "updated_main_data.xlsx"

    merger = ExcelMerger(main_file)
    merger.merge(additional_file)
    merger.save(output_file)
