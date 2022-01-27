from tkinter import *
root = Tk()
root.geometry("500x300")

def getvals():
    print(" Accepted ")

#Heading
Label(root, text='Pythyon Registration form', font="arial 15 bold").grid(row=0, column=3)

#Feild Name
name = Label(root, text="Name")
phone = Label(root, text="Phone")
gender = Label(root, text="Gender")
emergency = Label(root, text="Emergency")
paymentmode = Label(root, text="Payment Mode")

#Packing Feilds
name.grid(row=1, column=2)
phone.grid(row=2, column=2)
gender.grid(row=3, column=2)
emergency.grid(row=4, column=2)
paymentmode.grid(row=5, column=2)

# Variable For Storing Data
namevalue = StringVar
phonevalue = StringVar
gendervalue = StringVar
emergencyvalue = StringVar
paymentmodevalue = StringVar
checkvalue = IntVar

#Entry Feild
nameentry = Entry(root, textvariable=namevalue)
phoneentry = Entry(root, textvariable=phonevalue)
genderentry = Entry(root, textvariable=gendervalue)
emergencyentry = Entry(root, textvariable=emergencyvalue)
paymentmodeentry = Entry(root, textvariable=paymentmodevalue)

#Packing Entry Feilds
nameentry.grid(row=1, column=3)
phoneentry.grid(row=2, column=3)
genderentry.grid(row=3, column=3)
emergencyentry.grid(row=4, column=3)
paymentmodeentry.grid(row=5, column=3)

#CreatingCheck Box
checkbtn = Checkbutton(text=" Remember Me ? ", font="arial 10 italic", variable=checkvalue)
checkbtn.grid(row=6 ,column= 3)

#submit
Button(text=" Submit ", command=getvals).grid(row=7, column=3)
root.mainloop()