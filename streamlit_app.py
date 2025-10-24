# Import python packages

import importlib, sys

def debug_snowpark():
    try:
        sp = importlib.import_module("snowflake.snowpark")
        print("snowflake.snowpark module:", sp)
        f = importlib.import_module("snowflake.snowpark.functions")
        print("snowflake.snowpark.functions module:", f)
    except Exception as e:
        print("Import error:", repr(e))
        print("sys.path:", sys.path)

debug_snowpark()

import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")

cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
#st.dataframe(data=my_df, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients: '
                                , my_df
                                , max_selections  = 5
                                 )
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
        