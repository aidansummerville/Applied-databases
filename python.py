##importing the packages needed for this program

import pymysql 
import pymongo






def main():
      ##repeats back to the main menu
    while True:
      display_menu()
      ## records menu option
      choice = input("choice:")
      

      ## chooses related to menu option numbers and the functions needed to call to get them to work
      if (choice == "1"):
            get_15() 
      elif (choice == "2"):
            param = get_lessorgreat()
            number = get_number()
            cities_pop(number,param)
      elif (choice == "3"):
            name = city_name()
            code = country_code()
            dis = district()
            pop = population()
            try:
                new_city(name, code, dis, pop)
                ## prints an error is the country code dosent exist
            except pymysql.err.IntegrityError as e:
                  print("Error,", code, "does not exist")
      elif (choice == "4"):
            size = engine_size()
            car_engine(size)
      elif (choice == "5"):
            newID = id_input()
            newReg = reg_input()
            size = engine_size()
            new_car(newID, newReg, size)
      elif (choice == "6"):
            name = country_input()
            country_name(name)
      elif (choice == "7"):
            param = get_lessorgreat()
            number = get_number()
            country_pop(number, param)
            ##ends the program
      elif (choice == "x"):
            break
      ## anything other than 1-7 or x it diplays the program again
      else: 
            display_menu()



##creates the menu table
def display_menu():
    print('MENU')
    print('=====')
    print('1 - View 15 Cities')
    print('2 - View Cities by population')
    print('3 - Add New City')
    print('4 - Find Car by Engine Size')
    print('5 - Add New Car')
    print('6 - View Countries by name')
    print('7 - View Countries by population')
    print('x - Exit application')



## connects to mysql
conn = None

def connect():
      global conn
      conn = pymysql.connect(host="localhost", user="root", password="manu2006", db="world", cursorclass=pymysql.cursors.DictCursor)


## gets the first 15 citys and dipplays them
def get_15():
      if (not conn):
            connect();
      
      query = "select name, countrycode, district, population from city limit 15"


      with conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            for x in rows:
                 print( x["name"], "|", x["countrycode"], "|", x["district"], "|", x["population"])

## gets the user to enter < = >
def get_lessorgreat():
      return input("Enter < = or > : ")

## enter a number
def get_number():
      return input("Enter a number : ")

## displays the citys < > or = relatetd to the number inputed
def cities_pop(number,param):
      if (not conn):
            connect();
      
      if (param == ">"):
          query = "select name, countrycode, district, population from city where population > %s"
      elif (param == "<"):
            query = "select name, countrycode, district, population from city where population < %s"  
      elif (param == "="):
            query = "select name, countrycode, district, population from city where population = %s"


      with conn:
            cursor = conn.cursor()
            cursor.execute(query, (number))
            rows = cursor.fetchall()
            
            for x in rows:
                 print( x["name"], "|", x["countrycode"], "|", x["district"], "|", x["population"])


## gets the countrys of population < > or + the number inputed
def country_pop(number, param):
      if (not conn):
            connect();
      
      if (param == ">"):
          query = "select Code, name, Continent, population from country where population > %s"
      elif (param == "<"):
            query = "select Code, name, Continent, population from country where population < %s"  
      elif (param == "="):
            query = "select Code, name, Continent, population from country where population = %s"


      with conn:
            cursor = conn.cursor()
            cursor.execute(query, (number))
            rows = cursor.fetchall()
            
            for x in rows:
                 print( x["Code"], "|", x["name"], "|", x["Continent"], "|", x["population"])

## gets city name input

def city_name():
      return input("Enter City Name : ")

## gets country code input      
def country_code():
      return input("Country Code : ")

## gets district input
def district():
      return input("District : ")

## gets population input
def population():
      return input("Population : ")


## checkingif coutry code exists
def check_country(code):
        if (not conn):
            connect();

      
        query = " select * from city where countrycode = %s "


        with conn:
            cursor = conn.cursor()
            cursor.execute(query, (code))
            x = cursor.fetchall()
            
       
## inserts new row into city
def new_city(name, code, dis, pop):
      if (not conn):
            connect();

      
      query = "insert into city(name, countrycode, district, population) values(%s, %s, %s, %s)"


      with conn:
            cursor = conn.cursor()
            cursor.execute(query, (name, code, dis, pop))
            x = cursor.fetchall()
            print(x)

##  input country
def country_input():
      return input("Country Name : ")


## gets countrys that match the letters input
def country_name(name):
      if (not conn):
            connect();

      
      query = " select name, continent, population, headofstate from country where name like  %s "


      with conn:
            cursor = conn.cursor()
            cursor.execute(query, ('%' + name + '%',))
            rows = cursor.fetchall()
            
            for x in rows:
                 print( x["name"], "|", x["continent"], "|", x["population"], "|", x["headofstate"])


##gets engine size float number
def engine_size():
      return float(input("Engine size : "))


##connects the mongodb
myclient = None

def connect2():
      global myclient
      myclient = pymongo.MongoClient()
      myclient.admin.command('ismaster')
      

## finds matchs for car size
def find(size):
      mydb = myclient["project"]
      docs = mydb["docs"]
      query = { "car.engineSize": size}
      car = docs.find(query)
      print(car)
      for p in car:
            print(p)


## calls find
def car_engine(size):
      if (not myclient):
            try:
                  connect2()
                  find(size)
            except Exception as e:
                  print("error", e)

##takes id input
def id_input():
       return int(input("ID : "))


##takes reg input
def reg_input():
      return input("Registration : ")


## inserst id reg an engine size into collection
def insert(newID, newReg, size):
      mydb = myclient["project"]
      docs = mydb["docs"]
      x = "_id"
      r = "reg"
      es = "engineSize"
      c = "car"
      newdocs = [{x:newID, c:{r:newReg, es:size}}]
      docs.insert(newdocs)

## calls inser
def new_car(newID, newReg, size):
      if (not myclient):
            try:
                  connect2()
                  insert(newID, newReg, size)
            except Exception as e:
                  print("error", e)


if __name__ == '__main__':
      main()

