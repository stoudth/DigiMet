import tkinter as tk
from tkinter import *
from tkinter import ttk
import requests

#---------------------CITATIONS------------------------------
#tkinter Module:
# Van Rossum, G. (2021). The Python Library Reference, release 3.10. Python Software Foundation.

#requests Module:
# (2023). Requests, release 2.31.0. Python Software Foundation.

#The class structure and controller class of the code was adapted from:
#soumibardhan10, ankit_kumar_, &amp; abhigoya. (2022, December 11).
# Tkinter application to switch between different page frames.
# GeeksforGeeks. https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
#____________________________________________________________

#Global Variables
FONT = "Times New Roman"
FONTBOLD = "Times New Roman bold"
METCOLOR = '#d12d35'
BACKGROUNDCOLOR = 'white'


class DigiMet(tk.Tk):
    """
    Master Digimet class that creates the window to hold the different frames for our program. Creates the frames for our
    program at runtime and has methods to move between frames.
    """

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
            frame.grid(row=0, column=0, sticky=NSEW)
        self.raise_frame(WelcomePage)

    def raise_frame(self, frame):
        """
        Switches the frame being displayed to the passed frame utilizing the tkraise() method.
        :param frame: The class name for the frame to be raised.
        :return: Returns nothing
        """
        frame = self.frames[frame]
        frame.tkraise()

    def go_forward(self, from_frame, to_frame):
        """
        Sets the last_frame variable in the from_frame to the that of the to_frame. This variable is used when the back
        button is pressed later.
        :param from_frame: The class name of the frame being moved away from. The last_frame variable is adjusted of this
                            page.
        :param to_frame: The class name of the frame being moved to. This is used when the last_frame variable is set and
                            also is then passed to the raise_frame() method.
        :return: Returns nothing
        """
        self.frames[to_frame].set_last_frame(from_frame)
        self.raise_frame(to_frame)

    def load_home(self):
        """
        Used to load the home page. It resets all of the last_frame variables on all pages.
        :return: Returns nothing
        """
        for frame_class in self.frame_classes:
            if frame_class != WelcomePage:
                self.frames[frame_class].set_last_frame([])
        self.frames[ObjectSearchWindow].reset_data_members()
        self.frames[DepartmentSearchWindow].reset_search_var()
        self.raise_frame(WelcomePage)

    def go_back(self, from_page):
        """
        Used to move back to the last frame visited. If the from_frame is of the ObjectSearchWindow class, it will
        reset some of that pages data members so that there will not be load problems if a new Search is initialized.
        :param from_page: The class name of the frame being left. This is needed to check if data members need to be reset
        and to know which frame to go to based on the last_frame variable.
        :return: Returns nothing
        """
        if from_page == ObjectSearchWindow:
            self.frames[ObjectSearchWindow].reset_data_members()
        last_frame = self.frames[from_page].get_last_frame()
        if last_frame == WelcomePage:
            self.frames[DepartmentSearchWindow].reset_search_var()
        if last_frame is not None:
            self.raise_frame(last_frame)


class WelcomePage(tk.Frame):
    """
    WelcomePage frame class. This is the frame that is loaded on initial start-up and is the main hub of the program.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Widgets
        self.back_frame = Frame(self, bg=BACKGROUNDCOLOR, width=1000, height=700)
        self.welcome_label = Label(self, text='Welcome to DigiMet', font=(FONT, 70), bg=BACKGROUNDCOLOR, fg=METCOLOR)
        self.desc_label = Label(self, text="Digital Access to the Metropolitan Museum of Art's Collection",
                                font=(FONT, 30), bg=BACKGROUNDCOLOR, fg=METCOLOR)
        self.help_button = Button(self, text='HELP', padx=5, pady=5, highlightbackground=METCOLOR, highlightthickness=1,
                                  fg=METCOLOR, relief=RAISED, font=(FONT, 15), command=lambda: controller.go_forward(WelcomePage, HelpWindow))
        self.search_button = Button(self, text='Search Collection', padx=5, pady=5, highlightbackground=METCOLOR, command=lambda: controller.go_forward(WelcomePage, DepartmentSearchWindow),
                                    highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 30))

        #Features to come
        #self.lucky_button = Button(self, text='Surprise Me!', padx=5, pady=5, highlightbackground=METCOLOR, highlightthickness=1,
                            #fg=METCOLOR, relief=RAISED, font=(FONT, 30), state=DISABLED)
        #self.my_artwork_button = Button(self, text='Saved Artworks', padx=5, pady=5, highlightbackground=METCOLOR,
                                #highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 30), state=DISABLED)

        #Place Widgets
        self.back_frame.pack()
        self.welcome_label.place(relx=0.5, rely=0.25, anchor=CENTER)
        self.desc_label.place(relx=0.5, rely=0.35, anchor=CENTER)
        self.search_button.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.help_button.place(x=915, y=3)

        #Features to come placement
        # self.lucky_button.place(relx=0.5, rely=0.65, anchor=CENTER)
        # self.my_artwork_button.place(relx=0.5, rely=0.75, anchor=CENTER)


class HelpWindow(tk.Frame):
    """
    HelpWindow frame class. This frame will display information about the software and the Met. This page is accessed by
    clicking on the help button on each page.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Data members to store info during program and
        self.last_frame = []
        top_text_title = 'About DigiMet and The Metropolitan Museum of Art:'
        top_text_body_1 = "DigiMet is software that gives the user access to the Metropolitan Museum of Art's collection of" \
            "artwork digitally through the use of their open access API."
        top_text_body_2 = "The Metropolitan Museum of Art houses over 5,000 years of art from around the world. The museum" \
                          "founded in 1870 and now occupies two locations in New York City. Their mission statement is to" \
                          "'collect, study, conserve, and present significant works of art from across time and cultures in order " \
                          "to connect all people to creativity, knowledge, ideas, and one another.'"

        middle_text_title = 'Explanation of DigiMet Functions:'
        middle_text_body_1 = 'HOME BUTTON: This button will direct you back to the Welcome Page of the program.'
        middle_text_body_2 = 'BACK BUTTON: This button will navigate back to the last page you visited until you reach' \
            'the home page.'
        middle_text_body_3 = 'SEARCH COLLECTION: This button will take you to a page where you can select a specific Met department' \
                             'from a dropdown menu and search its catalog of objects. The objects will be displayed 10 at a' \
                             'time with the title and artist displayed. If the object does not have a title, it will be shown' \
                             'as "Untitled". If the object does not have a credited artist, it will be shown as "Unknown". You' \
                             "can hit the 'Next' button to load more results or hit the 'Previous' button to go back to a past page's results."
        bottom_title = 'For Further Questions and Assistance:'
        bottom_text = 'If you have further questions, contact digimetcollection@gmail.com.'

        #Widgets
        self.back_frame = Frame(self, bg=BACKGROUNDCOLOR, width=1000, height=700)
        self.help_label = Label(self, text='About DigiMet', fg=METCOLOR, bg=BACKGROUNDCOLOR, font=(FONT, 30))
        self.home_button_help_page = Button(self, text="HOME", padx=5, pady=5, highlightbackground=METCOLOR,
                                            highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                            command=controller.load_home)
        self.top_frame = Frame(self, width=950, height=200, padx=5, pady=5, highlightbackground=METCOLOR, highlightthickness=5, relief=RAISED, bg=BACKGROUNDCOLOR)
        self.middle_frame = Frame(self, width=950, height=200, padx=5, pady=5, highlightbackground=METCOLOR,
                                  highlightthickness=5, relief=RAISED, bg=BACKGROUNDCOLOR)
        self.bottom_frame = Frame(self, width=950, height=200, padx=5, pady=5, highlightbackground=METCOLOR,
                                  highlightthickness=5, relief=RAISED, bg=BACKGROUNDCOLOR)
        self.back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground=METCOLOR,
                                  highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                  command=lambda: controller.go_back(HelpWindow))
        self.top_text_1 = Label(self.top_frame, text=top_text_title, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONTBOLD, 18))
        self.top_text_2 = Label(self.top_frame, text=top_text_body_1, wraplength=900, justify=LEFT, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 15))
        self.top_text_3 = Label(self.top_frame, text=top_text_body_2, wraplength=900, justify=LEFT, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 15))
        self.middle_text_1 = Label(self.middle_frame, text=middle_text_title, wraplength=900, justify=LEFT, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONTBOLD, 18))
        self.middle_text_2 = Label(self.middle_frame, text=middle_text_body_1, wraplength=900, justify=LEFT, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 15))
        self.middle_text_3 = Label(self.middle_frame, text=middle_text_body_2, wraplength=900, justify=LEFT, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 15))
        self.middle_text_4 = Label(self.middle_frame, text=middle_text_body_3, wraplength=900, justify=LEFT, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 15))
        self.bottom_text_1 = Label(self.bottom_frame, text=bottom_title, wraplength=900, justify=LEFT, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONTBOLD, 18))
        self.bottom_text_2 = Label(self.bottom_frame, text=bottom_text, wraplength=900, justify=LEFT, bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 15))

        #Widget placement
        self.back_frame.pack()
        self.help_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.home_button_help_page.place(x=3, y=3)
        self.top_frame.place(relx=0.5, rely=0.23, anchor=CENTER)
        self.bottom_frame.place(relx=0.5, rely=0.83, anchor=CENTER)
        self.middle_frame.place(relx=0.5, rely=0.53, anchor=CENTER)
        self.back_button.place(x=97, y=3)
        self.top_text_1.place(x=0, y=0)
        self.top_text_2.place(x=0, y=32)
        self.top_text_3.place(x=0, y=82)
        self.middle_text_1.place(x=0, y=0)
        self.middle_text_2.place(x=0, y=32)
        self.middle_text_3.place(x=0, y=62)
        self.middle_text_4.place(x=0, y=92)
        self.bottom_text_1.place(x=0, y=0)
        self.bottom_text_2.place(x=0, y=32)

    def set_last_frame(self, page):
        """
        Adds the name of the page passed to the method to the last_frame member. This is used during backing tracking
        to the last page.
        :param page: The class name of the frame to be added to the last_Frame data member.
        :return: Returns nothing
        """
        self.last_frame.append(page)

    def get_last_frame(self):
        """
        Pops the name of the last frame visited out of the last_frame data member and returns it.
        :return: The class name of the last frame visited before this frame.
        """
        if len(self.last_frame) != 0:
            last_frame = self.last_frame.pop()
        else:
            last_frame = None
        return last_frame


class DepartmentSearchWindow(tk.Frame):
    """
    DepartmentSearchWindow frame class. This window displays the department search which allows the user to select a
    department name from a dropdown menu and search the items for it.
    """

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
        self.back_frame = Frame(self, bg=BACKGROUNDCOLOR, width=1000, height=700)
        self.home_button_search_dept = Button(self, text="HOME", padx=5, pady=5, highlightbackground=METCOLOR,
                                              highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                              command=controller.load_home)
        self.help_button_search_dept = Button(self, text='HELP', padx=5, pady=5, highlightbackground=METCOLOR,
                                              highlightthickness=1,
                                              fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                              command=lambda: controller.go_forward(DepartmentSearchWindow, HelpWindow))
        self.search_button = Button(self, text='Search Department',
                                    command=lambda: self.search_department(self.search_var.get()), padx=5, pady=5,
                                    highlightbackground=METCOLOR,
                                    highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 30))
        self.back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground=METCOLOR,
                                  highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                  command=lambda: controller.go_back(DepartmentSearchWindow))
        self.search_label = Label(self, text="Search", bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 90))
        self.dropdown_label = Label(self, text="Select a Department:", bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 20))
        self.load_label = Label(self, text="It may take a few seconds for results to load.", bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 10))

        #Listbox Widget
        self.search_var = tk.StringVar()
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.option_add("*TCombobox*Listbox*Font", (FONT, 15))
        self.style.configure("TCombobox", fieldbackground="white", background=METCOLOR, arrowcolor=METCOLOR,
                             bordercolor=METCOLOR, arrowsize='20', selectforeground=METCOLOR, lightcolor=METCOLOR,
                             insertcolor=METCOLOR, selectbackground=BACKGROUNDCOLOR)
        self.search_dropdown = ttk.Combobox(self, width=27, height=20, textvariable=self.search_var)
        self.search_dropdown['value'] = self.depts
        self.search_dropdown.current()

        #Widget placement
        self.back_frame.pack()
        self.home_button_search_dept.place(x=3, y=3)
        self.help_button_search_dept.place(x=915, y=3)
        self.dropdown_label.place(relx=0.335, rely=0.35, anchor=CENTER)
        self.search_dropdown.place(relx=0.555, rely=0.35, anchor=CENTER)
        self.search_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.back_button.place(x=97, y=3)
        self.search_label.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.load_label.place(relx=0.5, rely=0.55, anchor=CENTER)

    def load_departments(self):
        """
        Loads the department names and codes by sending a request to the Met API and then saves that info in data members.
        :return: Returns two arrays. If the API request was successful, they will hold the department names and codes, otherwise,
        they will be empty.
        """
        depts = []
        codes = []
        api_return = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/departments')
        data = api_return.json()
        data = data['departments']
        if data:
            for ind in range(len(data)):
                depts.append(data[ind]['displayName'])
                codes.append(data[ind]['departmentId'])
        self.launch_api = False
        return depts, codes

    def search_department(self, search_var):
        """
        When a department is selected in the dropdown box and the search button is hit, this method passes that information
        to the ObjectSearchWindow frame, tells that frame to begin searching that department's objects, and then raises
        that frame.
        :param search_var: Name of department to be searched
        :return: Returns nothing
        """
        for ind in range(len(self.depts)):
            if self.depts[ind] == search_var:
                self.controller.frames[ObjectSearchWindow].set_search_var(search_var, self.codes[ind])
                self.controller.frames[ObjectSearchWindow].search_by_department()
                self.controller.go_forward(DepartmentSearchWindow, ObjectSearchWindow)

    def set_last_frame(self, page):
        """
        Adds the name of the page passed to the method to the last_frame member. This is used during backing tracking
        to the last page.
        :param page: The class name of the frame to be added to the last_Frame data member.
        :return: Returns nothing
        """
        self.last_frame.append(page)

    def get_last_frame(self):
        """
        Pops the name of the last frame visited out of the last_frame data member and returns it.
        :return: The class name of the last frame visited before this frame.
        """
        if len(self.last_frame) != 0:
            last_frame = self.last_frame.pop()
        else:
            last_frame = None
        return last_frame

    def reset_search_var(self):
        """Resets the search_var data member."""
        self.search_var.set('')


class ObjectSearchWindow(tk.Frame):
    """
    ObjectSearchWindow frame class. This frame is used to display search results 10 objects at a time.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Container data members to store data
        self.last_frame = []
        self.controller = controller
        self.code = ''
        self.search_var = ''
        self.results = []
        self.total = 0
        self.depts = []
        self.start = 0
        self.end = 9
        self.list_box_details = []
        self.curr_objects = []
        self.objects_searched = []

        #Widgets
        self.back_frame = Frame(self, bg=BACKGROUNDCOLOR, width=1000, height=700)
        self.listbox_frame = Frame(self, bg=BACKGROUNDCOLOR)
        self.scrollbar = Scrollbar(self.listbox_frame, orient=HORIZONTAL)
        self.home_button_search_dept = Button(self, text="HOME", padx=5, pady=5, highlightbackground=METCOLOR,
                                              highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                              command=controller.load_home)
        self.help_button_search_dept = Button(self, text='HELP', padx=5, pady=5, highlightbackground=METCOLOR,
                                              highlightthickness=1,
                                              fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                              command=lambda: controller.go_forward(ObjectSearchWindow, HelpWindow))
        self.search_results_label = Label(self, text="Search Results", bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 70))
        self.listbox_label = Label(self, text='Select a result:', bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 20))
        self.listbox = Listbox(self.listbox_frame, width=80, height=10, font=(FONT, 15), bg=BACKGROUNDCOLOR, fg=METCOLOR,
                               selectbackground=METCOLOR, highlightbackground=METCOLOR, highlightthickness=1, xscrollcommand=self.scrollbar.set)
        self.listbox.select_set(0)
        self.result_back_button = Button(self, text='Previous', padx=5, pady=5, highlightbackground=METCOLOR,
                                         highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                         state=DISABLED, command=self.load_prev)
        self.result_forward_button = Button(self, text='Next', padx=5, pady=5, highlightbackground=METCOLOR,
                                            highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED,
                                            font=(FONT, 15), command=self.load_more)
        self.back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground=METCOLOR,
                                  highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                  command=lambda: controller.go_back(ObjectSearchWindow))
        self.search_button = Button(self, text="View Object Details", padx=5, pady=5,
                                    highlightbackground=METCOLOR,
                                    highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 30), state=DISABLED)
        self.coming_feature = Label(self, text="Feature Coming Soon", bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 10))
        self.scrollbar.config(command=self.listbox.xview)
        self.load_label = Label(self, text="Total Number of Results: " + str(self.total) + ". It may take a few seconds for results to load.", bg=BACKGROUNDCOLOR, fg=METCOLOR,
                                font=(FONT, 10))


        #Widget placement
        self.back_frame.pack()
        self.listbox_frame.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.home_button_search_dept.place(x=3, y=3)
        self.help_button_search_dept.place(x=915, y=3)
        self.search_results_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.listbox.pack(expand=True, fill=X)
        self.listbox_label.place(relx=0.18, rely=0.21)
        self.result_back_button.place(relx=0.2, rely=0.6, anchor=CENTER)
        self.result_forward_button.place(relx=0.8, rely=0.6, anchor=CENTER)
        self.back_button.place(x=97, y=3)
        self.search_button.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.coming_feature.place(relx=0.5, rely=0.64, anchor=CENTER)
        self.scrollbar.pack(side=BOTTOM, fill=X)
        self.load_label.place(relx=0.5, rely=0.55, anchor=CENTER)

    def set_search_var(self, new_search_var, new_code):
        """
        Sets the search_var and new_code data members. This method is called by the DepartmentSearchWindow class when a
        department is selected to be searched.
        :param new_search_var: New department to be searched
        :param new_code: New department code to be searched
        :return: Returns nothing
        """
        self.search_var = new_search_var
        self.code = new_code

    def search_by_department(self):
        """
        Based on the department code passed to the frame, an API request is sent to the Met and the results are saved.
        This method then calls the load_list_box() method to build out the entries in the display listbox.
        :return: Returns nothing
        """
        api_return = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=' + str(self.code))
        api_return = api_return.json()
        self.results = api_return
        self.total = api_return['total']
        self.load_label.config(text="Total Number of Results: " + str(self.total) + ". It may take a few seconds for results to load.")
        self.load_list_box(self.start, self.end)

    def load_list_box(self, start, end):
        """
        Makes a request to the Met API for the objects between the start and end indices. It then saves this information,
        for faster load times if they need to be viewed and then add the title and artist information to the listbox. If
        applicable, the method will call the pre_load_next() method to get the next 10 objects for faster load time.
        Only 10 objects will be displayed at a time to reduce load on Met API per their request.
        :param start: integer - starting index to be pulled/searched to display in the listbox
        :param end: integer - last index to be pulled/searched to display in the listbox
        :return: Returns nothing
        """
        #If the items have already been retrieved from the Met API and saved
        self.curr_objects = []
        if end <= len(self.objects_searched):
            for num in range(start, end+1):
                self.curr_objects.append(self.objects_searched[num])

        #Pulls items from the Met API if not already retrieved
        else:
            for num in range(start, end+1):
                object_id = self.results['objectIDs'][num]
                object_info = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(object_id))
                object_info = object_info.json()
                self.curr_objects.append(object_info)
                self.objects_searched.append(object_info)

        #Inserts information for range of given indices into the listbox
        self.listbox.delete(0, END)
        self.list_box_details = []
        listbox_index = 0
        display_index = start+1
        for obj in self.curr_objects:
            display_name = obj['artistDisplayName']
            if display_name == '':
                display_name = 'Unknown'
            title = obj['title']
            if title == '':
                title = 'Untitled'
            display = str(display_index) + '. ' + str(title) + ' by ' + str(display_name)
            self.list_box_details.append(display)
            self.listbox.insert(listbox_index, display)
            listbox_index += 1
            display_index += 1

        #Requests to preload the next items if they haven't been loaded already
        if end == len(self.objects_searched)-1:
            self.pre_load_next(start+10, end+10)

    def pre_load_next(self, start, end):
        """
        Pre-loads the upcoming items in the search.
        :param start: integer - starting index to be pulled/searched to display in the listbox
        :param end: integer - last index to be pulled/searched to display in the listbox
        :return: Returns nothing
        """
        for num in range(start, end + 1):
            object_id = self.results['objectIDs'][num]
            object_info = requests.get(
                'https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(object_id))
            self.objects_searched.append(object_info.json())

    def load_more(self):
        """
        Called when the Next button is selected to show 10 more results. Increments the start and end data members. If
        the end data member is greater than the length of the number of object IDs, it disables the Next button from
        being clicked and also sets the end index to the last index of the object IDs. If the Previous button is disabled,
        it enables it.
        :return: Returns nothing
        """
        self.start += 10
        self.end += 10
        if self.result_back_button['state'] == DISABLED:
            self.result_back_button['state'] = NORMAL
        if self.end >= self.total:
            self.end = self.total-1
            self.result_forward_button['state'] = DISABLED
        self.load_list_box(self.start, self.end)

    def load_prev(self):
        """
        Called when the Previous button is selected to show 10 prior results. Decrements the start and end data members. If
        the end data member is not cleanly divisible by 10 it rounds it sets it 9 indices higher than the start index.
        It disables the Previous button from being clicked if the start index. If the Next button is disabled, it enables it.
        :return:
        """
        self.start -= 10
        self.end = self.start + 9
        if self.result_forward_button['state'] == DISABLED:
            self.result_forward_button['state'] = NORMAL
        if self.start == 0:
            self.result_back_button['state'] = DISABLED
        self.load_list_box(self.start, self.end)

    def set_last_frame(self, page):
        """
        Adds the name of the page passed to the method to the last_frame member. This is used during backing tracking
        to the last page.
        :param page: The class name of the frame to be added to the last_Frame data member.
        :return: Returns nothing
        """
        self.last_frame.append(page)

    def get_last_frame(self):
        """
        Pops the name of the last frame visited out of the last_frame data member and returns it.
        :return: The class name of the last frame visited before this frame.
        """
        if len(self.last_frame) != 0:
            last_frame = self.last_frame.pop()
        else:
            last_frame = None
        return last_frame

    def reset_data_members(self):
        """
        Resets applicable data members when this page is navigated away from either, via the back button to the Search
        frame or when going to the Welcome Page.
        :return: Returns nothing
        """
        self.results = []
        self.depts = []
        self.start = 0
        self.end = 9
        self.list_box_details = []
        self.curr_objects = []
        self.objects_searched = []


app = DigiMet()
app.mainloop()
