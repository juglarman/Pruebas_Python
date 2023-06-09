# -*- coding: utf-8 -*-
"""GraficasPY.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UkOhqKPf_OQA72JRglp75l-EBbUBRbtZ
"""

import pandas as pd
import numpy as np
import plotly.express as px

pip install plotly==5.3.1

pip install kaleido

dfPrev = pd.read_excel( 'articles-391590_recurso.xlsx',  skiprows = 6 )

df = dfPrev.copy()

fig = px.bar(df, x="Total", y="Principal\n o\nSeccional", orientation='h')

fig.show()

fig = px.scatter(df, x="Servicios", y="Profesional",color="Sector IES")
fig.show()

df = dfPrev.copy()
fig = px.pie(df, values='Total', names='Caracter IES', title='Totales por Caracter IES')
fig.show()

fig = px.scatter(df, y="Departamento de \ndomicilio de la IES", x="Total", color="Sector IES", symbol="Sector IES")
fig.update_traces(marker_size=10)
fig.show()

fig.write_image("figure.png", engine="kaleido")