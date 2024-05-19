import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np

########################################################################################################################TASK4

mydb = mysql.connector.connect(host='localhost', user='root', password='', database='Task')

mycursor = mydb.cursor()

df = pd.read_csv('output.csv')

p_keys = np.arange(100, 137, dtype=int)
values = [(int(p_key),) for p_key in p_keys]

name = df['name'].values
score = df['score'].values
review = df['review'].values
rate = df['rate'].values
normalized = df['normalized'].values
location = df['location'].values

############insert into first table

# sqlFormula = "INSERT INTO restaurants (restaurant_id,restaurant_name,restaurant_address)VALUES (%s,%s,%s)"
# restaurants = []
# for i in range(len(p_keys)):
#     restaurants.append([int(p_keys[i]), name[i], location[i]])
# mycursor.executemany(sqlFormula, restaurants)

############insert into second table

# p_keys = [int(x) for x in p_keys]
# score = [float(x) for x in score]
# review = [int(x) for x in review]
# rate = [int(x) for x in rate]
# normalized = [float(x) for x in normalized]
# data = []
# for i in range(len(score)):
#     data.append([p_keys[i], score[i], review[i], rate[i], normalized[i]])
# sqlFormula = "INSERT INTO data (restaurant_id,score,review,rate,normalized)VALUES (%s,%s,%s,%s,%s)"
# mycursor.executemany(sqlFormula, data)


# mydb.commit()
# mydb.close()
