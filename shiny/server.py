from shiny import render
from shinywidgets import *
import ipyleaflet as mapmaker
import pandas as pd

def server(input, output, session):
	df = pd.read_csv("./data.csv", sep=",", encoding="utf-8")

	@output
	@render_widget
	def map():
		coordinates = [57.713, 22.391]
		return mapmaker.Map(basemap=mapmaker.basemaps.OpenStreetMap.Mapnik, 
							center=coordinates, zoom=3.3)
