import pandas as pd


data = [{
        "username": "",
        "password": "",
        "email": "",
        "full_name": ""
        }]

datafram = pd.DataFrame(data)

datafram.loc[0, "username"] = 11

datafram.to_excel("test.xlsx")


print(datafram)
