#!/usr/bin/env python3

from datetime import datetime
import os
import pandas as pd
import pdfplumber
import gradio as gr
from zipfile import ZipFile


df = pd.DataFrame()
mes = {"Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04", "Mayo": "05", "Junio": "06", "Julio":"07", "Agosto": "08","Septiembre": "09", "Noviembre": "11", "Octubre": "10", "Diciembre": "12"}
Nom = []
RUT = []
sol = []
des = []
hast = []
espe=[]

hoy=(datetime.today()).strftime("%d_%m_%Y")


def extraer(pdf):
	with pdfplumber.open(pdf) as temp:
		first_page = temp.pages[0]
		contenido = first_page.extract_text()
		nombre = contenido.split('por')[1].split(',')[0]
		rut = contenido.split('RUN')[1].split(',')[0].strip()
		solicitud = contenido.split('solicitud N°')[1].split('del')[0].strip()
		desde = contenido.split(solicitud + " del")[1].split(",")[0]
		hasta = contenido.split('una vigencia hasta el día')[1].split(".")[0].strip()
		desde_formato = desde.split('de')[1].split('del')[0].strip()
		formato_fecha = desde[:3].strip() + "/" + mes[desde_formato] + "/" + desde.split("del")[-1].strip()
		Nom.append(nombre)
		RUT.append(rut)
		sol.append(solicitud)
		des.append(formato_fecha)
		hast.append(hasta)

def agregar_lista(l):

	for archivo in l:
		#if archivo".pdf"):
			extraer(archivo)
	df["RUT"] = pd.Series(RUT)      
	df["Nombre"] = pd.Series(Nom)
	df["Especialidad"]=" "
	df["N° Resolución"] = pd.Series(sol)
	df["Desde"] = pd.Series(des)
	df["Hasta"] = pd.Series(hast)
	df["Fecha Renovación"]=pd.Series(hast)

def comparar_planillon(planillon):
	df1=pd.read_excel(planillon,header=3)
	df2=pd.DataFrame()
	#df2["RUT"]=df1["RUT"].map(str)+"-"+df1["DV"].map(str)
	df2["RUT"]=df1["RUT"].map(str)
	df2["ESPECIALIDAD"]=df1["ESPECIALIDAD"]
	
	for index, row in df.iterrows():
		for index1,row1 in df2.iterrows():
			if row["RUT"].split("-")[0]==row1["RUT"]:
				df.at[index,"Especialidad"]=row1["ESPECIALIDAD"]

def limpiar():
	Nom.clear()
	RUT.clear()
	sol.clear()
	des.clear()
	hast.clear()
	espe.clear()
	df.drop(df.index, inplace=True)

def all(files,planillon):
	agregar_lista(files)
	comparar_planillon(planillon)
	nombre_archivo = "Lic_"+hoy+".xlsx"
	a = df.to_excel(os.path.join(os.path.dirname(__file__),nombre_archivo))
	descarga = os.path.join(os.path.dirname(__file__),nombre_archivo)
	limpiar()
	df.drop(df.index, inplace=True)
	return descarga

with gr.Blocks() as demo:
	gr.Markdown("Seleccione licencias en formato PDF, luego selecciona planillón en formato Excel")
	out= gr.Markdown(" ")
	with gr.Row():
		gr.Markdown(" Licencias en PDF")
		pdfs= gr.File(file_count="multiple",interactive=True)
		gr.Markdown(" Planillón En Excel")
		excel= gr.File(file_count="single",interactive=True)
		limp_pdfs = gr.File.clear(pdfs,limpiar,pdfs,out)
			
			
	btn = gr.Button("Consolidar PDF's a Excel", variant="primary")
	#gr.Button.style(btn, full_width= True)
	nombre_archivo = "Lic_"+hoy+".xlsx"
	dir = os.path.join(os.path.dirname(__file__),nombre_archivo)
	descarga= gr.File()
	
	btn.click(all, [pdfs,excel], descarga)
	
	
	
if __name__ == "__main__":
	demo.launch()
	
	
	
	
