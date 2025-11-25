from src import load_data, get_data_info ,auto_handle_missing


df = load_data("csv", "Data/Row/Sample - Superstore.csv")

info = get_data_info(df)  

cleaned_DF=auto_handle_missing(df)

info = get_data_info(df)  
print(info) 

