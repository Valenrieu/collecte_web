from sys import exit
import datetime

try:
    import httpx

except (ModuleNotFoundError, ImportError):
    print("Les dependances n'ont pas ete installees, 'pip install -r requirements.txt'")
    exit(1)

KEYWORDS = ["q", "isHighlight", "title", "tags", "departmentId", "isOnView", "artistOrCulture",
			"medium", "hasImages", "getLocation", "dateBegin", "dateEnd"]

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/"
CLIENT = httpx.AsyncClient()

async def close_session():
    await CLIENT.aclose()

async def fetch_objects(metadataDate=None, departmentIds=None):
    url = BASE_URL+"objects?"

    if not metadataDate is None:
        try:
            datetime.date.fromisoformat(metadataDate)

        except ValueError as e:
            raise ValueError(str(e)+", date format must be YYYY-MM-DD.")

        url += "metadataDate="+metadataDate

        if not departmentIds is None:
            url += "&"

    elif not departmentIds is None:
        url += "departmentIds"+"="

        if type(departmentIds) in (tuple, list):
            for i in departmentIds:
                url += str(i)+"|"

            url = url[:-1] # Enlever le dernier "|"

        else:
            url += str(departmentIds)

    if url[-1]=="&":
        url = url[:-1]

    resp = await CLIENT.get(url)
    return resp.json()

async def fetch_object(id):
    resp = await CLIENT.get(BASE_URL+f"objects/{str(id)}")
    res = resp.json()

    # Tester si l'id est valide

    try:
        message = res["message"]
        raise ValueError(f"{str(id)} is not a valid id.")

    except KeyError:
        return res

async def fetch_departments(department=None):
	resp = await CLIENT.get(BASE_URL+"departments")
	resp = resp.json()
	res = {"departments":[]}

	try:
		dep = resp["departments"]

		for i in dep:
			id = i["departmentId"]

			if type(department) in (list, tuple):
				if id in department:
					res["departments"].append(i)

			elif type(department)==int:
				if id==department:
					res["departments"].append(i)
					break

	except KeyError:
		raise ValueError(f"{str(department)} is/are not valid id/s.")

	if len(res["departments"])==0:
		raise ValueError(f"{str(department)} is/are not valid id/s.")

	return res

async def fetch(**kwargs):
	url = BASE_URL+"search?"

	if "q" not in kwargs.keys():
		raise ValueError("Query must have a q parameter.")

	for i in kwargs:
		if i not in KEYWORDS:
			raise ValueError(f"{i} is not a valid keyword.")

		if i=="medium" or i=="geoLocation":
			url += i+"="

			if type(kwargs[i]) in (list, tuple):
				for j in kwargs[i]:
					url += str(kwargs[i])+"|"

				url = url[:-1]

			else:
				url += str(kwargs[i])

		if type(kwargs[i])==bool:
			kwargs[i] = str(kwargs[i]).lower()

		else:
			url += i+"="+str(kwargs[i])

		url += "&"

	if url[-1]=="&":
		url = url[:-1]

	resp = await CLIENT.get(url)
	return resp.json()

