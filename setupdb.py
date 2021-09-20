import mysql.connector
mydb = mysql.connector.connect(
    host="db", port="3306", user="root", passwd="password")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE AlphaQMoM")  # Creating database
mydb.commit()
mydb = mysql.connector.connect(
    host="db", port="3306", user="root", passwd="password", database="AlphaQMoM")
mycursor = mydb.cursor()
# Creating table for users
mycursor.execute(
    "CREATE TABLE allUsers (user TEXT NOT NULL,password LONGTEXT)")
for i in range(1, 31):
    if len(str(i)) == 1:
        command = "INSERT INTO allUsers (user, password) VALUES (%s, %s)"
        uname = "webDev_0"+str(i)
        val = (uname, "superuserpass")
        mycursor.execute(command, val)
        command1 = "INSERT INTO allUsers (user, password) VALUES (%s, %s)"
        uname = "appDev_0"+str(i)
        val1 = (uname, "superuserpass")
        mycursor.execute(command1, val1)
        command2 = "INSERT INTO allUsers (user, password) VALUES (%s, %s)"
        uname = "sysAd_0"+str(i)
        val2 = (uname, "superuserpass")
        mycursor.execute(command2, val2)
    else:
        command = "INSERT INTO allUsers (user, password) VALUES (%s, %s)"
        uname = "webDev_"+str(i)
        val = (uname, "superuserpass")
        mycursor.execute(command, val)
        command1 = "INSERT INTO allUsers (user, password) VALUES (%s, %s)"
        uname = "appDev_"+str(i)
        val1 = (uname, "superuserpass")
        mycursor.execute(command1, val1)
        command2 = "INSERT INTO allUsers (user, password) VALUES (%s, %s)"
        uname = "sysAd_"+str(i)
        val2 = (uname, "superuserpass")
        mycursor.execute(command2, val2)
mydb.commit()
print("Database updated successfully.")