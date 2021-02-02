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

class SnapToCursorCompare(object):

  def __init__(self, ax, x, y, color, i, j):
    self.ax = ax
    self.ly = ax.axvline(color='k', alpha=0.2)  # the vert line
    self.marker, = ax.plot([0],[0], marker="o", color=color, zorder=3)
    self.color = color
    self.x = x
    self.y = y
    self.i = i
    self.j = j
    self.txt = ax.text(0.7, 0.9, '')

  def mouse_move(self, event):
      if not event.inaxes: return
      x, y = event.xdata, event.ydata
      indx = np.searchsorted(self.x, [x])[0]
      x = self.x[indx+1]
      y = self.y[indx]
      self.ly.set_xdata(x)
      self.marker.set_data([x],[y])
      self.txt.set_text('%1.2f°C (jour %1d)' % (y, x))
      self.txt.set_color(self.color)
      self.txt.set_position((0,self.j-(4*self.i)-8))
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
  data_base=[]
  for column in range(3, 15):
    month_temperature=[]
    for row in range(3, 34):
      temperature_value = values.iloc[row, column]
      if(not np.isnan(temperature_value)):
        month_temperature.append(temperature_value)
    data_base.append(month_temperature)
  return data_base

def setValeursMoisErreur(df_erreur):
  data_base_error = []
  for column in range(3, 15):
    month_temperature=[]
    for row in range(3, 34):
        temperature_value = df_erreur.iloc[row, column]
        if(type(temperature_value) is str):
            temperature_value = np.average([getValeurApres(df_erreur, row, column), getValeurAvant(df_erreur, row, column)])
        if(not np.isnan((temperature_value))):
            month_temperature.append(temperature_value)

    data_base_error.append(month_temperature)
  return data_base_error

def getValeursMoisErreurCorrection(year):
  data_base_ok = []
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
  data_base_ok=year.copy()
  return data_base_ok

def getValeursMoissavukoski(savukoski):
  data_base_savukoski=[]
  current_month=1
  month_temperature_savukoski=[]
  for row in range(1, 365):
    if(savukoski.iloc[row, 1] != current_month):
      current_month=current_month+1
      data_base_savukoski.append(month_temperature_savukoski.copy())
      month_temperature_savukoski=[]
    temperature_value_savukoski = savukoski.iloc[row, 5]
    month_temperature_savukoski.append(temperature_value_savukoski.copy())
  data_base_savukoski.append(month_temperature_savukoski.copy())
  return data_base_savukoski

def getValeursMoisHelsinki(dataset):
  data_base_dataset=[]
  for column in range(0, 12):
    month_temperature_dataset=[]
    for row in range(0, 31):
      temperature_value_dataset = (dataset.iloc[row, column] - 32) * 5/9
      if(not np.isnan(temperature_value_dataset)):
        month_temperature_dataset.append(temperature_value_dataset)
    data_base_dataset.append(month_temperature_dataset)
  return data_base_dataset

def getValeursMoisCsv(csv):
  data_base_csv=[]
  current_month=1
  month_temperature_csv=[]
  for index, row in csv.iterrows():
    if(row["Mois"] != current_month):
      current_month=current_month+1
      data_base_csv.append(month_temperature_csv.copy())
      month_temperature_csv=[]
    temperature_value_csv = (row["Temp"]- 32) * 5/9
    month_temperature_csv.append(temperature_value_csv)
  data_base_csv.append(month_temperature_csv.copy())
  return data_base_csv

def getValeurApres(value_error, rowIndex, columnIndex):
    nextValue = value_error.iloc[(rowIndex + 1), columnIndex]
    if np.isnan(nextValue):
        return getNextCorrectValue(value_error, rowIndex+2, columnIndex)
    else:
        return nextValue
def getValeurAvant(value_error, rowIndex, columnIndex):
    nextValue = value_error.iloc[(rowIndex-1), columnIndex]
    if np.isnan(nextValue):
        return getNextCorrectValue(value_error, rowIndex-2, columnIndex)
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

def getScore(dataset1, dataset2):
  moy_data1=getMoy(dataset1)
  moy_data2=getMoy(dataset2)
  et_data1=getEcartType(dataset1)
  et_data2=getEcartType(dataset2)
  score_mois=[]
  score_annee=0
  score_retour=[]
  for m in range(0,12):
    score=abs(moy_data1[m]-moy_data2[m])+abs(et_data1[m]-et_data2[m])
    score_annee=score_annee + score
    score_mois.append(score)
  score_retour.append(score_annee)
  score_retour.append(score_mois)
  return score_retour

def getCourbe(mois,libelle):
  plot = plt.figure(libelle)
  plt.plot(mois)
  plt.title(libelle)
  plt.ylabel("Temperature")
  plt.xlabel("Jour") 
  plt.show()

def getCourbeAnnee(dataset):
  lenD=0
  for d in dataset:
    lenD=lenD+len(d)
  t = np.arange(0, lenD, 1)
  df_temp = pd.DataFrame(columns = ['Température'])
  for column in dataset:
      for value in column:
          df_temp = df_temp.append({'Température':value},ignore_index=True)
  df_temp.dropna()
  fig, ax = plt.subplots()
  ax.plot(t, flatten(dataset),)
  ax.set(title='Année')
  snap_cursor = SnaptoCursor(ax, t, flatten(dataset))
  fig.canvas.mpl_connect('motion_notify_event', snap_cursor.mouse_move)
  fig.canvas.set_window_title("Année")
  plt.show()

def getAllCourbesAnnee():
  fig, ax = plt.subplots(figsize=(15,7))
  datas=[]
  datas.append(flatten(data_base))
  datas.append(flatten(data_helsinki))
  datas.append(flatten(data_savukoski))
  datas.append(flatten(data_oslo))
  nom_fichiers=["Propre","Helsinki","Savukoski","Oslo"]
  plt.subplots_adjust(bottom=0.2)
  
  plt.title("Comparatif année")
  plt.xlabel("Jours")
  plt.ylabel("Degré")
  
  min_temp = -20
  max_temp = 30

  plt.axis([1, 366, min_temp-10, max_temp+10])
  plt.grid(True)

  cursors = []
  for i, data in enumerate(datas):
      t = np.arange(0, 365, 1)
      plot = plt.plot(data, label=nom_fichiers[i])
      cursors.append(SnapToCursorCompare(ax, t, data, plot[0].get_color(), i, min_temp-10))
      plt.connect('motion_notify_event', cursors[i].mouse_move)

  plt.legend()
  plt.show()

def affichageMois(canvas,fenetre,dataset,yPos):
  mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
  moyenne=getMoy(dataset)
  minMois=getMinParMois(dataset)
  maxMois=getMaxParMois(dataset)
  ecartType=getEcartType(dataset)
  for m in range(0,12):
    canvas.create_text(280+(m*130),90+yPos,fill="black",font="Times 13 bold",text=mois[m])
    canvas.create_text(280+(m*130),110+yPos,fill="black",font="Times 11",text="Moyenne : "+str("{:.2f}".format(moyenne[m])))
    canvas.create_text(280+(m*130),125+yPos,fill="black",font="Times 11",text="Min : "+str("{:.2f}".format(minMois[m])))
    canvas.create_text(280+(m*130),140+yPos,fill="black",font="Times 11",text="Max : "+str("{:.2f}".format(maxMois[m])))
    canvas.create_text(280+(m*130),155+yPos,fill="black",font="Times 11",text="Ecart-type : "+str("{:.2f}".format(ecartType[m])))
    canvas.create_text(280+(m*130),170+yPos,fill="black",font="Times 11",text="Score : "+str("{:.2f}".format(getScore(data_base,dataset)[1][m])))
    b = Button(fenetre, text="Graphique", width=10, command=partial(getCourbe,dataset[m],mois[m]),background="white",foreground="black",activebackground="grey",activeforeground="black")
    b.place(x=230+(m*130), y=185+yPos, anchor="nw", width=100, height=30)

def affichageValeursAnnées(canvas,fenetre,dataset,yPos):
  canvas.create_text(150,90+yPos,fill="black",font="Times 13 bold",text="Valeurs annuels")
  canvas.create_text(150,120+yPos,fill="black",font="Times 11",text="Min : "+str("{:.2f}".format(getMinAnnee(dataset))))
  canvas.create_text(150,140+yPos,fill="black",font="Times 11",text="Max : "+str("{:.2f}".format(getMaxAnnee(dataset))))
  canvas.create_text(150,160+yPos,fill="black",font="Times 11",text="Score : "+str("{:.2f}".format(getScore(data_base,dataset)[0])))
  b = Button(fenetre, text="Graphique année", width=10, command=partial(getCourbeAnnee,dataset),background="white",foreground="black",activebackground="grey",activeforeground="black")
  b.place(x=100, y=180+yPos, anchor="nw", width=100, height=30)
  affichageMois(canvas,fenetre,dataset,yPos)

def affichageFenetre():
  fenetre = Tk()
  fenetre.title("Qualité des données")
  fenetre.geometry('1800x1000')
  canvas=Canvas(fenetre,bg='#FFFFFF',width=800,height=1000,scrollregion=(0,0,1500,1500))
  
  b = Button(fenetre, text="Comparatif année", width=10, command=getAllCourbesAnnee,background="white",foreground="black",activebackground="grey",activeforeground="black")
  b.place(x=800, y=20, anchor="nw", width=200, height=30)
  canvas.create_text(900,60,fill="red",font="Times 15 bold",text="Données propres")
  # Tableau propre

  affichageValeursAnnées(canvas,fenetre,data_base,0)

  # Tableau erreurs
  canvas.create_text(900,235,fill="red",font="Times 15 bold",text="Données erreurs")
  affichageValeursAnnées(canvas,fenetre,data_error,165)

  # Tableau savukoski
  canvas.create_text(900,400,fill="red",font="Times 15 bold",text="Données Savukoski kirkonkylä")
  affichageValeursAnnées(canvas,fenetre,data_savukoski,330)


  # Tableau helsinki
  canvas.create_text(900,565,fill="red",font="Times 15 bold",text="Données d'Helsinki")
  affichageValeursAnnées(canvas,fenetre,data_helsinki,495)

  # Tableau Oslo
  canvas.create_text(900,730,fill="red",font="Times 15 bold",text="Données d'Oslo")
  affichageValeursAnnées(canvas,fenetre,data_oslo,660)

  canvas.pack(side=LEFT,expand=True,fill=BOTH)
  fenetre.mainloop()

#
# SI
#
values = pd.read_excel('data/Climat.xlsx', sheet_name=0)
data_base=setValeursMois()

#
# SI-ERROR
#
error = pd.read_excel('data/Climat.xlsx', sheet_name=1)
data_error = getValeursMoisErreurCorrection(setValeursMoisErreur(error))

#
# Values opendata
#
savukoski = pd.read_excel('data/Savukoski_kirkonkyla.xlsx', sheet_name=2)
data_savukoski=getValeursMoissavukoski(savukoski)

#
# Values Helsinki
#
helsinki = pd.read_excel('data/Helsinki.xlsx',sheet_name=0)
data_helsinki=getValeursMoisHelsinki(helsinki)

#
# Values Oslo
#
oslo= pd.read_csv('data/Oslo.csv')
data_oslo=getValeursMoisCsv(oslo)

#
# Affichage
#
affichageFenetre()
