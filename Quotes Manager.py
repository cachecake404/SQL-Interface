import pickle
import string
import MySQLdb
objlis = {}#Object dictionary to store all objects

#Defining class

print "                          Quotes Storage System" 


#Setting online or offline
onstatus = False #Boolean to check if online or offline later.
dbcheck = False #Making boolean value to prevent repeated requests to DB which causes xamp to crash.
tbcheck = False #Making boolean value to prevent repeated requests to TB which causes xamp to crash.

#First Check if database exsists

while True:
    try:     
        if dbcheck == True and onstatus == False:
            break
        if dbcheck == False:
                db = MySQLdb.connect(host = 'localhost',user = 'root' , passwd = '',db = 'quo_python')
                dbcheck = True#Sets to true if no error triggered
        onstatus = True
        break
    except:
        print "\n\nCould not establish a connection , Please Run MySQL service using \ntools like xampp and make sure you create a database 'quotes_python'" #Two print statments seperate just be able to use sniping tool.
        print "using a tool like MySQLworkbench and set host name as localhost and \nuser as root with no password to procced in online mode.\n"
        while True:
                choice = raw_input("Would you like to proceed in offline mode? ")
                if choice.lower() == 'yes':
                    onstatus = False
                    dbcheck = True #Setting to true so that we know the user want to go offline mode and we make it so to break previous loop
                    break
                    
                elif choice.lower() == 'no':
                    print "\nTrying to connect again \n "
                    dbcheck = False
                    break
                else:
                    print "Please enter a 'yes' or a 'no' as an answer! "

###Checking if new user and if so create a new table for data entery.
while onstatus == True:
    try:
        if tbcheck == False:
                cursor = db.cursor()
                cursor.execute("select * from quo_python.quotable;")
                data = cursor.fetchall() # function that returns the data in form tuple
                tbcheck = True
        if tbcheck == True and  onstatus == False:
            break
        break
    except:
        while True:
            a = raw_input("There Exsists no table created for operation on your current database do you wish to create a new table?  ")
            a = string.lower(a)

            if   a == "yes":
                cursor.execute("create table quotable (ID int primary key not null  , Name varchar(50) , Quote varchar(50)); ")
                print "Table has been created!\n"
                tbcheck = False 
                break
            elif a == "no":
                while True:
                    choice = raw_input("Would you like to proceed in offline mode? ")
                    if choice.lower() == 'yes':
                        onstatus = False
                        tbcheck = True
                        break
                    elif choice.lower() == 'no':
                        print "\n Then please make table and try again. \n "
                        tbcheck = False
                        break
                    else:
                        print "Please enter a 'yes' or a 'no' as an answer! "
                 



#Making a function to print value of table in a much better way.

def pinter2(x): #Taking the the data value as x an argument

        ls = [] # To contain values of the tuple which was within the tuple , all the column values
        conum = 0 #Counter for putting space for numofil

        for i in x:# Loop to put in values of column within data(tuple) passed as an argument.
            for j in range(len(i)):
                ls.append(i[j])
            numofil = len(i)

        # ls will contain all values for column from row 0 to n

        
        if len(ls) > 3: #To show  if there are more than 1 row
            print "ID , Name , Quote is: \n"
            pinter(x)

        else:
            roll = ls[0]
            name = ls[1]
            quote = ls[2]
            print "\nUser ID is: ",ls[0]
            print "Name is: ",ls[1]
            print "Favourite Quote is: ",ls[2]

#Defining the class for quote managment system.

class quotes():
            def __init__(self,idi,quote,name):
                self.id = idi
                self.name = name
                self.quote=quote
            def display(self):
                print "\nOkay ID is ",self.id
                print "Name is ",self.name
                print "Your favourite quote is '",self.quote,"'\n"
            def register(self): #Function to register online database.
                try:
                    cursor.execute("insert into quotable (ID,Name,Quote) values("+str(self.id)+",'"+str(self.name)+"','"+str(self.quote)+"');")
                    db.commit()
                except Exception as eror:
                    db.rollback()
                    print "You had an error it was that: \n\n\n"
                    print eror
            def ondisplay(self):
                cursor.execute("select * from quo_python.quotable where id="+str(self.id)+";")
                data = cursor.fetchall()
                return data #This can be used later in pinter2
            def deldbob(self):
                cursor.execute("delete from quo_python.quotable \nwhere id="+str(self.id)+";")
                db.commit()
                
                
            

#Now we load any previous Objects after defining class , You must load after defining class.
try:
    p = open('pick.dat','rb')
    objlis = pickle.load(p)
    print "\nStatus Report:\nPrevious Objects Loaded!\nOnline Status:",onstatus
except:
    pass

#Now user interface with user input with offline or online mode set.
while True:
    try:
        

        ch1 = int(raw_input("\nEnter: \n 1.To Register new User \n 2.Check User Details \n 3.Change Quote for user \n 4.Register User to database \n 5.Check User Details From Database \n 6.Delete User  \n 7.Save and Exit\n\n"))
        if ch1==1:
            no = int(raw_input("Enter the number of users you want to register: "))
            for i in range(len(objlis),len(objlis)+no):
                #Starting from the len of list because we don't want to mess up assigning of ID which should be unique and to account for the fact when we load x number
                #of previous objects from pickle it should start from that particular ID and ending with len(objlis)+no so it runs the loop that number of times.
                namaya = raw_input("Enter your name: ")
                quote = raw_input("Enter your favourite quote: ")
                while True:
                    idi=int(raw_input("Enter you unique ID: "))
                    if objlis.has_key(idi) == True:
                        print "The User ID is already taken try. "
                    else:
                        break
                obj = quotes(idi,quote,namaya) #  i Assigns The Id
                objlis.update({idi:obj})
                print "User has been Registered under the ID ",idi
        if ch1==2:
            idi=int(raw_input("\nEnter the ID of the user you want to display details of :"))
            try:
                objlis[idi].display()
            except KeyError:
                print "\nSorry no user under the given ID has been registered in this system.\n"

        if ch1==3:
            idi =int(raw_input("\nEnter the ID of the user you the quote to be changed: "))
            quote = raw_input("Enter the new quote: ")
            try:
                objlis[idi].quote = quote
                print "Quote has been changed successfully! Remember to register this object to database to make sure quote is changed on it as well.\n"
            except KeyError:
                print "The given ID is invalid!"

        if ch1==4 and onstatus ==True:
            idi =int(raw_input("\nEnter the ID of the user you want to register on database: "))
            try:
                objlis[idi].register()
            except KeyError:
                print "The given ID is invalid!"
        if ch1==4 and onstatus ==False:
                print "\nRestart the program and make sure your online on the database\n"

        if ch1==5 and onstatus ==True:
            idi =int(raw_input("\nEnter the ID of the user you want to find details from database: "))
            try:
                data = objlis[idi].ondisplay()
                pinter2(data)
            except KeyError:
                print "The given ID is invalid!"
            except IndexError:
                print "\nSomething went wrong , make sure this object has been registred in database.\n"

        if ch1==5 and onstatus ==False:
                print "\nRestart the program and make sure your online on the database\n"

        if ch1==6:
            idi = int(raw_input("Enter user id to be delted : "))
            try:
                try:
                    objlis[idi].deldbob()
                except:
                    pass
                del objlis[idi]
                print "Deletion Done\n"
            except:
                print "Nothing to be deleted: "
                
        if ch1==7: #Before exiting we make sure we dump all objects in objectlist.
            pic = open('pick.dat','wb')
            pickle.dump(objlis,pic)
            pic.close()
            cred = raw_input("\n\n\nThank you for using Quotes Manager \nMade By Sam Thomas XII A")
            break

    
    except ValueError:
        print "Invalid input of data type , please make sure you input right type of data."

    
    
