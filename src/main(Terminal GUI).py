###########################################################################################################
#                                                                                                         #
#                                           LLIBRERIES                                                    #
#                                                                                                         #
###########################################################################################################

import mysql.connector

## Llibreries pròpies ##
import Login
import MenusJoc
2
mydb = mysql.connector.connect(
host="192.168.3.10",
user="terict",          
# password='terict',    #SENSE PASSWORD
database='tericttest' 
)

mycursor = mydb.cursor()

while(True):

   Answer, Nick, Admin = Login.login(mycursor, mydb)

   if Answer:
      MenusJoc.menuPrincipal(Nick, mycursor, mydb, Admin)
   else:
      break

print()
print("######################################################################################")
print("#                                                                                   #")
print(" #                                  Fins aviat !                                   #")
print("#                                                                                   #")
print("######################################################################################")
print()