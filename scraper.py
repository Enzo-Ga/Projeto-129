from bs4 import BeautifulSoup
import requests
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

def scrape():
    response = requests.get(START_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    bright_star_table = soup.find("table", class_="wikitable")

    table_body = bright_star_table.find("tbody")

    table_rows = table_body.find_all("tr")

    scraped_data = []

    for row in table_rows[1:]:  # Pular a linha de cabeçalho
        table_cols = row.find_all("td")
        temp_list = []

        for col_data in table_cols:
            data = col_data.get_text().strip()
            temp_list.append(data)

        scraped_data.append(temp_list)

    return scraped_data


scraped_data = scrape()

stars_data = []

for data_row in scraped_data:
    Star_names = data_row[1]
    Distance = data_row[3]
    Mass = data_row[5]
    Radius = data_row[6]
    Lum = data_row[7]

    required_data = [Star_names, Distance, Mass, Radius, Lum]
    stars_data.append(required_data)

headers = ["Star_names", "Distance", "Mass", "Radius", "Luminosity"]

star_df_1 = pd.DataFrame(stars_data, columns=headers)

star_df_1.to_csv("scraped_data.csv", index=True, index_label="id")

data_list = []


SECOND_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"  


def new_scrape():
    response = requests.get(SECOND_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    take_tables = soup.find_all("table", class_="wikitable")
    data_list = []  # Criando uma lista vazia para armazenar os dados
    
    for table in take_tables:
        rows = table.find_all("tr")
        
        for row in rows[1:]:  # Pular a primeira linha (cabeçalho)
            cols = row.find_all("td")
            
            if len(cols) >= 4:
                star_name = cols[0].get_text().strip()
                radius = cols[1].get_text().strip()
                mass = cols[2].get_text().strip()
                distance = cols[3].get_text().strip()
                
                data_list.append([star_name, radius, mass, distance])

    # Criando um DataFrame usando a biblioteca pandas
    headers = ["Star_names", "Distance", "Mass", "Radius"]
    df = pd.DataFrame(data_list, columns=headers)

    # Criando um arquivo CSV a partir do DataFrame
    csv_filename = "brown_dwarfs_data.csv"
    df.to_csv(csv_filename, index=False)

    print("DataFrame:")
    print(df.head())
    print(f"\nCSV file '{csv_filename}' created successfully.")

# Chame a função para executar a extração e criação do DataFrame e arquivo CSV
new_scrape()


df_1 = pd.read_csv("brown_dwarfs_data.csv")
df_1.dropna(inplace=True)
df_1["Mass"] = df_1["Mass"].astype(float)
df_1["Radius"] = df_1["Radius"].astype(float)
df_1["Radius"] *= 0.102763
df_1["Mass"] *= 0.000954588
df_1.to_csv("cleaned_brown_dwarfs.csv", index=False)

df_2 = pd.read_csv("scraped_data.csv")
df_2 = pd.read_csv("cleaned_brown_dwarfs.csv")
merge_df = pd.merge(df_1, df_2, on="Star_names")
merge_df.to_csv("merge_data", index=False)
