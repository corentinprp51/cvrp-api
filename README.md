# CVRP API
## _A CVRP Api builded for UPC - Computer Science Department_

[![UPC Computer Sciences](https://www.lsi.upc.edu/~gavalda/page/cslogo.png)](https://www.cs.upc.edu/)

CVRP API is an api of resolving routing capacities problems with the gurobipy algorithm

## Prerequisites
Before installing the project, you need some prerequisites
- Install Python3 and pip
- Install Flask and add it to your environnment variables
- Have a licence of gurobipy

## Installation
To install the project there are some things you need to do
- Create a .env file

```
DATABASE_URL=*URL* #URL of your database connection
```

- Create a .flaskenv file

```
FLASK_APP=app #define the file where the Flask app is running
FLASK_DEBUG=True #debug mode active in development mode
```


- Install all dependencies
```shell
pip install -r requirements.txt
```

## Run the web server
```
flask run
```
