from shiny import ui
from shinywidgets import *

CHOICES = ["Année d'acquisition",
		   "Année de début de création",
		   "Année de fin de création"]

app_ui = ui.page_fluid(
	ui.panel_title("La collection de peintures européennes du Metropolitanian Museum of Art"),

	ui.layout_sidebar(
		ui.panel_sidebar(
			ui.h2("Filtrer"),
			ui.input_selectize("variable", "Variable", choices=CHOICES, selected=CHOICES[0]),
			ui.input_slider("year_range", "Années", value=(1871, 2023), min=1871, max=2023),
			ui.p("Source : ", ui.a("https://www.metmuseum.org", href="https://www.metmuseum.org"))
		),

		ui.panel_main(
			output_widget("map"),
			ui.output_plot("word_cloud"),
			ui.output_plot("pie"),
			ui.output_plot("avg_time")
		)
	)
)
