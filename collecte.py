import metmuseum
import time
import asyncio
import pandas as pd
from termcolor import cprint

REQUEST_LIMIT = 80

def clean_data_frame(df):
	df.dropna(subset=["objectID"], inplace=True)

async def fetch_data():
	request_counter = 0
	tasks = []
	res = []
	requests_counter = 0
	cprint(f"{time.strftime('%X')}", "light_cyan", end="")
	print(" Envoi des requetes")

	# Recupere les id des peintures crees en Europe
	# Je n'ai pas utilise le departement peintures europeennes
	# car certaines peintures appartiennent a d'autres departements
	ids = await metmuseum.fetch(geoLocation="Europe", medium="Paintings", q="\"\"")
	requests_number = ids["total"]
	print("Requete ", end="")
	cprint("0", "light_yellow", end="")
	print("/", end="")
	cprint(f"{str(requests_number)}", "light_magenta", end="")

	for id in ids["objectIDs"]:
		if request_counter==REQUEST_LIMIT:
			print("\rRequete ", end="")
			cprint(f"{requests_counter}", "light_yellow", end="")
			print("/", end="")
			cprint(f"{str(requests_number)}", "light_magenta", end="")

			res += await asyncio.gather(*tasks)
			time.sleep(1.2)
			request_counter = 0
			tasks = []

		tasks.append(asyncio.ensure_future(metmuseum.fetch_object(id)))
		requests_counter += 1
		request_counter += 1

	if requests_number % REQUEST_LIMIT != 0:
		print("\rRequete ", end="")
		cprint(f"{requests_counter}", "light_yellow", end="")
		print("/", end="")
		cprint(f"{str(requests_number)}", "light_magenta", end="")
		res += await asyncio.gather(*tasks)

	print()
	cprint(f"{time.strftime('%X')}", "light_cyan", end="")
	print(" Exportation des donnees vers shiny/data.csv")

	df = pd.json_normalize(res)
	clean_data_frame(df)
	df.to_csv("./shiny/data.csv", index=False, encoding="utf-8")

async def main():
	beginning_time = time.time()
	print("===== Collecte de donnees sur ", end="")
	cprint("https://www.metmuseum.org", "light_green", end="")
	print(" =====")

	task1 = asyncio.create_task(fetch_data())
	await task1

	if task1.done():
		elapsed_time = time.gmtime(time.time()-beginning_time)
		print(f"Temps d'execution : ", end="")
		cprint(f"{time.strftime('%M:%S', elapsed_time)}", "red")

		await metmuseum.close_session()

if __name__=="__main__":
	asyncio.run(main())

