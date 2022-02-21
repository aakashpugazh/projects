import json
import warnings
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
    sems = ["sem1","sem2","sem3","sem4","sem5","sem6","sem7","sem8"]
    allsubs = {}
    num = 0
    den = 0
    for sem in sems:
        subs = database.fetch(semester=sem)
        subs = {j:k for i,j,k in subs}
        if subs.keys() == subjects[sem].keys():
            gradepoints = {i:grades[j] for i,j in subs.items()}
            for i in gradepoints:
                num += int(gradepoints[i]) * int(subjects[sem][i])
                den += int(subjects[sem][i])
            
    txt = str(round(num/den,3))
    return txt
            
    
    
class Handler:
    def subjectsWindow(self,sem):
        global semester
        semester = sem
        result = database.fetch(semester)
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
        result = database.fetch(semester)
        result = {j:k for i,j,k in result}
        subject = self.get_parent().get_children()[0].get_children()[0].get_text()
        grade = self.get_active_text()
        if subject in result:
            database.update(subject,grade)
        else:
            database.insert(semester,subject,grade)
        result = database.fetch(semester)
        result = {j:k for i,j,k in result}
        if result.keys() == subjects[semester].keys():
            lbl.set_text(gpacalculate(result))
    def claculate(self,lbl):
        result = database.fetch(semester)
        result = {j:k for i,j,k in result}
        lbl.set_text(gpacalculate(result))
    
    def closed(self):
        mainWindow.points_label.set_text(overallgpa())
        
class mainWindow(Gtk.Window):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.set_size_request(600, 600)
        cgpatxt = overallgpa()
        cgpa_label = label("CGPA :","Palatino Bold 20")
        self.points_label = label(cgpatxt,"Palatino Bold 20")
        sem1 = button("Sem 1",75,50,"Palatino Bold 20")
        sem2 = button("Sem 2",75,50,"Palatino Bold 20")
        sem3 = button("Sem 3",75,50,"Palatino Bold 20")
        sem4 = button("Sem 4",75,50,"Palatino Bold 20")
        sem5 = button("Sem 5",75,50,"Palatino Bold 20")
        sem6 = button("Sem 6",75,50,"Palatino Bold 20")
        sem7 = button("Sem 7",75,50,"Palatino Bold 20")
        sem8 = button("Sem 8",75,50,"Palatino Bold 20")
        sem1.connect("clicked",Handler.subjectsWindow,"sem1")
        sem2.connect("clicked",Handler.subjectsWindow,"sem2")
        sem3.connect("clicked",Handler.subjectsWindow,"sem3")
        sem4.connect("clicked",Handler.subjectsWindow,"sem4")
        sem5.connect("clicked",Handler.subjectsWindow,"sem5")
        sem6.connect("clicked",Handler.subjectsWindow,"sem6")
        sem7.connect("clicked",Handler.subjectsWindow,"sem7")
        sem8.connect("clicked",Handler.subjectsWindow,"sem8")

        
        
        tool_grid = Gtk.Grid()
        tool_grid.set_halign(Gtk.Align.CENTER)
        tool_grid.set_row_spacing(40)
        tool_grid.set_valign(Gtk.Align.CENTER)
        tool_grid.set_column_spacing(40)
        tool_grid.attach(cgpa_label,0,0,1,1)
        tool_grid.attach(self.points_label,1,0,1,1)
        tool_grid.attach(sem1,0,1,1,1)
        tool_grid.attach(sem2,1,1,1,1)
        tool_grid.attach(sem3,0,2,1,1)
        tool_grid.attach(sem4,1,2,1,1)
        tool_grid.attach(sem5,0,3,1,1)
        tool_grid.attach(sem6,1,3,1,1)
        tool_grid.attach(sem7,0,4,1,1)
        tool_grid.attach(sem8,1,4,1,1)
        
        self.add(tool_grid)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        
    
        
        
        
mainWindow = mainWindow()
Gtk.main()
