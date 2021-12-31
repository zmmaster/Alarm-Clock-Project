from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3 
from sqlite3 import Error

# This class handles the Graphical User Interface for the alarm clock
class AlarmClockGUI:
    
    def __init__(self,root):
        
        #This block creates the main window
        root.title("Alarm Clock")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # This block is to instantiate a Listbox 
        self.alarmNames = ["Apple"]
        self.alarms = StringVar(value=self.alarmNames)
        self.lbox = Listbox(mainframe, listvariable=self.alarms)
        self.lbox.grid(column=1, row=1,columnspan=3, rowspan= 1, sticky=(NW,NE))

        

        # These blocks instantiate the desired value to create an alarm
        self.time = StringVar()
        time_entry = ttk.Entry(mainframe, width=40, textvariable=self.time) 
        time_entry.grid(column=1, row=3, sticky=E)

        self.date = StringVar()
        date_entry = ttk.Entry(mainframe, width=40, textvariable=self.date)
        date_entry.grid(column=1, row=4, sticky=E)
        
        # This instantiates any needed Buttons
        ttk.Button(mainframe, text="Add Alarm", command=self.addAlarm).grid(column=4, row=5, stick=SW)
        ttk.Button(mainframe, text="Edit Alarm", command=self.editAlarmGUI).grid(column=4, row=1, sticky=(NE))
        ttk.Button(mainframe, text="Delete Alarm", command=self.deleteAlarm).grid(column=4,row=2, sticky=N)
        
        self.ampm = StringVar()
        ttk.Radiobutton(mainframe, text="A.M.", variable=self.ampm, value='A.M.').grid(column=3, row=3,stick=(W,E))
        ttk.Radiobutton(mainframe, text="P.M.", variable=self.ampm, value='P.M.').grid(column=4, row=3,stick=(W,E))

        # Thes blocks create the necessary labels
        ttk.Label(mainframe, text='Please add an alarm by filling out the information below').grid(column=1,row=2, sticky=(W,E))
        ttk.Label(mainframe, text='Time: ').grid(column=1, row=3, sticky=(W))
        ttk.Label(mainframe, text='Date: ').grid(column=1, row=4, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)


        # This puts the cursor in the time entry when the window is opened
        time_entry.focus()

    def addAlarm(self,*args):
        """ This method retrieves the data from the GUI and instantiates an Alarm object """

        # This block gets the data from the GUI
        time = self.time.get()
        date = self.date.get()
        ampm = self.ampm.get()
         
        # This creates a new class instance of Alarm
        newAlarm = Alarm(time,date,ampm)

        print(newAlarm) 

        # This ensures the new alarm will be updated to the listbox
        self.alarmNames.append(newAlarm) 
        self.alarms.set(self.alarmNames)
        
         
    

    def deleteAlarm(self, *args):
        """  This deletes the selected alarm or returns an error message if none are selected """

        idxs = self.lbox.curselection() # This retrieves the index of the listbox 
        if len(idxs)==1: # The length will only ever be one if something is selected in the listbox 
            idx = int(idxs[0])

            self.alarmNames.pop(idx)    
            self.alarms.set(self.alarmNames)
            self.alarms.set(list(filter(None,self.alarmNames))) # The list filter is to get rid of a None type that was being returned that was undesirable    
        else: 
            # If nothing is selected, present an error message
            messagebox.showinfo(message='Please select an alarm')

    
    def editAlarm(self, *args):
        """This method identifies an alarm selected in the listbox and edits it"""

        idxs = self.lbox.curselection()
        idx = int(idxs[0])
        
        self.alarmNames.append(self.addAlarm()) # Appends new alarm by calling addAlarm()  method
        self.deleteAlarm() # Deletes currently selected alarm using deleteAlarm()  method
        self.alarms.set(list(filter(None,self.alarmNames))) # The list filter is to get rid of a None type that was being returned that was undesirable

    
    def editAlarmGUI(self,*args):
        """ This method creates a new window to edit the alarm in"""

        idxs = self.lbox.curselection() # This retrieves the index of the listbox 
        if len(idxs)==1: # The length will only ever be one if something is selected in the listbox 

            # This block creates a new window when edit is pressed
            editbox = Toplevel(root)
            editboxFrame = ttk.Frame(editbox, padding="3 3 12 12")
            editboxFrame.grid(column=0, row=0, sticky=(N,W,E,S))
            
            
            editbox.title("Edit your Alarm")

            # Creates binds for this window
            editbox.bind('q', lambda e: editbox.destroy()) 
            
            # Widgets to be placed in the window            
            self.time = StringVar()
            time_entry = ttk.Entry(editboxFrame, width=20, textvariable=self.time) 
            time_entry.grid(column=2, row=3, sticky=E)

            self.date = StringVar()
            date_entry = ttk.Entry(editboxFrame, width=20, textvariable=self.date)
            date_entry.grid(column=2, row=4, sticky=E)
            
            self.ampm = StringVar()
            ttk.Radiobutton(editboxFrame, text="A.M.", variable=self.ampm, value='A.M.').grid(column=3, row=3,stick=(W,E))
            ttk.Radiobutton(editboxFrame, text="P.M.", variable=self.ampm, value='P.M.').grid(column=4, row=3,stick=(W,E))

            ttk.Label(editboxFrame, text='Time: ').grid(column=1, row=3, sticky=(W))
            ttk.Label(editboxFrame, text='Date: ').grid(column=1, row=4, sticky=W)
            savebtn = ttk.Button(editboxFrame,text='Save', command=self.editAlarm )
            savebtn.grid(column=3,row=4,sticky=(SE))
             
        else: 
            # If nothing is selected, present an error message
            messagebox.showinfo(message='Please select an alarm')
            


        


class Alarm:

    def __init__(self,time,date, ampm):
        self.time = time
        self.date = date
        self.ampm = ampm
        self.status = True  # This attribute indicates if the alarm is active or not, it will instantly be set to True(Active) when the alarm instance is activated
        self.sound = True # Currently a place holder value, I need to add a way in the GUI to select sounds from the database and correlate it to this class attribute

        d.addalarmtodb(self.time, self.date, self.ampm, self.status, self.sound) # This method adds the new alarm to the databse upon being instantiated
        self.id = d.getalarmid() # This retrieves the id from the database and stores it as an attribute so the alarm can later be identified

    # This allows for control of how the alarm is displayed in the listbox
    def __repr__(self):
        if self.status:
            return f'Alarm {self.id} set for {self.time}  {self.ampm} on {self.date} is active'
        else:
            return f'Alarm set for {self.time}  {self.ampm} on {self.date} is inactive'

    # The goal is to have the database pull daily on the alarms that will be needed for a certain day to limit alarm threads
    def alarmchecktoday(self):
        pass
    
    # The goal is for this method to handle the actual activation of the alarm 
    def alarmactivation(self):
        pass

""" The create_connection(), execute_query_(), and execute_read_query() methods are adapted from Real Python: https://realpython.com/python-sql-libraries/. 
    This turtorial helped me gain an understanding of the basics of SQLite.
"""
# This class will handle database entry and query
class database:
    def __init__(self):
        self.connection = self.create_connection("E:\\sm_app.sqlite")
        self.create_alarm_table = """
        CREATE TABLE IF NOT EXISTS alarm(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time  TEXT NOT NULL,
            date INTEGER NOT NULL,
            ampm TEXT NOT NULL,
            status TEXT NOT NULL,
            sound TEXT NOT NULL
        );
        """
        self.execute_query(self.connection, self.create_alarm_table)

    def create_connection(self, path): 
        """ This establishes a connection to the database and retruns it to be used by other methods"""      

        connection = None
        try:
            connection = sqlite3.connect(path) 
            print("Connection to SQLite DB succesful") # If the location exists a connection to the data base is established
        except Error as e: # Otherwise the error is handled and an error message is printed
            print(f"The error '{e}' occurred") 

        return connection # Retruns a conenction object, which can be used to execute queries


    def execute_query(self, connection, query, values=()):
        """ This method can be used to create tables and insert records into the created tables"""

        cursor = connection.cursor()
        try:
            cursor.execute(query, values) # This executes any query passed to it in form of string
            connection.commit()
            print("Query executed successfully")
        except Error as e: # This will print any error message if necessary
            print(f"The error '{e}' occurred")

    def execute_read_query(self, connection, query, values=()): 
        """ This method will fetch data out of the database """

        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            print("Read query happening")
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
    
    def getalarmid(self):
        """ This method retrieves the id given to the last entered alarm"""

        rowsearch = """SELECT * FROM alarm
                        ORDER BY id DESC LIMIT 1;         
        """
               
        row = self.execute_read_query(self.connection, rowsearch)
        
        # This block iterates over the row and extracts out the id from it
        for column in row:
            dbid = column[0]
            print(dbid)

        return dbid

    def addalarmtodb(self, time, date, ampm, status, sound):
        """ This adds the alarm to the database using a prepared statement"""

        create_alarm = """
        INSERT INTO 
            alarm (time, date, ampm, status, sound)
        VALUES
            (?, ?, ?, ?, ?);
        """
        self.execute_query(self.connection, create_alarm, (time, date, ampm, status, sound))
            
    def deletealarmdb(self, dbid):
        """ Currently not working, This method deletes the alarm from the database"""
        delete_alarm = "DELETE FROM alarm WHERE id = ?" # Create a prepared delete statement
                
        self.execute_query(self.connection, delete_alarm, (alarm.id)) # This deletes the selected entry from the database
        
if __name__ == '__main__':

    root = Tk() # Creates a Tkinter object
    
    d = database() # Intialize a connection to the database everytime the program is run
    
    AlarmClockGUI(root)
    root.mainloop() # Enter into the event loop


