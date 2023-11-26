import metmuseum
import time
import asyncio
import pandas as pd
from termcolor import cprint

REQUEST_COUNTER = 0
REQUEST_LIMIT = 80

async def fetch_data():
	global REQUEST_COUNTER
	tasks = []
	res = []
	requests_counter = 0
	cprint(f"{time.strftime('%X')}", "light_cyan", end="")
	print(" Envoi des requetes")

	# Recuperer les objets des collections peintures europeennes, sculptures europeennes
	# et art greco-romain
	a = await metmuseum.fetch_objects(departmentIds=[11])
	requests_number = a["total"]
	print("Requete ", end="")
	cprint("0", "light_yellow", end="")
	print("/", end="")
	cprint(f"{str(requests_number)}", "light_magenta", end="")

	for id in a["objectIDs"]:
		if REQUEST_COUNTER==REQUEST_LIMIT:
			print("\rRequete ", end="")
			cprint(f"{requests_counter}", "light_yellow", end="")
			print("/", end="")
			cprint(f"{str(requests_number)}", "light_magenta", end="")

			res += await asyncio.gather(*tasks)
			time.sleep(1.2)
			REQUEST_COUNTER = 0
			tasks = []

		tasks.append(asyncio.ensure_future(metmuseum.fetch_object(id)))
		requests_counter += 1
		REQUEST_COUNTER += 1

	if requests_number % REQUEST_LIMIT != 0:
		print("\rRequete ", end="")
		cprint(f"{requests_counter}", "light_yellow", end="")
		print("/", end="")
		cprint(f"{str(requests_number)}", "light_magenta", end="")
		res += await asyncio.gather(*tasks)

	print()
	cprint(f"{time.strftime('%X')}", "light_cyan", end="")
	print(" Exportation du fichier vers /shiny/data.csv")
	df = pd.json_normalize(res)
	df.to_csv("./shiny/data.csv", index=False, encoding="utf-8")

async def main():
	beginning_time = time.time()
	print("===== Collecte de donnees sur ", end="")
	cprint("https://www.metmuseum.org", "green", end="")
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

