import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page
streamlit.dataframe(fruits_to_show)
#creating a function for fruit advice
def get_fruitvice_advice(fruit_selected):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_selected)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
streamlit.header('FruityVice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('please select a fruit to get information')
  else:
    returned_output = get_fruitvice_advice(fruit_choice)
    streamlit.dataframe(returned_output)
except urlerror as e:
  streamlit.error()
streamlit.write('The user entered ', returned_output)


# normalize your json result
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#streamlit.text(fruityvice_normalized)
# change output into a table format
#streamlit.dataframe(fruityvice_normalized)
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

fruit_added = streamlit.text_input('what fruit would you like to add:','kiwi')
streamlit.write('Thanks for adding',fruit_added)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
