import pandas as pd
import json


test = """
[{
  "id": 1,
  "first_name": "Jeanette",
  "last_name": "Penddreth",
  "email": "jpenddreth0@census.gov",
  "gender": "Female",
  "ip_address": "26.58.193.2"
}, {
  "id": 2,
  "first_name": "Giavani",
  "last_name": "Frediani",
  "email": "gfrediani1@senate.gov",
  "gender": "Male",
  "ip_address": "229.179.4.212"
}, {
  "id": 3,
  "first_name": "Noell",
  "last_name": "Bea",
  "email": "nbea2@imageshack.us",
  "gender": "Female",
  "ip_address": "180.66.162.255"
}, {
  "id": 4,
  "first_name": "Willard",
  "last_name": "Valek",
  "email": "wvalek3@vk.com",
  "gender": "Male",
  "ip_address": "67.76.188.26"
}]
"""


def main(json_text, file_name=None):
    d = convert_json_to_dict(json_text)
    df = convert_dict_to_df(d)
    df_to_csv(df, file_name)


def convert_json_to_dict(j):
    return json.loads(j)


def convert_dict_to_df(d):
    return pd.DataFrame.from_dict(d)


def df_to_csv(df, filename=None):

    if filename:
        df.to_csv(filename)
    else:
        df.to_csv("default_csv_name.csv")


if __name__ == "__main__":
    main(test)

