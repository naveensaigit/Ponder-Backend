import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_df(URL):
  r = requests.get(URL)
  soup = BeautifulSoup(r.content, 'html5lib')
  tb = soup.find_all('table')
  if len(tb) <= 2:
    print('ERROR OCCURS FOR THIS URL: ',URL)
    return {"response": []}
  df = pd.read_html(str(tb[2]), header=0)[0]

  links = []
  for tag in tb[2].find_all("a"):
    if tag.has_attr("href") and "http" in tag["href"] and "edit" not in tag["href"]:
      links.append(tag["href"])

  links = np.array(links, dtype=str)

  links = links.reshape(-1,5)

  df.loc[:, ["Mirrors", "Mirrors.1", "Mirrors.2", "Mirrors.3", "Mirrors.4"]] = links
  df = df[(df["Language"] == "English") & (df["Extension"] == "pdf")]

  mirrors = df["Mirrors"]
  img_links = []
  for mirror in mirrors:
    r = requests.get(mirror)
    soup = BeautifulSoup(r.content, 'html5lib')
    link = soup.find('img', attrs={"alt": "cover"})
    if link is not None:
      img_links.append("http://library.lol" + link["src"])
    else:
      img_links.append("https://mrb.imgix.net/assets/default-book.png")

  df["icons"] = img_links
  df = df.drop("Edit", 1)
  if type(df) == dict:
    print("---------------------------------Dict problem------------------------------------------------------------------------------", URL)
  return df