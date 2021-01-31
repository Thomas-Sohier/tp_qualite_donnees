#
# Import
#

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from tkinter import *
from functools import partial
import statistics 

#
# Class
#
class SnaptoCursor(object):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.ly = ax.axvline(color='k', alpha=0.2)
        self.marker, = ax.plot([0],[0], marker="o", color="crimson", zorder=3) 
        self.x = x
        self.y = y
        self.txt = ax.text(0.7, 0.9, '')

    def mouse_move(self, event):
        if not event.inaxes: return
        x, y = event.xdata, event.ydata
        indx = np.searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        self.ly.set_xdata(x)
        self.marker.set_data([x],[y])
        text = '%1.2f°C (jour %1d)' % (y, x)
        avg = getAverageXDays(self,event.xdata,event.ydata,30)
        self.txt.set_text(text + ' \n'+'%1.2f°C (moyenne 30d)' % (avg))
        self.txt.set_position((x,y))
        self.txt.set_position((x,y))
        self.ax.figure.canvas.draw_idle()
#
# Fontions
#
flatten = lambda t: [item for sublist in t for item in sublist]

def getAverageXDays(self,x,y,nbJours):
  temperature_day=[]

  for j in range(0,nbJours):
    indx = np.searchsorted(self.x, [x])[0]
    y = self.y[indx - j]
    temperature_day.append(y)

  return np.average(temperature_day) 


def setValeursMois():
  values_by_month=[]
  for column in range(3, 15):
    month_temperature=[]
    for row in range(3, 34):
      temperature_value = values.iloc[row, column]
      if(not np.isnan(temperature_value)):
        month_temperature.append(temperature_value)
    values_by_month.append(month_temperature)
  return values_by_month

def setValeursMoisErreur(df_erreur):
  values_by_month_error = []
  for column in range(3, 15):
    month_temperature=[]
    for row in range(3, 34):
        temperature_value = df_erreur.iloc[row, column]
        if(type(temperature_value) is str):
            temperature_value = np.average([getValeurApres(df_erreur, row, column), getValeurAvant(df_erreur, row, column)])
        if(not np.isnan((temperature_value))):
            month_temperature.append(temperature_value)

    values_by_month_error.append(month_temperature)
  return values_by_month_error

def getValeursMoisErreurCorrection(year):
  values_by_month_ok = []
  for indexMonth,month in enumerate(year,start=0):
    for indexDay,day in enumerate(month,start=0):
      if(indexMonth==0 and indexDay==0):
        if(abs(day - month[indexDay+1]) > 12):
          year[indexMonth][indexDay]=month[indexDay+1]
      elif(indexMonth==11 and indexDay==len(month)-1):
        if(abs(day - month[indexDay-1]) > 12):
          year[indexMonth][indexDay]=month[indexDay-1]
      elif(indexDay==0):
        if(abs(day - month[indexDay+1]) > 12 and abs(day - year[indexMonth-1][len(year[indexMonth-1])-1]) > 12):
          year[indexMonth][indexDay]=np.average( [ month[indexDay+1],year[indexMonth-1][len(year[indexMonth-1])-1]])
      elif(indexDay==len(month)-1):
        if(abs(day - month[indexDay-1]) > 12 and abs(day - year[indexMonth+1][len(year[indexMonth+1])-1]) > 12):
          year[indexMonth][indexDay]=np.average([month[indexDay-1],year[indexMonth+1][len(year[indexMonth+1])-1]])
      else:
        if(abs(day - month[indexDay-1]) > 12 and abs(day - month[indexDay+1]) > 12):
          year[indexMonth][indexDay]=np.average([month[indexDay-1],month[indexDay+1]])
  values_by_month_ok=year.copy()
  return values_by_month_ok

def getValeurApres(df, rowIndex, columnIndex):
    nextValue = df.iloc[(rowIndex + 1), columnIndex]
    if np.isnan(nextValue):
        return getNextCorrectValue(df, rowIndex+2, columnIndex)
    else:
        return nextValue
def getValeurAvant(df, rowIndex, columnIndex):
    nextValue = df.iloc[(rowIndex-1), columnIndex]
    if np.isnan(nextValue):
        return getNextCorrectValue(df, rowIndex-2, columnIndex)
    else:
        return nextValue

def getMoy(dataset):
  average=[]
  for m in dataset:
    average.append(np.average(m))
  return average

def getEcartType(dataset):
  ecart_type=[]
  for m in dataset:
    ecart_type.append(np.std(m))
  return ecart_type

def getMinParMois(dataset):
  min_per_month=[]
  for m in dataset:
    min_per_month.append(min(m))
  return min_per_month

def getMinAnnee(dataset):
  min_year= min(getMinParMois(dataset))
  return min_year

def getMaxParMois(dataset):
  max_per_month=[]
  for m in dataset:
    max_per_month.append(max(m))
  return max_per_month

def getMaxAnnee(dataset):
  max_year= max(getMaxParMois(dataset))
  return max_year

def getCourbe(mois,libelle):
  plot = plt.figure(libelle)
  plt.plot(mois)
  plt.title(libelle)
  plt.ylabel("Temperature")
  plt.xlabel("Jour") 
  plt.show()

def getCourbeAnnee():
  t = np.arange(0, 365, 1)
  s = np.sin(2 * 2 * np.pi * t)
  df_temp = pd.DataFrame(columns = ['Température'])
  for column in df:
      for value in df[column]:
          df_temp = df_temp.append({'Température':value},ignore_index=True)
  df_temp.dropna()
  fig, ax = plt.subplots()
  ax.plot(t, flatten(values_by_month),)
  ax.set(title='Année')
  snap_cursor = SnaptoCursor(ax, t, flatten(values_by_month))
  fig.canvas.mpl_connect('motion_notify_event', snap_cursor.mouse_move)
  plt.show()

def affichageMois(canvas,fenetre,dataset,yPos):
  mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
  moyenne=getMoy(dataset)
  minMois=getMinParMois(dataset)
  maxMois=getMaxParMois(dataset)
  ecartType=getEcartType(dataset)
  canvas.create_text(150,220+yPos,fill="black",font="Times 15 bold",text="Valeurs mensuelles")
  for m in range(0,12):
    canvas.create_text(150+(m*130),240+yPos,fill="black",font="Times 15 bold",text=mois[m])
    canvas.create_text(150+(m*130),270+yPos,fill="black",font="Times 13",text="Moyenne : "+str("{:.2f}".format(moyenne[m])))
    canvas.create_text(150+(m*130),290+yPos,fill="black",font="Times 13",text="Min : "+str("{:.2f}".format(minMois[m])))
    canvas.create_text(150+(m*130),310+yPos,fill="black",font="Times 13",text="Max : "+str("{:.2f}".format(maxMois[m])))
    canvas.create_text(150+(m*130),330+yPos,fill="black",font="Times 13",text="Ecart-type : "+str("{:.2f}".format(ecartType[m])))
    b = Button(fenetre, text="Graphique", width=10, command=partial(getCourbe,dataset[m],mois[m]),background="white",foreground="black",activebackground="grey",activeforeground="black")
    b.place(x=100+(m*130), y=350+yPos, anchor="nw", width=100, height=30)

def affichageValeursAnnées(canvas,fenetre,dataset,yPos):
  canvas.create_text(900,90+yPos,fill="black",font="Times 15 bold",text="Valeurs annuels")
  canvas.create_text(900,120+yPos,fill="black",font="Times 13",text="Min : "+str("{:.2f}".format(getMinAnnee(dataset))))
  canvas.create_text(900,140+yPos,fill="black",font="Times 13",text="Max : "+str("{:.2f}".format(getMaxAnnee(dataset))))
  b = Button(fenetre, text="Graphique année", width=10, command=getCourbeAnnee,background="white",foreground="black",activebackground="grey",activeforeground="black")
  b.place(x=850, y=160+yPos, anchor="nw", width=100, height=30)

def affichageFenetre():
  fenetre = Tk()
  fenetre.title("Qualité des données")
  fenetre.geometry('1800x800')
  canvas=Canvas(fenetre,bg='#FFFFFF',width=800,height=800,scrollregion=(0,0,1500,1500))
  canvas.create_text(900,20,fill="black",font="Times 20 bold",text="Trouver la capitale")
  canvas.create_text(900,60,fill="black",font="Times 20 bold",text="Données propres")
  # Tableau propre

  affichageValeursAnnées(canvas,fenetre,values_by_month,0)
  affichageMois(canvas,fenetre,values_by_month,0)

  # Tableau erreurs
  canvas.create_text(900,450,fill="black",font="Times 20 bold",text="Données erreurs")
  affichageValeursAnnées(canvas,fenetre,values_correction,400)
  affichageMois(canvas,fenetre,values_correction,400)

  canvas.pack(side=LEFT,expand=True,fill=BOTH)
  fenetre.mainloop()

#
# Partie 1 SI
#
df = pd.read_excel(r'data/Climat.xlsx', skiprows = 2,  nrows= 32, usecols = 'C:O')
values = pd.read_excel('data/Climat.xlsx', sheet_name=0)
df = df.drop(df.index[0])
df.drop(df.columns[0], axis=1, inplace=True)
df
values_by_month=setValeursMois()

#
# Partie 2 SI-ERROR
#
error = pd.read_excel('data/Climat.xlsx', sheet_name=1)
values_correction = getValeursMoisErreurCorrection(setValeursMoisErreur(error))
#print(values_correction)


affichageFenetre()
