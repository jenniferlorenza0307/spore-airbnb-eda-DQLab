# Singapore Airbnb Listings - Exploratory Data Analysis (EDA)
Portfolio Project Bootcamp Data Analyst with Python & SQL[^1]

Slides containing summary result of this EDA findings: `Summary of Findings.pdf`

Python code for Dash Plotly dashboard: `eda-airbnb-spore.py`

## Tentang Project
DQLab sebagai perusahaan data mendapatkan permintaan klien yang berasal dari Singapura. Calon owner (pemilik) property tersebut akan menyewakan properti di
marketplace Airbnb dan tentunya ingin mendapatkan keuntungan maksimal dari penyewaan properti. Sebelumnya telah diketahui bahwa tempat penyewaan yang tepat 
berpengaruh terhadap tingginya kegiatan penyewaan. Sebagai seorang data analyst DQLab yang ditugaskan mengolah data properti Airbnb Singapura, analisis seperti 
apa yang akan kamu berikan untuk membantu client agar client tersebut bisa mendapatkan keuntungan terbaik dari hasil kegiatan penyewaan yang akan dilakukan?
Dalam final project kali ini akan dilakukan analisis terhadap data penginapan airbnb di Singapore. Terdapat 3 jenis data (tersedia dalam excel dan csv) yang 
diberikan kepada peserta. Data yang diberikan mencangkup data detail per listings, data historis penyewaan per listings, dan mapping neighbourhood_group untuk 
setiap neighborhood. Diberikan juga kamus data untuk setiap dataset yang diberikan. Dalam kamus tersebut, setiap field diberi deskripsi singkat mengenai arti 
dari field tersebut. 

## Dataset Glosarium

- Data 1: DQLab Airbnb Listing Dataset

  Data pertama berisi mengenai daftar listing Airbnb di Singapore. File name: `DQLab_listings(22Sep2022).csv`

  | No | Field Name       | Description                                                              |
  |----|------------------|--------------------------------------------------------------------------|
  | 1  | id               | Listing's unique Airbnb id                                               |
  | 2  | name             | Listing's name/display in Airbnb web                                     |
  | 3  | host_id          | Listing host's unique ID                                                 |
  | 4  | host_name        | Listing host's name                                                      |
  | 5  | neighbourhood    | Listing's neighbourhood name                                             |
  | 6  | latitude         | Listing's earth latitude location                                        |
  | 7  | longitude        | Listing's earth longitude location                                       |
  | 8  | room_type        | Listing's room type                                                      |
  | 9  | price            | Listing's price                                                          |
  | 10 | minimum_nights   | Indicator of minimum stay length                                         |
  | 11 | availability_365 | Indicator of the total number of days the listing is available in a year |
  
- Data 2: Listings Reviews History

  Data kedua berisi mengenai data historis order/rent per listing di Singapore dari 1 Januari 2018 sampai dengan 22 September 2022. 
  File name:	 `DQLab_reviews(22Sep2022).csv`
  
  | No | Field Name       | Description                                                              |
  |----|------------------|--------------------------------------------------------------------------|
  | 1  | listing_id       | Listing's unique Airbnb id                                               |
  | 2  | date             | Date when specific listing was rented                                    |

- Data 3: Neighborhood Mapping 

  Data ketiga berisi mengenai mapping region Singapore berdasarkan neghhbourhoodnya. File name: `DQLab_nieghbourhood(22Sep2022).csv`
  
  | No | Field Name       | Description                                                              |
  |----|------------------|--------------------------------------------------------------------------|
  | 1  | neighbourhood_group       | Singapore region (North/East/South/West/North-East)                     |
  | 2  | neighbourhood             | Singapore neighborhoods name                                    |


[^1]: Credits for all dataset, guidelines, and data glosarium belongs to [dqlab.id](https://dqlab.id/)
