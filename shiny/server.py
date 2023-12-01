from shiny import render, reactive, ui
from shinywidgets import *
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import utils

def server(input, output, session):
	df = pd.read_csv("./data/data.csv", sep=",", encoding="utf-8")
	country_count = df.groupby("country")["country"].count().reset_index(name="count")
	country_count = utils.translate_countries_french(country_count)
	values = {"Année d'acquisition":"accessionYear",
	   		  "Année de début de création":"objectBeginDate",
	   		  "Année de fin de création":"objectEndDate"}

	@output
	@render_widget
	def map():
		column = values.get(input.variable())

		dft = df.loc[(df[column]>=input.year_range()[0]) & (df[column]<=input.year_range()[1])]
		country_countt = dft.groupby("country")["country"].count().reset_index(name="count")
		country_countt = utils.translate_countries_french(country_countt)

		map = px.choropleth(country_countt, locationmode="country names", locations="country",
							color="count", labels={"count":"Nombre d'oeuvres", "country":"Pays"},
							scope="europe", color_continuous_scale="Viridis",
							title="Distribution géographique des oeuvres",
							hover_name="pays", hover_data={"country":False})
		map.update_layout(width=800, height=500)
		
		return map

	@output
	@render.plot
	def word_cloud():
		column = values.get(input.variable())
		dft = df.loc[(df[column]>=input.year_range()[0]) & (df[column]<=input.year_range()[1]), "terms"]
		words = ""

		for i in range(len(dft)):
			try:
				for j in eval(dft.loc[i]): # eval(str) -> list
					words += j.capitalize()+" "

			except (TypeError, KeyError):
				continue

		if len(words)==0:
			words = "Not Enough Data"

		plot, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
		wordcloud = WordCloud(max_font_size=40).generate(words)
		plot = plt.imshow(wordcloud, interpolation="bilinear")
		ax.set_title("Mots clés descriptifs des oeuvres les plus cités")
		plt.axis("off")

		return plot, ax

	@output
	@render.plot
	def pie():
		column = values.get(input.variable())
		dft = df.loc[(df[column]>=input.year_range()[0]) & (df[column]<=input.year_range()[1])]
		data = dft.groupby("artistGender")["artistGender"].count().reset_index(name="count")
		fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
		wedges, texts, autotexts = plt.pie(data["count"], labels=data["artistGender"],
										   autopct="%1.1f%%", radius=0.75, colors=["darkorange", "lightseagreen"])
		ax.set_title("Répartition des sexes des artistes")

		return fig, ax

	@output
	@render.plot
	def avg_time():
		column = values.get(input.variable())
		dft = df.loc[(df[column]>=input.year_range()[0]) & (df[column]<=input.year_range()[1])]
		data = dft.groupby("country")["constructionTime"].mean().reset_index(name="avg")
		data = utils.translate_countries_french(data)
		data.sort_values(by="avg", inplace=True, ascending=False)

		if len(data)>10:
			data = data.iloc[0:10]

		fig, ax = plt.subplots()
		ax.bar(data["pays"], data["avg"], color="lightseagreen")
		ax.set_title("Temps de création moyen d'une oeuvre par pays")
		ax.set_ylabel("Temps en années")
		ax.set_xlabel("Pays")

		return fig, ax

	@reactive.Effect(priority=1)
	@reactive.event(input.variable)
	def update_slider():
		column = values.get(input.variable())
		min = df[column].min()
		max = df[column].max()
		ui.update_slider("year_range", value=(min, max), min=min, max=max)
