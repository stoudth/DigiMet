import tkinter as tk
from tkinter import *
from tkinter import ttk
import requests

font ="Times New Roman"

class DigiMet(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("DigiMet: A Digital Art Collection")

        frame_container = tk.Frame(self)
        frame_container.pack(side=TOP, fill=BOTH, expand=True)
        self.resizable(False, False)

        self.frame_classes = [WelcomePage, HelpWindow, DepartmentSearchWindow, ObjectSearchWindow]
        self.frames = {}
        for page in self.frame_classes:
            frame = page(frame_container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, stick='nsew')
        self.raise_frame(WelcomePage)
        print(self.frames)

    def raise_frame(self, frame):
        frame = self.frames[frame]
        frame.tkraise()

    def go_forward(self, from_frame, to_frame):
        self.frames[to_frame].set_last_frame(from_frame)
        self.raise_frame(to_frame)

    def load_home(self):
        for frame_class in self.frame_classes:
            if frame_class != WelcomePage:
                self.frames[frame_class].set_last_frame([])
        self.raise_frame(WelcomePage)

    def go_back(self, from_page):
        last_frame = self.frames[from_page].get_last_frame()
        if last_frame is not None:
            self.raise_frame(last_frame)


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        self.back_frame = Frame(self, bg='white', width=1000, height=700)
        self.welcome_label = Label(self, text='Welcome to DigiMet', font=(font, 70), bg='white', fg='#d12d35')
        self.desc_label = Label(self, text="Digital Access to the Metropolitan Museum of Art's Collection",
                           font=(font, 30), bg='white', fg=
                           '#d12d35')
        self.help_button = Button(self, text='HELP', padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1,
                             fg='#d12d35', relief=RAISED, font=(font, 15), command=lambda:controller.go_forward(WelcomePage, HelpWindow))
        self.search_button = Button(self, text='Search Collection', padx=5, pady=5, highlightbackground='#d12d35', command=lambda:controller.go_forward(WelcomePage, DepartmentSearchWindow),
                               highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 30))
        self.lucky_button = Button(self, text='Surprise Me!', padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1,
                              fg='#d12d35', relief=RAISED, font=(font, 30), state=DISABLED)
        self.my_artwork_button = Button(self, text='Saved Artworks', padx=5, pady=5, highlightbackground='#d12d35',
                                   highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 30), state=DISABLED)

        self.back_frame.pack()
        self.welcome_label.place(relx=0.5, rely=0.25, anchor=CENTER)
        self.desc_label.place(relx=0.5, rely=0.35, anchor=CENTER)
        self.search_button.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.lucky_button.place(relx=0.5, rely=0.65, anchor=CENTER)
        self.my_artwork_button.place(relx=0.5, rely=0.75, anchor=CENTER)
        self.help_button.place(x=915, y=3)


class HelpWindow(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        #Container data member to store data
        self.last_frame = []
        top_text = 'About DigiMet:'

        #Widgets
        self.back_frame = Frame(self, bg='white', width=1000, height=700)
        self.help_label = Label(self, text='About DigiMet', fg='#d12d35', bg='white', font=(font, 30))
        self.home_button_help_page = Button(self, text="HOME", padx=5, pady=5, highlightbackground='#d12d35',
                                         highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 15),
                                         command=controller.load_home)
        self.top_frame = Frame(self, width=950, height=200, padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=5, relief=RAISED, bg='white')
        self.middle_frame = Frame(self, width=950, height=200, padx=5, pady=5, highlightbackground='#d12d35',
                          highlightthickness=5, relief=RAISED, bg='white')
        self.bottom_frame = Frame(self, width=950, height=200, padx=5, pady=5, highlightbackground='#d12d35',
                          highlightthickness=5, relief=RAISED, bg='white')
        self.back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground='#d12d35',
                                  highlightthickness=1, bg='white', fg='#d12d35', relief=RAISED, font=(font, 15),
                                  command=lambda: controller.go_back(HelpWindow))
        self.top_text = Label(self.top_frame)

        #Widget placement
        self.back_frame.pack()
        self.help_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.home_button_help_page.place(x=3, y=3)
        self.top_frame.place(relx=0.5, rely=0.23, anchor=CENTER)
        self.bottom_frame.place(relx=0.5, rely=0.83, anchor=CENTER)
        self.middle_frame.place(relx=0.5, rely=0.53, anchor=CENTER)
        self.back_button.place(x=97, y=3)

    def set_last_frame(self, page):
        self.last_frame.append(page)

    def get_last_frame(self):
        if len(self.last_frame) != 0:
            last_frame = self.last_frame.pop()
        else:
            last_frame = None
        return last_frame

        #if self.last_frame != WelcomePage:
            #self.back_button.destroy()


class DepartmentSearchWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Container data member to hold data
        self.last_frame = []

        #Grabs Met Departments when page is made
        self.launch_api = True
        if self.launch_api:
            self.depts, self.codes = self.load_departments()

        #Widgets
        self.back_frame = Frame(self, bg='white', width=1000, height=700)
        self.home_button_search_dept = Button(self, text="HOME", padx=5, pady=5, highlightbackground='#d12d35',
                                         highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 15),
                                         command=controller.load_home)
        self.help_button_search_dept = Button(self, text='HELP', padx=5, pady=5, highlightbackground='#d12d35',
                                         highlightthickness=1,
                                         fg='#d12d35', relief=RAISED, font=(font, 15),
                                         command=lambda: controller.go_forward(DepartmentSearchWindow, HelpWindow))
        self.search_button = Button(self, text='Search Department',
                                    command=lambda: self.search_department(self.search_var.get()), padx=5, pady=5,
                                    highlightbackground='#d12d35',
                                    highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 30))
        self.back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground='#d12d35',
                                  highlightthickness=1, bg='white', fg='#d12d35', relief=RAISED, font=(font, 15),
                                  command=lambda: controller.go_back(DepartmentSearchWindow))

        #Listbox Widget
        self.search_var = tk.StringVar()
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.option_add("*TCombobox*Listbox*Font", (font, 15))
        self.style.configure("TCombobox", fieldbackground="white", background='#d12d35', arrowcolor='#d12d35',
                             bordercolor='#d12d35', arrowsize='20', selectforeground='#d12d35', lightcolor='#d12d35',
                             insertcolor='#d12d35', selectbackground='white')
        self.search_dropdown = ttk.Combobox(self, width=27, height=20, textvariable=self.search_var)
        self.search_dropdown['value'] = self.depts
        self.search_dropdown.current()

        #Widget placement
        self.back_frame.pack()
        self.home_button_search_dept.place(x=3, y=3)
        self.help_button_search_dept.place(x=915, y=3)
        self.search_dropdown.place(relx=0.5, rely=0.35, anchor=CENTER)
        self.search_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.back_button.place(x=97, y=3)

    def load_departments(self):
        try:
            api_return = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/departments')
            data = api_return.json()
            data = data['departments']
            depts = []
            codes = []
            for ind in range(len(data)):
                depts.append(data[ind]['displayName'])
                codes.append(data[ind]['departmentId'])
            self.launch_api = False
            return depts, codes
        except:
            return []

    def search_department(self, search_var):
        for ind in range(len(self.depts)):
            if self.depts[ind] == search_var:
                self.controller.frames[ObjectSearchWindow].set_search_var(search_var, self.codes[ind])
                self.controller.frames[ObjectSearchWindow].search_by_department()
                self.controller.go_forward(DepartmentSearchWindow, ObjectSearchWindow)

    def set_last_frame(self, page):
        self.last_frame.append(page)

    def get_last_frame(self):
        if len(self.last_frame) != 0:
            last_frame = self.last_frame.pop()
        else:
            last_frame = None
        return last_frame


class ObjectSearchWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Container data members to store data
        self.last_frame = []
        self.controller = controller
        self.code = ''
        self.search_var = ''
        self.results = []
        self.depts = []
        self.launch_search = True
        self.start = 0
        self.end = 9
        self.list_box_details = []
        self.curr_objects = []

        #Widgets
        self.back_frame = Frame(self, bg='white', width=1000, height=700)
        self.home_button_search_dept = Button(self, text="HOME", padx=5, pady=5, highlightbackground='#d12d35',
                                              highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 15),
                                              command=controller.load_home)
        self.help_button_search_dept = Button(self, text='HELP', padx=5, pady=5, highlightbackground='#d12d35',
                                              highlightthickness=1,
                                              fg='#d12d35', relief=RAISED, font=(font, 15),
                                              command=lambda: controller.go_forward(ObjectSearchWindow, HelpWindow))
        self.search_results_label = Label(self, text="Search Results", bg='white', fg='#d12d35', font=(font, 70))
        self.listbox_label = Label(self, text='Select a result:', bg='white', fg='#d12d35', font=(font, 20))
        self.listbox = Listbox(self, width=80, height=10, font=(font, 15), bg='white', fg='#d12d35',
                               selectbackground='#d12d35', highlightbackground='#d12d35', highlightthickness=1)
        self.listbox.select_set(0)
        self.result_back_button = Button(self, text='Previous', padx=5, pady=5, highlightbackground='#d12d35',
                                         highlightthickness=1, bg='white', fg='#d12d35', relief=RAISED, font=(font, 15),
                                         state=DISABLED, command=self.load_prev)
        self.result_forward_button = Button(self, text='Next', padx=5, pady=5, highlightbackground='#d12d35',
                                            highlightthickness=1, bg='white', fg='#d12d35', relief=RAISED,
                                            font=(font, 15), command=self.load_more)
        self.back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground='#d12d35',
                                  highlightthickness=1, bg='white', fg='#d12d35', relief=RAISED, font=(font, 15),
                                  command=lambda: controller.go_back(ObjectSearchWindow))

        #Widget placement
        self.back_frame.pack()
        self.home_button_search_dept.place(x=3, y=3)
        self.help_button_search_dept.place(x=915, y=3)
        self.search_results_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.listbox.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.listbox_label.place(relx=0.15, rely=0.2)
        self.result_back_button.place(relx=0.2, rely=0.6, anchor=CENTER)
        self.result_forward_button.place(relx=0.8, rely=0.6, anchor=CENTER)
        self.back_button.place(x=97, y=3)

    def set_search_var(self, new_search_var, new_code):
        self.search_var = new_search_var
        self.code = new_code
        print(self.search_var)

    def return_search_var(self):
        print(self.search_var.get())

    def search_by_department(self):
        print(self.search_var)
        print(self.code)
        api_return = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=' + str(self.code))
        api_return = api_return.json()
        print(api_return)
        self.launch_search = False
        self.results = api_return
        self.load_list_box(self.start, self.end)

    def load_list_box(self, start, end):
        #self.listbox = Listbox(self, width=80, height=10, font=(font, 17), bg='white', fg='#d12d35', selectbackground='#d12d35', highlightbackground='#d12d35', highlightthickness=1)
        self.curr_objects = []
        for num in range(start, end+1):
            object_id = self.results['objectIDs'][num]
            object_info = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(object_id))
            self.curr_objects.append(object_info.json())
        self.listbox.delete(0, END)
        self.list_box_details = []
        listbox_index = 0
        display_index = start+1
        for object in self.curr_objects:
            display_name = object['artistDisplayName']
            if display_name == '':
                display_name = 'Unknown'
            title = object['title']
            if title == '':
                title = 'Untitled'
            display = str(display_index) + '. ' + str(title) + ' by ' + str(display_name)
            self.list_box_details.append(display)
            self.listbox.insert(listbox_index, display)
            listbox_index += 1
            display_index += 1
        print(self.list_box_details)

    def load_more(self):
        self.start += 10
        self.end += 10
        if self.result_back_button['state'] == DISABLED:
            self.result_back_button['state'] = NORMAL
        if self.end > len(self.results['objectIDs']):
            self.result_forward_button['state'] = DISABLED
        self.load_list_box(self.start, self.end)

    def load_prev(self):
        self.start -= 10
        self.end -= 10
        if self.result_forward_button['state'] == DISABLED:
            self.result_forward_button['state'] = NORMAL
        if self.start == 0:
            self.result_back_button['state'] = DISABLED
        self.load_list_box(self.start, self.end)

    def set_last_frame(self, page):
        self.last_frame.append(page)

    def get_last_frame(self):
        if len(self.last_frame) != 0:
            last_frame = self.last_frame.pop()
        else:
            last_frame = None
        return last_frame



app = DigiMet()
app.mainloop()

#digimet_window.mainloop()