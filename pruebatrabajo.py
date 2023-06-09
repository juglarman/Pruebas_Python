# -*- coding: utf-8 -*-
"""PruebaTrabajo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14m17FS473wJo8lrMaTe250adXZXJN-gu
"""

pip install autocorrect

import pandas as pd
import numpy as np
import difflib
import re
from autocorrect import Speller
spell = Speller(lang='es')

#Calling two datasets from 2015 to 2016
dfPrev1 = pd.read_excel( 'articles-391559_recurso (1).xlsx',  skiprows = 6 )
dfPrev2 = pd.read_excel( 'articles-391560_recurso (1).xlsx',  skiprows = 6 )

#Columns names verifications
dfPrev1Columns = dfPrev1.columns.tolist()
dfPrev2Columns = dfPrev2.columns.tolist()
print([x for x in dfPrev1Columns if x not in dfPrev2Columns])
print([x for x in dfPrev2Columns if x not in dfPrev1Columns])

#columns names renamed
dfPrev2.rename(columns = {'Género':'Sexo',
                          'Inscritos 2015':'Inscritos',
                          'Id_Sector':'ID Sector IES',
                          'Id_Caracter':'ID Caracter',
                          'Id_Nivel':'ID Nivel Académico',
                          'Id_Nivel_Formacion':'ID Nivel de Formación',
                          'Id_Metodologia':'ID Metodología',
                          'Id_Area':'ID Área',
                          'Id Género':'ID Sexo'
                          }, inplace = True)
dfPrev1.rename(columns = {'Inscritos 2016':'Inscritos'}, inplace = True)

#dataframes concated
frames = [dfPrev1, dfPrev2]
dfPrev = pd.concat(frames)

#Fixing columns names
dfPrev.rename(columns = {'Código de \nla Institución':'ID Institucion',
                          'Principal\n o\nSeccional':'Principal/Seccional',
                          'Código del \ndepartamento\n(IES)':'ID Departamento (IES)',
                          'Código del \nMunicipio\n(IES)':'ID Municipio',
                          'Municipio de\ndomicilio de la IES':'Municipio de Domicilio IES',
                          'Código \nSNIES del\nprograma':'ID Programa Academico',
                          'Código del \nDepartamento\n(Programa)':'ID Departamento Programa',
                          'Código del \nMunicipio\n(Programa)':'ID Municipio Programa',
                          'Departamento de \ndomicilio de la IES':"Departamento de Domicilio IES"
                          }, inplace = True)

df = dfPrev.copy()

#Remove na rows
df.dropna(axis = 0 ,inplace=True)

#Selecting numeric and string columns
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
numericColumns = df.select_dtypes(include=numerics).columns.tolist()
textColumns = [x for x in df.columns.tolist() if x not in numericColumns]

#Redefining not code or id columns
textColumns = [x for x in textColumns if ("ID" not in x) and ("Id" not in x)]
textColumns = [x for x in textColumns if "Código" not in x]

#Capitalize string columns
df[textColumns] = df[textColumns].astype(str).apply(lambda col: col.str.capitalize())

#Function for normalize
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

#normalizing string columns
for names in textColumns:
  df[names] = df[names].apply(lambda x: normalize(x))

#Erasing duplicates
df.drop_duplicates( subset=None , inplace=True )

#Function for eliminate non letters characteres, eliminate multiple spaces and correct orthography
def GrammarCorrection(x):
  return  re.sub(' +', ' ', spell( re.sub(r'[^\w\s]', '', x) ))

#function for look for similary words and unify for minimize redundancies
def Similary(table, column):
  cutLimit = 0.88
  elements = table[column].unique().tolist()
  partialList = elements.copy()
  #print(elements)
  finishing = True
  while(finishing):
    #print(partialList)
    elem = partialList[0]
    #print(elem)
    partialList = [ x for x in partialList if x != elem ]
    #print(partialList)
    if len(partialList) == 0:
      break
      finishing = False
    
    #print(partialList)
    if column == "Programa Académico":
      cutLimit = 0.88

    coinci = difflib.get_close_matches(elem,partialList,cutoff = cutLimit)
    if len(coinci) != 0:
      print( "Coincidencias de -", elem, ":", coinci )
      print("-----------------------------------------------")
    partialList = [ x for x in partialList if x not in coinci ]
    table.loc[table[column].isin(coinci), column] = elem
    #print( GrammarCorrection(elem))

dfp = df.copy()

#3 iterations for the function
for i in range(3):
  for colText in textColumns:
    print('##################COLUMNA#################',colText)
    Similary(dfp,colText)

print("De",len(df['Programa Académico'].unique().tolist())," programas académicos, se redujeron a ",len(dfp['Programa Académico'].unique().tolist()))

#Last corrections
dfp['Departamento de oferta del programa'].unique().tolist()
dfp.loc[dfp['Sexo']=="Hombre", 'Sexo'] = "Masculino"
dfp.loc[dfp['Sexo']=="Mujer", 'Sexo'] = "Femenino"
dfp.loc[dfp['Metodología']=="Distancia (tradicion", 'Metodología'] = "A distancia (tradicional)"
dfp.loc[dfp['Metodología']=='A distancia (tradicional)', 'Metodología'] = "Virtual"
dfp.loc[dfp['Metodología']=="A distancia (virtual)", 'Metodología'] = "Virtual"

dfp.to_excel('DatosTratadosEjercicio.xlsx')

dfp.to_csv('DatosTratadosEjercicio3.csv')