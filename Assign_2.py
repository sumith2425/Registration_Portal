import re
import json
import tkinter as tk
from tkinter import *
from tkinter import messagebox


class Person:
    def __init__(self,user_id,password,name):
        self.user_id =user_id
        self.password=password
        self.name = name
        
class Student(Person):
    def __init__(self, user_id, password,name):
        super().__init__(user_id, password,name)
        
class Teacher(Person):
    def __init__(self, user_id, password,name,role,designation):
        super().__init__(user_id, password,name)
        self.role = role
        self.designation = designation
        
class UG_Student(Student):
    def __init__(self, user_id, password,name,role,year_of_graduation):
        super().__init__(user_id, password,name)
        self.role = role
        self.year_of_graduation =year_of_graduation

class PG_Student(Student):
    def __init__(self, user_id, password,name,role,specialization):
        super().__init__(user_id, password,name)
        self.role = role
        self.specialization=specialization
        
class Academic_Unit:
    def __init__(self):
        self.records = []
        self.load_data()

    def add_member(self, member):
        self.records.append(member)
        self.save_data()

    def find_member_by_id(self, user_id):
        for member in self.records:
            if member.user_id == user_id:
                return member
        return None

    def remove_member(self, id):
        member = self.find_member_by_id(id)
        if member:
            self.records.remove(member)
            self.save_data()
    
    # saves the list into the json file
    def save_data(self):
        with open("members_data.json", "w") as file:
            data = [{"user_id": member.user_id, "password": member.password, "name": member.name,
                     "role": getattr(member, "role", None), "designation": getattr(member, "designation", None),
                     "year_of_graduation": getattr(member, "year_of_graduation", None),
                     "specialization": getattr(member, "specialization", None)} for member in self.records]
            json.dump(data, file)

    def load_data(self):
        try:
            with open("members_data.json", "r") as file:
                data = json.load(file)
                for entry in data:
                    role = entry["role"]
                    if role == "UG Student":
                        member = UG_Student(entry["user_id"], entry["password"], entry["name"], role, entry["year_of_graduation"])
                    elif role == "PG Student":
                        member = PG_Student(entry["user_id"], entry["password"], entry["name"], role, entry["specialization"])
                    elif role == "Teacher":
                        member = Teacher(entry["user_id"], entry["password"], entry["name"], role, entry["designation"])
                    else:
                        member = Person(entry["user_id"], entry["password"], entry["name"])
                    self.records.append(member)
        except FileNotFoundError:
            pass
        
    def sign_up(self):
        self.suproot = tk.Tk()
        self.suproot.config(bg="orange")
        self.suproot.geometry("650x500")
        self.suproot.title("Academic Unit")
        supframe = tk.Frame(self.suproot)
        supframe.place(relx=0.5,rely=0.5,anchor="center")
        supframe.config(height=370,width=450)
        Label(supframe,text = "SIGN UP",font=("Times",20,"bold"),fg="blue").place(relx = 0.39,rely = 0.05) 
        self.user_id = Label(supframe,text = "User ID",font=("calibre")).place(x = 40,y = 80)  
        self.password = Label(supframe,text = "Password",font=("calibre")).place(x = 40,y = 130)  
        self.Sup_userid_entry = tk.Entry(supframe,font=('calibre'),width=25)
        self.Sup_userid_entry.place(x= 140,y=80)
        self.Sup_password_entry = tk.Entry(supframe, font=('calibre'),width=25,show="*")
        self.Sup_password_entry.place(x= 140,y=130)
        button = Button(supframe,text = "Sign Up",font=("calibre"),command=self.get_role).place(relx = 0.423,rely = 0.7)
        self.suproot.mainloop()
        
            
    def sign_in(self):
        self.sinroot = tk.Tk()
        self.sinroot.config(bg="orange")
        self.sinroot.geometry("650x500")
        self.sinroot.title("Academic Unit")
        sinframe = tk.Frame(self.sinroot)
        sinframe.place(relx=0.5,rely=0.5,anchor="center")
        sinframe.config(height=370,width=450)
        Label(sinframe,text = "SIGN IN",font=("Times",20,"bold")).place(relx = 0.39,rely = 0.05) 
        self.user_id = Label(sinframe,text = "User ID",font=("calibre",)).place(x = 40,y = 80)  
        self.password = Label(sinframe,text = "Password",font=("calibre")).place(x = 40,y = 130)  
        self.Sin_userid_entry = tk.Entry(sinframe, font=('calibre'),width=25)
        self.Sin_userid_entry.place(x= 140,y=80)
        self.Sin_password_entry = tk.Entry(sinframe, font=('calibre'),width=25,show="*")
        self.Sin_password_entry.place(x= 140,y=130)
        self.count =1
        button1 = Button(sinframe,text = "Sign In",font=("calibre"),command=academic_unit.sign_in_button_clicked).place(relx = 0.423,rely = 0.5)
        Label(sinframe,text = "Don't have an Account?",font=("calibre",15)).place(x=125,y=255)
        button2 = Button(sinframe,text = "Sign Up",font=("calibre"),fg="red",command=academic_unit.sign_up).place(relx = 0.415,rely = 0.8)
        
        self.sinroot.mainloop()
        
    def sign_in_button_clicked(self):
        id = self.Sin_userid_entry.get()
        passw = self.Sin_password_entry.get()
        
        user = academic_unit.find_member_by_id(id)
        
        if user is not None:
            # Authenticate the user
            if passw==user.password:
                messagebox.showinfo("Success", "Sign in successful!")
                academic_unit.edit_your_info(user)
            else:
                if self.count==3:
                    messagebox.showerror("Error","Account Deactivated\n\nYou've entered incorrect credentials three times")
                    academic_unit.remove_member(id)
                    self.count=1
                else:
                    messagebox.showerror("Error", f"Incorrect credentials. {3-self.count} {'attempts' if 3-self.count > 1 else 'attempt'} remaining. Account will be deactivated after three unsuccessful attempts.")
                    self.count+=1
        else:
            messagebox.showerror("Error", "User not found. Please register first.")

        
    def sign_up_user(self,get_role,variable,name):
        id = self.Sup_userid_entry.get()
        passw = self.Sup_password_entry.get()
        if get_role.lower() =="ug student":
            user = UG_Student(id,passw,name,"UG Student",variable)
            academic_unit.add_member(user)
            self.get_year_of_graduation.destroy()
            self.get_role_root.destroy()
            messagebox.showinfo("Success","You are Successfully Signed Up.")
            self.suproot.destroy()
        elif get_role.lower() == "pg student":
            user = PG_Student(id,passw,name,"PG Student",variable)
            academic_unit.add_member(user)
            self.get_specialization.destroy()
            self.get_role_root.destroy()
            messagebox.showinfo("Success","You are Successfully Signed Up.")
            self.suproot.destroy()
        elif get_role.lower() == "teacher":
            user = Teacher(id,passw,name,"Teacher",variable)
            academic_unit.add_member(user)
            self.get_designation.destroy()
            self.get_role_root.destroy()
            messagebox.showinfo("Success","You are Successfully Signed Up.")
            self.suproot.destroy()
            
    def get_role(self):
        id = self.Sup_userid_entry.get()
        passw = self.Sup_password_entry.get()
        member = academic_unit.find_member_by_id(id)
        if member in academic_unit.records:
            messagebox.showerror("Error","User id already present.Please Sign in")
            self.suproot.destroy()
            return
            
        if not self.validate_user_input(id,passw):
            return
        self.get_role_root = tk.Tk()
        self.get_role_root.geometry("650x500")
        self.get_role_root.title("Role")
        get_role_frame = tk.Frame(self.get_role_root)
        get_role_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_role_frame.config(height=370,width=450)
        name = Label(get_role_frame,text= "Name",font=("calibre",15))
        name.grid(row = 0, column = 0, sticky = N, pady = 20)
        name_entry = tk.Entry(get_role_frame,font=('calibre'),width=25)
        name_entry.grid(row = 0, column = 1, sticky = N, pady = 20)
        Label(get_role_frame,text= "Select your role:",font=("calibre",15)).grid(row = 2, column = 0, sticky = N, pady = 10)
        ug_button = Button(get_role_frame,text = "UG Student",font=("calibre"),command=lambda: self.ask_year_of_graduation(name_entry.get())).grid(row = 3, column = 1, sticky = W, pady = 5)
        pg_button = Button(get_role_frame,text = "PG Student",font=("calibre"),command=lambda: self.ask_specialization(name_entry.get())).grid(row = 4, column = 1, sticky = W, pady = 5)
        teacher_button = Button(get_role_frame,text = "Teacher",font=("calibre"),command=lambda: self.ask_designation(name_entry.get())).grid(row = 5, column = 1, sticky = W, pady = 5)
        
        self.get_role_root.mainloop()
            
    def ask_year_of_graduation(self,name1):
        self.get_year_of_graduation = tk.Tk()
        self.get_year_of_graduation.geometry("650x500")
        self.get_year_of_graduation.title("Year of Graduation")
        get_year_frame = tk.Frame(self.get_year_of_graduation)
        get_year_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_year_frame.config(height=370,width=450)
        year = Label(get_year_frame,text= "Enter the Year of Graduation",font=("calibre",15))
        year.pack()
        year_entry = tk.Entry(get_year_frame,font=('calibre'),width=25)
        year_entry.pack()
        
        pg_button = Button(get_year_frame,text = "Submit",font=("calibre"),command=lambda: self.sign_up_user("UG Student",year_entry.get(),name1)).pack()
        self.get_year_of_graduation.mainloop()
    
    def ask_specialization(self,name1):
        self.get_specialization = tk.Tk()
        self.get_specialization.geometry("650x500")
        self.get_specialization.title("Specialization")
        get_specialization_frame = tk.Frame(self.get_specialization)
        get_specialization_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_specialization_frame.config(height=370,width=450)
        specialization = Label(get_specialization_frame,text= "Select your Specialization",font=("calibre",15))
        specialization.pack(pady=20)
        pg_button = Button(get_specialization_frame,text = "M.Sc",font=("calibre"),command=lambda: self.sign_up_user("PG Student","M.Sc",name1)).pack()
        pg_button = Button(get_specialization_frame,text = "MBA",font=("calibre"),command=lambda: self.sign_up_user("PG Student","MBA",name1)).pack()
        pg_button = Button(get_specialization_frame,text = "Ph.D",font=("calibre"),command=lambda: self.sign_up_user("PG Student","Ph.D",name1)).pack()
        self.get_specialization.mainloop()
    
    def ask_designation(self,name1):
        self.get_designation = tk.Tk()
        self.get_designation.geometry("650x500")
        self.get_designation.title("Designation")
        get_designation_frame = tk.Frame(self.get_designation)
        get_designation_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_designation_frame.config(height=370,width=450)
        designaion = Label(get_designation_frame,text= "Select your Specialization",font=("calibre",15))
        designaion.pack(pady=20)
        pg_button = Button(get_designation_frame,text = "Professor",font=("calibre"),command=lambda: self.sign_up_user("Teacher","Professor",name1)).pack()
        pg_button = Button(get_designation_frame,text = "Assistant Professor",font=("calibre"),command=lambda: self.sign_up_user("Teacher","Assistant Professor",name1)).pack()
        self.get_designation.mainloop()
    
    def edit_your_info(self,member):
        self.edit_root = tk.Tk()
        self.edit_root.geometry("850x800")
        self.edit_root.config(bg="blue")
        self.edit_root.title("Edit your Info")
        edit_frame = tk.Frame(self.edit_root)
        edit_frame.place(relx=0.5,rely=0.5,anchor="center")
        edit_frame.config(height=670,width=650)
        Label(edit_frame,text= f"Welcome ",font=("calibre",22)).place(relx=0.4,rely =0.05)
        Label(edit_frame,text= f"Name     : {member.name} ",font=("calibre",18)).place(x=40,y=100)
        userid_button = Button(edit_frame,text = "Edit",font=("calibre"),command=lambda: self.Change_name(self.edit_root,member)).place(x=440,y=100)
        Label(edit_frame,text= f"User-ID  : {member.user_id} ",font=("calibre",18)).place(x=40,y=140)
        userid_button = Button(edit_frame,text = "Edit",font=("calibre"),command=lambda: self.Change_user_id(self.edit_root,member)).place(x=440,y=140)
        Label(edit_frame,text= "Password : ********** ",font=("calibre",18)).place(x=40,y=180)
        password_button = Button(edit_frame,text = "Edit",font=("calibre"),command=lambda: self.Change_password(self.edit_root,member)).place(x=440,y=180)
        Label(edit_frame,text= f"Role     : {member.role} ",font=("calibre",18)).place(x=40,y=230)
        role_button = Button(edit_frame,text = "Edit",font=("calibre"),command=lambda: self.Change_role(self.edit_root,member)).place(x=440,y=230)
        if member.role == "UG Student":
            Label(edit_frame,text= f"Year of Graduation: {member.year_of_graduation} ",font=("calibre",18)).place(x=40,y=280)
            Button(edit_frame,text = "Edit",font=("calibre"),command=lambda: self.edit_year_of_graduation(self.edit_root,member)).place(x=440,y=280)
        elif member.role == "PG Student":
            Label(edit_frame,text= f"Specialization: {member.specialization} ",font=("calibre",18)).place(x=40,y=280)
            Button(edit_frame,text = "Edit",font=("calibre"),command=lambda: self.edit_specialization(self.edit_root,member)).place(x=440,y=280)
        elif member.role == "Teacher":
            Label(edit_frame,text= f"Designation: {member.designation} ",font=("calibre",18)).place(x=40,y=280)
            Button(edit_frame,text = "Edit",font=("calibre"),command=lambda: self.edit_designation(self.edit_root,member)).place(x=440,y=280)
        deregistration_button = Button(edit_frame,text = "Deregister",font=("calibre"),command=lambda: self.Deregister(self.edit_root,member)).place(x=240,y=320)
        
        self.edit_root.mainloop()
        
    def check_name(self,member,new_name):
        
        member.name = new_name
        messagebox.showinfo("Success",'Name succesfully changed.')
        self.edit_name.destroy()
        self.edit_root.destroy()
        self.save_data()
        academic_unit.edit_your_info(member)
        
    def Change_name(self,ed_root,member):
        self.edit_name = tk.Tk()
        self.edit_name.geometry("650x500")
        self.edit_name.title("Change your Name")
        edit_name_frame = tk.Frame(self.edit_name)
        edit_name_frame.place(relx=0.5,rely=0.5,anchor="center")
        edit_name_frame.config(height=370,width=450)
        Label(edit_name_frame,text = "Enter the new Name: ",font=("calibre",15)).pack()
        self.edit_name_entry = tk.Entry(edit_name_frame,font=('calibre'),width=25)
        self.edit_name_entry.pack()
        Button(edit_name_frame,text = "Change",font=("calibre"),command=lambda: self.check_name(member,self.edit_name_entry.get())).pack()
        self.edit_name.mainloop()
        
    def check_user_id(self,member,new_id):
        if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$", new_id):
            messagebox.showerror("Error", "Invalid email address.Please try again")
        else:
            member.user_id = new_id
            messagebox.showinfo("Success",'User ID succesfully changed.')
            self.edit_user_id_entry.destroy()
            self.edit_user_id.destroy()
            self.edit_root.destroy()
            self.save_data()
            academic_unit.edit_your_info(member)
        
    def Change_user_id(self,ed_root,member):
        self.edit_user_id = tk.Tk()
        self.edit_user_id.geometry("650x500")
        self.edit_user_id.title("Change your UserId")
        edit_user_id_frame = tk.Frame(self.edit_user_id)
        edit_user_id_frame.place(relx=0.5,rely=0.5,anchor="center")
        edit_user_id_frame.config(height=370,width=450)
        Label(edit_user_id_frame,text = "Enter the new User Id: ",font=("calibre",15)).pack()
        self.edit_user_id_entry = tk.Entry(edit_user_id_frame,font=('calibre'),width=25)
        self.edit_user_id_entry.pack()
        Button(edit_user_id_frame,text = "Change",font=("calibre"),command=lambda: self.check_user_id(member,self.edit_user_id_entry.get())).pack()
        self.edit_user_id.mainloop()
    
    def check_password(self,member,new_password):
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*])[A-Za-z\d!@#$%&*]{8,12}$", new_password):
            messagebox.showerror("Error", "Invalid New Password.Please try again. Password length should be 8-12 character long and should contain  at least one upper case, one digit, one lower case and a special character")
        else:
            member.password = new_password
            messagebox.showinfo("Success",'Password succesfully changed.')
            
            self.edit_password_entry.destroy()
            self.edit_password.destroy()
            self.edit_root.destroy()
            self.save_data()
            academic_unit.edit_your_info(member)
            
    def Change_password(self,ed_root,member):
        self.edit_password = tk.Tk()
        self.edit_password.geometry("650x500")
        self.edit_password.title("Change Password")
        edit_password_frame = tk.Frame(self.edit_password)
        edit_password_frame.place(relx=0.5,rely=0.5,anchor="center")
        edit_password_frame.config(height=370,width=450)
        Label(edit_password_frame,text = "Enter the new Password: ",font=("calibre",15)).pack()
        self.edit_password_entry = tk.Entry(edit_password_frame,font=('calibre'),width=25,show="*")
        self.edit_password_entry.pack()
        Button(edit_password_frame,text = "Change",font=("calibre"),command=lambda: self.check_password(member,self.edit_password_entry.get())).pack()
        
        self.edit_password.mainloop()
        
    def check_role_ug(self,member):
        self.get_year_of_graduation = tk.Tk()
        self.get_year_of_graduation.geometry("650x500")
        self.get_year_of_graduation.title("Year of Graduation")
        get_year_frame = tk.Frame(self.get_year_of_graduation)
        get_year_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_year_frame.config(height=370,width=450)
        year = Label(get_year_frame,text= "Enter the Year of Graduation",font=("calibre",15))
        year.pack()
        year_entry = tk.Entry(get_year_frame,font=('calibre'),width=25)
        year_entry.pack()
        Button(get_year_frame,text = "Submit",font=("calibre"),command=lambda: self.change(member,"UG Student",year_entry.get())).pack()
        self.get_year_of_graduation.mainloop()
        
    def check_role_pg(self,member):
        self.get_specialization = tk.Tk()
        self.get_specialization.geometry("650x500")
        self.get_specialization.title("Specialization")
        get_specialization_frame = tk.Frame(self.get_specialization)
        get_specialization_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_specialization_frame.config(height=370,width=450)
        specialization = Label(get_specialization_frame,text= "Select your Specialization",font=("calibre",15))
        specialization.pack(pady=20)
        pg_button = Button(get_specialization_frame,text = "M.Sc",font=("calibre"),command=lambda: self.change(member,"PG Student","M.Sc")).pack()
        pg_button = Button(get_specialization_frame,text = "MBA",font=("calibre"),command=lambda: self.change(member,"PG Student","MBA")).pack()
        pg_button = Button(get_specialization_frame,text = "Ph.D",font=("calibre"),command=lambda: self.change(member,"PG Student","Ph.D")).pack()
        self.get_specialization.mainloop()
        
    def check_role_teacher(self,member):
        self.get_designation = tk.Tk()
        self.get_designation.geometry("650x500")
        self.get_designation.title("Designation")
        get_designation_frame = tk.Frame(self.get_designation)
        get_designation_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_designation_frame.config(height=370,width=450)
        designaion = Label(get_designation_frame,text= "Select your Designation",font=("calibre",15))
        designaion.pack(pady=20)
        pg_button = Button(get_designation_frame,text = "Professor",font=("calibre"),command=lambda: self.change(member,"Teacher","Professor")).pack()
        pg_button = Button(get_designation_frame,text = "Assistant Professor",font=("calibre"),command=lambda: self.change(member,"Teacher","Assistant Professor")).pack()
        self.get_designation.mainloop()
        
    def change(self,member,role,var):
        if(role == "UG Student"):
            member1 = UG_Student(member.user_id,member.password,member.name,role,var)
            academic_unit.records.remove(member)
            academic_unit.add_member(member1)
            messagebox.showinfo("Success",'Role succesfully changed.')
            self.get_year_of_graduation.destroy()
            self.edit_role.destroy()
            self.edit_root.destroy()
            self.save_data()
            academic_unit.edit_your_info(member1)
        elif(role == "PG Student"):
            member1 = PG_Student(member.user_id,member.password,member.name,role,var)
            academic_unit.records.remove(member)
            academic_unit.add_member(member1)
            messagebox.showinfo("Success",'Role succesfully changed.')
            self.get_specialization.destroy()
            self.edit_role.destroy()
            self.edit_root.destroy()
            self.save_data()
            academic_unit.edit_your_info(member1)
        elif(role == "Teacher"):
            member1 = Teacher(member.user_id,member.password,member.name,role,var)
            academic_unit.records.remove(member)
            academic_unit.add_member(member1)
            messagebox.showinfo("Success",'Role succesfully changed.')
            self.get_designation.destroy()
            self.edit_role.destroy()
            self.edit_root.destroy()
            self.save_data()
            academic_unit.edit_your_info(member1)
            
    
    def Change_role(self,ed_root,member):
        self.edit_role = tk.Tk()
        self.edit_role.geometry("650x500")
        self.edit_role.title("Change Role")
        edit_role_frame = tk.Frame(self.edit_role)
        edit_role_frame.place(relx=0.5,rely=0.5,anchor="center")
        edit_role_frame.config(height=370,width=450)
        Label(edit_role_frame,text = "Select the New Role: ",font=("calibre",15)).pack()
        ug_button = Button(edit_role_frame,text = "UG Student",font=("calibre"),command=lambda: self.check_role_ug(member)).pack()
        pg_button = Button(edit_role_frame,text = "PG Student",font=("calibre"),command=lambda: self.check_role_pg(member)).pack()
        teacher_button = Button(edit_role_frame,text = "Teacher",font=("calibre"),command=lambda: self.check_role_teacher(member)).pack()
        
        self.edit_role.mainloop()
        
    def edit_year_of_graduation(self,ed_root,member):
        self.get_year_of_graduation = tk.Tk()
        self.get_year_of_graduation.geometry("650x500")
        self.get_year_of_graduation.title("Edit Year of Graduation")
        get_year_frame = tk.Frame(self.get_year_of_graduation)
        get_year_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_year_frame.config(height=370,width=450)
        new_year = Label(get_year_frame,text= "Enter the Year of Graduation",font=("calibre",15))
        new_year.pack()
        new_year_entry = tk.Entry(get_year_frame,font=('calibre'),width=25)
        new_year_entry.pack()
        
        Button(get_year_frame,text = "Submit",font=("calibre"),command=lambda: self.change_year(member,new_year_entry.get)).pack()
    
    def change_year(self,member,new_year):
        member.year_of_graduation = new_year
        self.get_year_of_graduation.destroy()
        self.edit_root.destroy()
        self.save_data()
        academic_unit.edit_your_info(member)
        
    def edit_specialization(self,ed_root,member):
        self.edit_specialization_root = tk.Tk()
        self.edit_specialization_root.geometry("650x500")
        self.edit_specialization_root.title("Edit Specialization")
        edit_specialization_frame = tk.Frame(self.edit_specialization_root)
        edit_specialization_frame.place(relx=0.5,rely=0.5,anchor="center")
        edit_specialization_frame.config(height=370,width=450)
        specialization = Label(edit_specialization_frame,text= "Select your Specialization",font=("calibre",15))
        specialization.pack(pady=20)
        pg_button = Button(edit_specialization_frame,text = "M.Sc",font=("calibre"),command=lambda: self.change_specialization("M.Sc",member)).pack()
        pg_button = Button(edit_specialization_frame,text = "MBA",font=("calibre"),command=lambda: self.change_specialization("MBA",member)).pack()
        pg_button = Button(edit_specialization_frame,text = "Ph.D",font=("calibre"),command=lambda: self.change_specialization("Ph.D",member)).pack()
    
    def change_specialization(self,spec,member):
        member.specialization = spec
        self.edit_specialization_root.destroy()
        self.edit_root.destroy()
        self.save_data()
        academic_unit.edit_your_info(member)
        
    def edit_designation(self,ed_root,member):
        self.edit_designation_root = tk.Tk()
        self.edit_designation_root.geometry("650x500")
        self.edit_designation_root.title("Designation")
        get_designation_frame = tk.Frame(self.edit_designation_root)
        get_designation_frame.place(relx=0.5,rely=0.5,anchor="center")
        get_designation_frame.config(height=370,width=450)
        designaion = Label(get_designation_frame,text= "Select your Specialization",font=("calibre",15))
        designaion.pack(pady=20)
        Button(get_designation_frame,text = "Professor",font=("calibre"),command=lambda: self.change_designation(member,"Professor")).pack()
        Button(get_designation_frame,text = "Assistant Professor",font=("calibre"),command=lambda: self.change_designation(member,"Assistant Professor")).pack()
    
    def change_designation(self,member,desig):
        member.designation = desig
        self.get_designation.destroy()
        self.edit_root.destroy()
        self.save_data()
        academic_unit.edit_your_info(member)
        
    def Deregister(self,ed_root,member):
        answer = messagebox.askyesno("Confirmation","Are you sure that you want to Deregister?")
        if answer:
            academic_unit.records.remove(member)
            self.edit_root.destroy()
            self.save_data()
            messagebox.showinfo("Success","Successfully Deregisterd.")
        
    def validate_user_input(self, user_id, password):
        # Add validation rules as needed
        if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$", user_id):
            messagebox.showerror("Error", "Invalid email address.Please try again.\n User-ID should be in the format of email address.")
            return False

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*])[A-Za-z\d!@#$%&*]{8,12}$", password):
            messagebox.showerror("Error", "Invalid password format.Please try again.Password length should be 8-12 character long and should contain  at least one upper case, one digit, one lower case and a special character")
            return False

        return True

        
if __name__ =="__main__":
    academic_unit = Academic_Unit()
    academic_unit.sign_in()