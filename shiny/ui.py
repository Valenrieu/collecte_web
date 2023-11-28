from shiny import ui
from shinywidgets import *

app_ui = ui.page_fluid(
	ui.panel_title("Test"),
	output_widget("map")
)
