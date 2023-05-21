import json
import requests
import pymysql

response= requests.get("https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries%2Bstates%2Bcities.json")

json_data=response.json()

cn=[]
st=[]
ct=[]
for country in json_data:
    country['timezones']=str(country['timezones'])
    country['translations']=str(country['translations'])
    if len(country['states'])!=0:
        for state in country['states']:
            a={'country_id':country['id']}
            state.update(a)
            if len(state['cities'])!=0:
                for city in state['cities']:
                    b={'state_id':state['id']}
                    city.update(b)
                    ct.append(city)
            state.pop('cities','')
            st.append(state)
    country.pop('states','')
    cn.append(country)
    
    

# creating database in mysql
try:
    con=pymysql.connect(user='root',password='root',host='localhost')
    if con:
        print('Connection Successfully Established')
    else:
        print('Connection Failed')
    cur=con.cursor()
    query="create database countriesStatesCities"
    cur.execute(query)
    print('Database created successfully')
    query2="alter database countriesStatesCities character set utf8mb4 collate utf8mb4_unicode_ci"
    cur.execute(query2)
    print('database altered for non-ascii string')
except pymysql.DatabaseError as e:
    if con:
        con.rollback()
        print('There is a problem : ',e)
finally:
    if cur:
        cur.close()
    if con:
        con.close()

# Create Tables
try:
    con=pymysql.connect(user='root',password='root',host='localhost',database='countriesStatesCities')
    if con:
        print('Connection established successfully')
    else:
        print('Connection not established')
    cur=con.cursor()
    query1="create table countries(id int,name varchar(255),iso3 varchar(255),iso2 varchar(255),numeric_code varchar(255),phone_code varchar(255),capital varchar(255),currency varchar(255),currency_name varchar(255),currency_symbol varchar(255),tld varchar(255),native varchar(255),region varchar(255),subregion varchar(255),timezones text,translations text,latitude varchar(255),longitude varchar(255),emoji varchar(255),emojiU varchar(255),primary key(id))"
    cur.execute(query1)
    print('countries table created successfully')
    query2="create table states(id int,name varchar(255),state_code varchar(255),latitude varchar(255),longitude varchar(255),type varchar(255),country_id int,primary key(id),constraint fkst foreign key(country_id) references countries(id))"
    cur.execute(query2)
    print('states table created successfully')
    query3="create table cities(id int,name varchar(255),latitude varchar(255),longitude varchar(255),state_id int,primary key(id),constraint fkct foreign key(state_id) references states(id))"
    cur.execute(query3)
    print('cities table created successfully')
except pymysql.DatabaseError as e:
    if con:
        con.rollback()
        print('There is a problem : ',e)
finally:
    if cur:
        cur.close()
    if con:
        con.close()

# inserting data into tables
try:
    con=pymysql.connect(user='root',password='root',host='localhost',database='countriesStatesCities')
    if con:
        print('Connection Successfully Established')
    else:
        print('Connection Failed')
    cur=con.cursor()
    cur=con.cursor()
    query1="insert into countries(id,name,iso3,iso2,numeric_code,phone_code,capital,currency,currency_name,currency_symbol,tld,native,region,subregion,timezones,translations,latitude,longitude,emoji,emojiU)values(%(id)s,%(name)s,%(iso3)s,%(iso2)s,%(numeric_code)s,%(phone_code)s,%(capital)s,%(currency)s,%(currency_name)s,%(currency_symbol)s,%(tld)s,%(native)s,%(region)s,%(subregion)s,%(timezones)s,%(translations)s,%(latitude)s,%(longitude)s,%(emoji)s,%(emojiU)s)" 
    cur.executemany(query1,cn)
    con.commit()
    print('Record inserted into countries successfully')
    query2="insert into states (country_id,id,name,state_code,latitude,longitude,type) values(%(country_id)s,%(id)s,%(name)s,%(state_code)s,%(latitude)s,%(longitude)s,%(type)s)"
    cur.executemany(query2,st)
    con.commit()
    print('Record inserted into states successfully')
    query3="insert into cities (state_id,id,name,latitude,longitude) values(%(state_id)s,%(id)s,%(name)s,%(latitude)s,%(longitude)s)"
    cur.executemany(query3,ct)
    con.commit()
    print('Record inserted into cities successfully')
except pymysql.DatabaseError as e:
    if con:
        con.rollback()
        print('There is a problem : ',e)
finally:
    if cur:
        cur.close()
    if con:
        con.close()