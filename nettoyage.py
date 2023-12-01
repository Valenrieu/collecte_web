import json

with open("nationalities.json", "r") as file:
	NATIONALITIES = json.load(file)

def delete_columns(df):
	df = df[["objectID", "isHighlight", "accessionYear", "isPublicDomain",
			 "objectName", "artistDisplayName", "artistNationality",
			 "artistGender", "objectBeginDate", "objectEndDate",
			 "country", "tags"
			]]

	return df

def extract_tags(row):
	res = []

	try:
		for i in row["tags"]:
			res.append(i["term"])

		row["terms"] = res

	except TypeError:
		row["terms"] = float("NaN")

	return row

def complete_values(row):
	countries = {"Flemish":"Belgium", "North France":"France",
                 "Flanders":"Belgium", "italy":"Italy", "German":"Germany"}

	if row["artistGender"]=="":
		row["artistGender"] = "Homme"

	else:
		row["artistGender"] = "Femme"

	if row["country"]!="":
		row["country"] = countries.get(row["country"], row["country"])

	elif row["artistNationality"]!="":
		row["country"] = NATIONALITIES.get(row["artistNationality"])

	return row

def drop_rows(df):
	invalid_countries = [None, "Japan", "Canada", "Brazil", "South Africa",
						 "Argentina", "Undefined", "China", "United States"]

	df.dropna(subset=["country"], inplace=True)
	indexes = df[df['country'].isin(invalid_countries)].index
	df.drop(indexes, inplace=True)

def delete_tags(df):
	df = df[["objectID", "isHighlight", "accessionYear", "isPublicDomain",
			 "objectName", "artistDisplayName", "artistNationality",
			 "artistGender", "objectBeginDate", "objectEndDate",
			 "country", "terms", "constructionTime"
			]]

	return df

def clean(df):
	df.dropna(subset=["objectID"], inplace=True)
	df = delete_columns(df)
	df = df.apply(complete_values, axis=1)
	drop_rows(df)
	df["constructionTime"] = df["objectEndDate"] - df["objectBeginDate"]
	df["terms"] = float("NaN")
	df = df.apply(extract_tags, axis=1)
	df = delete_tags(df)
	return df
