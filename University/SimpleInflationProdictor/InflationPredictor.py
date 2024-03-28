#Antoni Strasz
import requests
import datetime
import json
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt


gus_data_url = "https://api-dbw.stat.gov.pl/api/1.1.0/variable/variable-data-section?id-zmienna=305&id-przekroj=739&id-rok={year}&id-okres=247&ile-na-stronie=50&numer-strony=0&lang=pl/?format=json"

nbp_gold_data_url = "http://api.nbp.pl/api/cenyzlota/{start_date}/{end_date}/"


#Przyjmuje rok z którego ma wczytać dane
#Zwraca dict o numerach miesiąca jako kluczach i wartościach odpowiadających wskaźnikowi cen towarów i usług konsumpcyjnych na dany miesiąc
def get_gus_data(year: int):
    response = requests.get(gus_data_url.format(year = year))
    status_code = response.status_code
    response = response.json()
    if status_code != 200:
        raise Exception(response["error-reason"])
    data = {response["data"][i]["rownumber"]:response["data"][i]["wartosc"] for i in range(0,12)}
    return data


#Przyjmuje początkową i końcową datę z którego okresu wczytać dane
#Zwraca średnią cenę złota w tym okresie
def get_nbp_gold_mean(start_date: datetime.date, end_date: datetime.date):
    response = requests.get(nbp_gold_data_url.format(start_date = start_date, end_date=end_date))
    status_code = response.status_code
    if status_code != 200:
        raise Exception(response.text)
    response = json.loads(response.text)
    gold_sum = sum(float(i["cena"]) for i in response)
    return round(gold_sum/len(response), 2)

#Przyjmuje rok z którego ma wczytać dane
#Zwraca dict o numerach miesiąca jako kluczach i wartościach odpowiadających cenie złota w danym miesiącu
def get_nbp_gold_data(year: int):
    start_date = datetime.date(year, 1, 1)
    data = {}
    for i in range(1,13):
        end_date = start_date + relativedelta(months=1)
        #API zwraca wykiki włącznie z końcowym dziem, stąd odjęcie dnia
        gold_mean = get_nbp_gold_mean(start_date=start_date, end_date=end_date-relativedelta(days=1))
        start_date = end_date
        data[i] = gold_mean
    return data

#Przewidywania na podstawie podanej listy danych dla poprzednich lat
#Liczy średnią dla każdego miesiąca
def predict(yearly_data: list):
    data_entries_count = len(yearly_data)
    prediction = yearly_data[0]
    for yd in yearly_data[1:]:
        for key in yd.keys():
            prediction[key] += yd[key]
    for month in prediction:
        prediction[month] = round(prediction[month]/data_entries_count,2)
    return prediction



def draw_inflation_chart(axis,gus_data, nbp_gold_data, title, legend):
    xs = gus_data.keys()
    ys_gus = gus_data.values()
    ys_nbp = nbp_gold_data.values()
    axis.plot(xs, ys_gus, marker="x")
    axis.plot(xs, ys_nbp, marker="o")

    axis.set_title(title)
    axis.legend(legend)



#Rysuje wykres dla danych z podanego okresu lat i przewiduje wykres dla roku następnego
def Inflation_chart(start_year: int, end_year: int):
    collected_data = {"gus" :[], "nbp": []}
    obr, sb_plts = plt.subplots(end_year-start_year+2,1)
    plt.subplots_adjust(hspace=1)
    plt.xlim([1, 12])
    for i in range(start_year,end_year+1):
        gus_data = get_gus_data(i)
        nbp_gold_data = get_nbp_gold_data(i)
        collected_data["gus"].append(gus_data)
        collected_data["nbp"].append(nbp_gold_data)
        draw_inflation_chart(sb_plts[i-start_year],gus_data,nbp_gold_data,"Dane za rok: " + str(i),["Wskaźnik cen()", "Średnia cena złota(ZŁ)"])
    draw_inflation_chart(sb_plts[-1],predict(collected_data["gus"]),predict(collected_data["nbp"]),"Przewidywania rok: " + str(end_year+1),["Przewidywany wskaźnik cen", "Przewidywana średnia cena złota"])
    plt.show()

Inflation_chart(2018, 2021)

