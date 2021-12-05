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

def graf(df):
    duration = df['duration'].values
    price = df['price'].values

    fig = plt.figure()
    plt.scatter(duration, price, color='purple')
    plt.title('Preço vs Durção')
    plt.xlabel('Duração')
    plt.ylabel('Preço')
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    imgdata.close()
    return data

def dominique(request):
    df = pd.read_sql("""SELECT title, price, duration, date(date_time) AS date FROM
                (user_booking AS b INNER JOIN user_service AS s ON b.service_id = s.id);""",
                con=connection)
    plot = graf(df)
    return render(request, 'trabalho/dominique.html', {'plot': plot})
















def graf7(df):
    duration = df['duration'].values
    price = df['price'].values

    fig = plt.figure()
    plt.scatter(duration, price, color='purple')
    plt.title('Preço vs Durção')
    plt.xlabel('Duração')
    plt.ylabel('Preço')
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    imgdata.close()
    return data

def iara(request):
    df = pd.read_sql("""SELECT title, price, duration, date(date_time) AS date FROM
                (user_booking AS b INNER JOIN user_service AS s ON b.service_id = s.id);""",
                con=connection)
    plot = graf7(df)
    return render(request, 'trabalho/iara.html', {'plot': plot})




















def graf2(dfy):
    dfy['n'] = 1
    dfy = dfy[["category", "n"]]
    dfy = dfy.groupby("category")
    dfy = dfy.sum()
    dfy.reset_index(inplace=True)
    dfy.rename(columns={"index":"category"}, inplace=True)

    fig = plt.figure()
    plt.pie(dfy['n'], labels=dfy['category'],
            autopct='%.2f', explode=(0, 0.3, 0, 0, 0 , 0, 0, 0, 0, 0))
    plt.axis('equal')
    plt.title('Categoria dos Serviços')
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    imgdata.close()
    return data

def juliana(request):
    dfy = pd.read_sql("""SELECT * FROM
                (user_service AS b INNER JOIN user_servicecategory AS s ON b.category_id = s.id);""",
                  con=connection)
    plot = graf2(dfy)
    return render(request, 'trabalho/juliana.html', {'plot': plot})


def graf3(df):
    df['n'] = 1
    df = df[["title", "n"]]
    df = df.groupby("title")
    df = df.sum()
    df.reset_index(inplace=True)
    df.rename(columns={"index":"title"}, inplace=True)
    df = df.sort_values(by='n', ascending=False)
    df = df.head(10)
    df = df.sort_values(by='n')

    fig = plt.figure()
    plt.barh(df['title'], df['n'],
                      color='darkorange', edgecolor='black', )
    plt.title('Serviços mais frequentes')
    plt.tight_layout()
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    imgdata.close()
    return data


def jonathan(request):
    df = pd.read_sql("""SELECT title, service_id FROM
                (user_booking AS b INNER JOIN user_service AS s ON b.service_id = s.id);""",
                  con=connection)

    plot = graf3(df)
    return render(request, 'trabalho/jonathan.html', {'plot': plot})
