import json
import warnings,sys
from db import Database
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GLib
warnings.filterwarnings("ignore")

sfile = open("./subjects.json","r")
subjects = json.load(sfile)
grades = {"O":10,"A+":9,"A":8,"B+":7,"B":6,"RA":0,"SA":0}
database = Database("Cgpa.db")

def label(name, des=None, w=None, h=None):
        Label = Gtk.Label()
        Label.set_text(name)
        if w and h:
            Label.set_size_request(w, h)
        if des:
            Label.override_font(Pango.FontDescription(des))
        Label
        return Label

def button(name, w=None, h=None, des=None, handler=None,args=None):
        btn = Gtk.Button()
        lbl = label(name, des)
        btn.add(lbl)
        if w and h:
            btn.set_size_request(w, h)
        if handler and not args:
            btn.connect("clicked", handler)
        if handler and args:
            btn.connect("clicked", handler,args)
        return btn
def gradebox():
    # entries = Gtk.ListStore(str)
    # for i in grades:
    #     entries.append([i])
    # gb = Gtk.ComboBox.new_with_model_and_entry(entries)
    gb = Gtk.ComboBoxText()
    for i in grades:
        gb.append_text(i)
    return gb

def gpacalculate(result):
    gradepoints = {i:grades[j] for i,j in result.items()}
    num = 0
    den = 0
    for i in gradepoints:
        num += int(gradepoints[i]) * int(subjects[semester][i])
        den += int(subjects[semester][i])
    txt = str(round(num/den,3))
    return txt

def overallgpa():
    txt = "0"
    if username == "Users":
        return "0"
    sems = ["sem1","sem2","sem3","sem4","sem5","sem6","sem7","sem8"]
    allsubs = {}
    num = 0
    den = 0
    for sem in sems:
        subs = database.fetch(semester=sem,username=username)
        subs = {j:k for i,j,k in subs}
        if subs.keys() == subjects[sem].keys():
            gradepoints = {i:grades[j] for i,j in subs.items()}
            for i in gradepoints:
                num += int(gradepoints[i]) * int(subjects[sem][i])
                den += int(subjects[sem][i])
    if den != 0:  
        txt = str(round(num/den,3))
    return txt

def messagedialog(parent,text):
    dialog = Gtk.MessageDialog(
    transient_for=parent.get_parent().get_parent(),
    message_type=Gtk.MessageType.INFO,
    buttons=Gtk.ButtonsType.OK,
    text=text)
    dialog.run()
    dialog.destroy()
            
    
    
class Handler:
    def subjectsWindow(self,sem):
        userbox = mainWindow.get_children()[0].get_children()[-1]
        if userbox.get_active_text() == "Users":
            messagedialog(self,"Please select a user and then try")
            return
        global semester
        semester = sem
        result = database.fetch(semester,username)
        result = {j:k for i,j,k in result}
        semsub = [i for i in subjects[sem]]
        np_window = Gtk.Dialog(parent=mainWindow)
        np_window.set_title("Subjects")
        np_window.set_resizable(False)
        subjectsGrid = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        subjectsGrid.set_margin_start(15)
        subjectsGrid.set_margin_end(15)
        subjectsGrid.set_margin_top(15)
        subjectsGrid.set_margin_bottom(15)
        subjectsGrid.set_spacing(25)
        gpa = label("0",des="Palatino Bold 15")
        for i in range(len(semsub)):
            pairBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            gb = gradebox()
            align = Gtk.Alignment(xscale=0,xalign=0)
            btn = label(str(semsub[i]),"Palatino Bold 15")
            if semsub[i] in result.keys():
                gb.set_active(list(grades.keys()).index(result[semsub[i]]))
                gb.connect("changed",Handler.gradeSelected,gpa)
            else:
                gb.connect("changed",Handler.gradeSelected,gpa)
            align.add(btn)
            pairBox.pack_start(align,True,True,10)
            pairBox.add(gb)
            subjectsGrid.add(pairBox)
        calculate = label("Your GPA is",des="Calibri Bold 15")
        subjectsGrid.add(calculate)
        if result.keys() == subjects[semester].keys():
            gpa.set_text(gpacalculate(result))
        subjectsGrid.add(gpa)
        np_window.vbox.add(subjectsGrid)
        np_window.set_transient_for(mainWindow)
        np_window.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        np_window.set_modal(True)
        np_window.connect("destroy",Handler.closed)
        np_window.show_all()
    def gradeSelected(self,lbl):
        result = database.fetch(semester,username)
        result = {j:k for i,j,k in result}
        subject = self.get_parent().get_children()[0].get_children()[0].get_text()
        grade = self.get_active_text()
        if subject in result:
            database.update(subject,grade,username)
        else:
            database.insert(semester,subject,grade,username)
        result = database.fetch(semester,username)
        result = {j:k for i,j,k in result}
        if result.keys() == subjects[semester].keys():
            lbl.set_text(gpacalculate(result))
    def claculate(self,lbl):
        result = database.fetch(semester,username)
        result = {j:k for i,j,k in result}
        lbl.set_text(gpacalculate(result))
    
    def closed(self):
        mainWindow.points_label.set_text(overallgpa())
    
    def createuserwindow(self):
        userbox = Gtk.Dialog()
        userbox.set_title("Create User")
        userbox.set_resizable(False)
        userbox.set_transient_for(mainWindow)
        userbox.set_modal(True)
        userbox.set_position(Gtk.WindowPosition.CENTER)
        namelabel = label("Enter User Name","Palatino Bold 20")
        namefield = Gtk.Entry()
        createbutton = button("Create",55,30,"Palatino Bold 20",Handler.createuser,namefield)
        deletebutton = button("delete",55,30,"Palatino Bold 20",Handler.deleteuser,namefield)
        userbox.vbox.set_margin_start(20)
        userbox.vbox.set_margin_end(20)
        userbox.vbox.set_margin_top(20)
        userbox.vbox.set_margin_bottom(20)
        userbox.vbox.set_spacing(20)
        userbox.vbox.add(namelabel)
        userbox.vbox.add(namefield)
        userbox.vbox.add(createbutton)
        userbox.vbox.add(deletebutton)
        userbox.show_all()
    
    def createuser(self,namefield):
        username = namefield.get_text()
        if username == "":
            messagedialog(self,"Enter valid Username")
        else:
            mainWindow.get_children()[0].get_children()[-1].append_text(username)
        res = database.create(username)
        if res == -1:
            messagedialog(self,"User already exist")
        else:
            namefield.get_parent().get_parent().destroy()
    
    def userselected(self,points):
        global username
        username = self.get_active_text()
        gpa = overallgpa()
        points.set_text(gpa)
    
    def deleteuser(self,namefield):
        user = namefield.get_text()
        users = database.fetchusers()
        if user in users:
            confirm = Gtk.MessageDialog(transient_for=self.get_parent().get_parent(),modal=True,buttons=Gtk.ButtonsType.OK_CANCEL)
            confirm.props.text = "Are You sure to delete %s"%(user)
            response = confirm.run()
            confirm.destroy()
            if response == Gtk.ResponseType.OK:
                database.deleteuser(user)
                messagedialog(self,"User is deleted App will be closed\nnow restart the app")
                sys.exit()
        else:
            messagedialog(self,"User Not Found")
        
class mainWindow(Gtk.Window):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.set_size_request(600, 600)
        global username 
        username = "Users"
        cgpatxt = overallgpa()
        users = Gtk.ComboBoxText()
        users.append_text("Users")
        users.set_active(0)
        createuser = button("Create/Delete",75,30,"Palatino Bold 20",Handler.createuserwindow)
        for user in database.fetchusers():
            users.append_text(user)
        cgpa_label = label("CGPA :","Palatino Bold 20")
        self.points_label = label(cgpatxt,"Palatino Bold 20")
        users.connect("changed",Handler.userselected,self.points_label)
        sem1 = button("Sem 1",75,50,"Palatino Bold 20",Handler.subjectsWindow,"sem1")
        sem2 = button("Sem 2",75,50,"Palatino Bold 20",Handler.subjectsWindow,"sem2")
        sem3 = button("Sem 3",75,50,"Palatino Bold 20",Handler.subjectsWindow,"sem3")
        sem4 = button("Sem 4",75,50,"Palatino Bold 20",Handler.subjectsWindow,"sem4")
        sem5 = button("Sem 5",75,50,"Palatino Bold 20",Handler.subjectsWindow,"sem5")
        sem6 = button("Sem 6",75,50,"Palatino Bold 20",Handler.subjectsWindow,"sem6")
        sem7 = button("Sem 7",75,50,"Palatino Bold 20",Handler.subjectsWindow,"sem7")
        sem8 = button("Sem 8",75,50,"Palatino Bold 20",Handler.subjectsWindow,"sem8")
        
        
        tool_grid = Gtk.Grid()
        tool_grid.set_halign(Gtk.Align.CENTER)
        tool_grid.set_row_spacing(40)
        tool_grid.set_column_homogeneous(True)
        tool_grid.set_valign(Gtk.Align.CENTER)
        tool_grid.set_column_spacing(40)
        tool_grid.attach(users,0,0,1,1)
        tool_grid.attach(createuser,1,0,1,1)
        tool_grid.attach(cgpa_label,0,1,1,1)
        tool_grid.attach(self.points_label,1,1,1,1)
        tool_grid.attach(sem1,0,2,1,1)
        tool_grid.attach(sem2,1,2,1,1)
        tool_grid.attach(sem3,0,3,1,1)
        tool_grid.attach(sem4,1,3,1,1)
        tool_grid.attach(sem5,0,4,1,1)
        tool_grid.attach(sem6,1,4,1,1)
        tool_grid.attach(sem7,0,5,1,1)
        tool_grid.attach(sem8,1,5,1,1)
        
        self.add(tool_grid)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        
    
        
        
        
mainWindow = mainWindow()
Gtk.main()
