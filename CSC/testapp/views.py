from django.shortcuts import render
import pymysql
#from operator import itemgetter


# Create your views here.

# creating connection with dataase
cnx = pymysql.connect(user='root', password="root", host="localhost", database='countriesStatesCities')
cursor = cnx.cursor()

#index page where the form and result is populated.
def index(request):
    query="Select name,id,iso2,emoji from countries"
    cursor.execute(query)
    country=cursor.fetchall()
    context={"country":country}
    return render(request,"index.html",context)

#  to populate state dropdown when country is selected. 
def state_view(request,id):
    query="select name,id,state_code from states where country_id="+str(id)+" order by name"
    cursor.execute(query)
    states=cursor.fetchall()
    context={"states":states}
    return render(request,"state.html",context)

#  to populate city dropdown when state is selected.
def city_view(request,id):
    query="select name,id from cities where state_id="+str(id)+" order by name"
    cursor.execute(query)
    cities=cursor.fetchall()
    if cities:
        context={"cities":cities}
    else:
        context={"cities":["",0]}
    return render(request,"city.html",context)