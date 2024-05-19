from bs4 import BeautifulSoup
import requests
from requests import Timeout
import re
import pandas as pd
import numpy as np

########################################################################################################################TASK1
max_retry = 100
url1 = 'https://lastsecond.ir/restaurants/rafsanjan?sort=3'
url2 = 'https://lastsecond.ir/restaurants/rafsanjan?sort=3&page=2'

for i in range(max_retry):
    try:
        page1 = requests.get(url1)
        print(page1.status_code)
        soup1 = BeautifulSoup(page1.text, 'lxml')
        # print(soup)
        break
    except Timeout as to:
        print("time out for first page")
###
for i in range(max_retry):
    try:
        page2 = requests.get(url2)
        print(page2.status_code)
        soup2 = BeautifulSoup(page2.text, 'lxml')
        # print(soup)
        break
    except Timeout as to:
        print("time out for second page")
##$$$$

##$$$$
###
name = soup1.find_all('small', class_='title__en')
name_column = [title.text.strip() for title in name]
# @@@@@@@@
name2 = soup2.find_all('small', class_='title__en')
name_column2 = [title.text.strip() for title in name2]
name_column.extend(name_column2)
###

###
score = soup1.find_all('div', class_='score-no score-no__md')
score = score[:-3]
temp4 = [title.text.strip() for title in score]
score_column = [re.sub("[^0.0-9.0]", "", item) for item in temp4]
score_column = [item for item in score_column if item]
# @@@@@@@@
score2 = soup2.find_all('div', class_='score-no score-no__md')
score2 = score2[:-3]
temp44 = [title.text.strip() for title in score2]
score_column2 = [re.sub("[^0.0-9.0]", "", item) for item in temp44]
score_column2 = [item for item in score_column2 if item]
score_column.extend(score_column2)

###

###
review = soup1.find_all('small', class_='count count__md')
temp1 = [title.text.strip() for title in review]
review_column = [re.sub("[^0-9]", "", item) for item in temp1]
review_column = [item for item in review_column if item]
# @@@@@@@@
review2 = soup2.find_all('small', class_='count count__md')
temp11 = [title.text.strip() for title in review2]
review_column2 = [re.sub("[^0-9]", "", item) for item in temp11]
review_column2 = [item for item in review_column2 if item]
review_column.extend(review_column2)
while len(review_column) < 37:
    review_column.append(0)
###

###
rate = soup1.find_all('div', class_='details__rank')
strings_list = [str(item) for item in rate]
rate_column = [re.findall(r'<span>(\d+)', str(BeautifulSoup(item, "html.parser").span))[0] for item in strings_list]
# @@@@@@@@
rate2 = soup2.find_all('div', class_='details__rank')
strings_list2 = [str(item) for item in rate2]
rate_column2 = [re.findall(r'<span>(\d+)', str(BeautifulSoup(item, "html.parser").span))[0] for item in strings_list2]
rate_column.extend(rate_column2)
####

###
location = soup1.find_all('div', class_='details__location')
replacement = 'رفسنجان / ایران'
location_column = [replacement for _ in location]
# @@@@@@@@@@
location2 = soup2.find_all('div', class_='details__location')
replacement2 = 'رفسنجان / ایران'
location_column2 = [replacement2 for _ in location2]
location_column.extend(location_column2)
###

###
p_keys = np.arange(100, 137, dtype=int)
values = [(int(p_key),) for p_key in p_keys]
###

########################################################################################################################TASK2


review_column_int = [int(x) for x in review_column]
score_column_float = [float(x) for x in score_column]
rate_column_int = [int(x) for x in rate_column]
p_keys_int = [int(x) for x in p_keys]

x = sum(review_column_int)
res = [((num + 1) ** 3 * ((num + 1) / x)) for num in
       review_column_int]
review_score_res = [(x * (y + 1) * 0.65) for x, y in zip(res, score_column_float)]
rate_res = [((27 - x) * 0.35) for x in rate_column_int]
normalized_column = [(x + y) for x, y in zip(review_score_res, rate_res)]
normalized_column = np.round(normalized_column, decimals=3)

bins = [0, 2, 9, 9.5, 10.5, 15]
labels = ['E', 'D', 'C', 'B', 'A']
categories = np.digitize(normalized_column, bins=bins, right=True)
category_column = [labels[i - 1] for i in categories]

data = {'category': category_column, 'name': name_column, 'score': score_column_float, 'review': review_column_int,
        'rate': rate_column_int,
        'normalized': normalized_column, 'location': location_column}
df = pd.DataFrame(data)
df.to_csv('output.csv', index=False, encoding='utf-8-sig')
