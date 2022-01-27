import mysql.connector
from tkinter import *
from tkinter import messagebox
from subprocess import call
 
def Ok():
    # mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="studentmanagement")
    # mycursor = mysqldb.cursor()
    uname = e1.get()
    password = e2.get()
 
    # sql = "select * from user where uname = %s and password = %s"
    # mycursor.execute(sql, [(uname), (password)])
    # results = mycursor.fetchall()
 
    if (uname=="" and password=="123"):
        messagebox.showinfo("","Blank not allowed")

    elif(uname=="Admin" and password=="123"):
        messagebox.showinfo("","Login Success")

    else :
        messagebox.showinfo("","Incorrent Username and Password")
        return False
 
 
 
root = Tk()
root.title("Login")
root.geometry("300x200")
global e1
global e2
 
Label(root, text="Login",font=("Arial", 15, "bold"), bg="#00376b", fg="#FFFCF9").place(x=10, y=10)
Label(root, text="UserName").place(x=10, y=60)
Label(root, text="Password").place(x=10, y=80)
 
e1 = Entry(root)
e1.place(x=140, y=60)
 
e2 = Entry(root)
e2.place(x=140, y=80)
e2.config(show="*")
 
Button(root, text="Login", command=Ok ,height = 2, width = 13).place(x=150, y=120)
 
root.mainloop()