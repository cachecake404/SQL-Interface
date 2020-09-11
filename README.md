# SQL-Interface

A test project created to try and store famous quotes as records in SQL tables but as seralized pickle objects. 
This is done so that if the connection is lost to SQL then we can later update the tables when the connection is reestablished.

A simple CLI interface allows for CRUD opertaions.

## Run Guide

Run your SQL server and then make a database called "quo_python" with it being on localhost. 
(The names for this can be changed by editing the script if desired) 

Leave the username as "user" and password empty. (This can also be modified in the script)

Then run Quotes_Managment_System.py script.
