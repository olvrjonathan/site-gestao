import numpy as np
from numpy.lib.function_base import average
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from io import StringIO
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
import warnings
#warnings.simplefilter("ignore") # Oculta erros de threading irrelevantes para a função
#from django.db.models import Avg, Max, Min, Count, F, Q

def grafico(df):
    day = df.index.min()
    df.reset_index(inplace=True)
    x = df.index.values.reshape(-1, 1)
    y1 = df['price'].to_numpy().reshape(-1, 1)
    y2 = df['duration'].to_numpy().reshape(-1,1)
    reg = LinearRegression().fit(x, y1)
    x_ = np.array([x.min(), x.max()]).reshape(-1, 1)
    y_ = reg.predict(x_)

    fig = plt.figure()
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.plot(x_,y_)
    plt.xlabel(f'Dias a partir de {day}')
    plt.ylabel('Receita (azul) e minutos trabalhados (laranja)')
    plt.title('Tendência de receita ao longo do tempo')
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    imgdata.close()
    return data

def inicio(request):
    return render(request, 'trabalho/inicio.html')

def marcelo(request):
    df = pd.read_sql("""SELECT title, price, duration, date(date_time) AS date FROM
                (user_booking AS b INNER JOIN user_service AS s ON b.service_id = s.id)
                WHERE paid_out = 1;""", con=connection)
    plot = grafico(df[['price', 'duration', 'date']].groupby('date').agg(sum))
    return render(request, 'trabalho/marcelo.html', {'plot': plot})
