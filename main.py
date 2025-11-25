from src import load_data, get_data_info


df = load_data("csv", "Data/Raw/BreadBasket_DMS.csv")

info = get_data_info(df)  
print(info) 