from shiny import render

def server(input, output, session):
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"
