import dbcreds
import mariadb

conn = mariadb.connect(user=dbcreds.user,
                    password=dbcreds.password,
                    host=dbcreds.host,
                    port=dbcreds.port,
                    database=dbcreds.database
                    )
cursor = conn.cursor()

try:
    def sign_up():
        print("******* Sign up *******")
        alias = input("Enter alias: ")
        password = input("Enter password: ")
        cursor.execute("INSERT INTO hackers(alias, password) VALUES(?,?)", [alias, password])
        conn.commit()

    def log_in():
        print("******* Log in *******")
        alias = input("Enter alias: ")
        password = input("Enter password: ")
        cursor.execute("SELECT * FROM hackers WHERE alias=? and password=?",[alias, password])
        info = cursor.fetchone()
        
        if info != None:
            print("Select from the options below:\n\n1. Enter a new exploit\n2. See all exploits\n3. See other exploit\n4. Exit application")
            option = int(input("Enter selection:"))
            if option == 1:
                exploit = input("Enter new exploits:\n")
                cursor.execute("INSERT INTO exploits(content, user_id) VALUES (?,(SELECT id FROM hackers WHERE alias=?));", [exploit, alias])
                conn.commit()
            if option == 2:
                print("Exploit list:\n")
                cursor.execute("SELECT content FROM exploits")
                result = cursor.fetchall()
                for list in result:
                    print(list)
            if option == 3:
                print("Others exploit list:")
                cursor.execute("SELECT content FROM exploits INNER JOIN hackers ON exploits.user_id=hackers.id WHERE alias!=?",[alias])
                result = cursor.fetchall()
                for list in result:
                    print(list)
            if option == 4:
                print("Exiting")

        else:
            print("Data Does Not Exist")



    print("******* WELCOME *******\n1. Sign up\n2. Log in\n")
    selection = int(input("Select option:"))
    if selection == 1:
        sign_up()
    if selection == 2:
        log_in()
    else:
        print("Invalid entry")
except mariadb.DataError:
    print("Something wrong with your data")
except mariadb.OperationalError:
    print("Something wrong with the connection")
except mariadb.ProgrammingError:
    print("Your query was wrong")
except mariadb.IntegrityError:
    print("Your query would have broken the database and we stopped it")
finally:
    if (cursor != None):
        cursor.close()
    else:
        print("There was never a cursor to begin with")
    if (conn != None):
        conn.rollback()
        conn.close()
    else:
        print("The connection never opened, nothing to close here")