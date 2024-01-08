import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import requests

#Global Variables
FONT = "Times New Roman"
FONTBOLD = "Times New Roman bold"
METCOLOR = '#d12d35'
BACKGROUNDCOLOR = 'white'
DEPARTMENT_ID_SEARCH = 'https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds='
OBJECT_ID_SEARCH = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/'
TOP_TEXT_TITLE = 'About DigiMet and The Metropolitan Museum of Art:'
TOP_TEXT_BODY_1 = "DigiMet is software that gives the user access to the Metropolitan Museum of Art's collection of" \
                  "artwork digitally through the use of their open access API." \
                  "\n\nThe Metropolitan Museum of Art houses over 5,000 years of art from around the world. The museum" \
                  "founded in 1870 and now occupies two locations in New York City. Their mission statement is to" \
                  "'collect, study, conserve, and present significant works of art from across time and cultures in order " \
                  "to connect all people to creativity, knowledge, ideas, and one another."
MIDDLE_TEXT_TITLE = 'Explanation of DigiMet Functions:'
MIDDLE_TEXT_BODY_1 = 'HOME BUTTON: This button will direct you back to the Welcome Page of the program.' \
                     '\n\nBACK BUTTON: This button will navigate back to the last page you visited until you reach' \
                     'the home page.' \
                     '\n\nSEARCH COLLECTION: This button will take you to a page where you can select a specific Met ' \
                     'department from a dropdown menu and search its catalog of objects. The objects will be displayed ' \
                     '10 at a time with the title and artist displayed. If the object does not have a title, it will ' \
                     'be shown as "Untitled". If the object does not have a credited artist, it will be shown ' \
                     'as "Unknown". You can hit the "Next" button to load more results or hit the "Previous" button to ' \
                     "go back to a past page's results. If you wish to view the details of an object, you can select" \
                     "the object and click 'View Object Details'. This will open a new window that shows information " \
                     "about the object." \
                     "\n\nSURPRISE ME: This button will select a random object from the Metropolitan's collection and " \
                     "display information about it in a new window."
BOTTOM_TITLE = 'For Further Questions and Assistance:'
BOTTOM_BODY = 'If you have further questions, contact digimetcollection@gmail.com.'
NOT_IN_PUBLIC_DOMAIN = 'Image is unavailable because it is not in the public domain.'


class DigiMet(tk.Tk):
    """
    Master Digimet class that creates the window to hold the different frames for our program. Creates the frames for our
    program at runtime and has methods to move between frames.
    """

    def __init__(self):
        super().__init__()

        #Window Features
        self.title("DigiMet: A Digital Art Collection")
        self.resizable(False, False)

        #Data Members
        self._frame_container = tk.Frame(self)
        self._frame_container.pack(side=TOP, fill=BOTH, expand=True)
        self._picture_object = {}
        self._picture_object_title = StringVar()
        self._frame_classes = [WelcomePage, HelpWindow, DepartmentSearchWindow, ObjectSearchWindow]
        self._frames = {}

        self.build_frames()

    def build_frames(self):
        """
        Builds the frames for the program.
        :return: Returns nothing
        """
        for page in self._frame_classes:
            frame = page(self._frame_container, self)
            self._frames[page] = frame
            frame.grid(row=0, column=0, sticky=NSEW)
        self.raise_frame(WelcomePage)

    def get_frames(self):
        """Returns the applications frames."""
        return self._frames

    def raise_frame(self, frame):
        """
        Switches the frame being displayed to the passed frame utilizing the tkraise() method.
        :param frame: The class name for the frame to be raised.
        :return: Returns nothing
        """
        frame = self._frames[frame]
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
        self._frames[to_frame].set_last_frame(from_frame)
        self.raise_frame(to_frame)

    def load_home(self):
        """
        Used to load the home page. It resets all of the last_frame variables on all pages.
        :return: Returns nothing
        """
        for frame_class in self._frame_classes:
            if frame_class != WelcomePage:
                self._frames[frame_class].set_last_frame([])
        self._frames[ObjectSearchWindow].reset_data_members()
        self._frames[DepartmentSearchWindow].reset_search_var()
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
            self._frames[ObjectSearchWindow].reset_data_members()
        last_frame = self._frames[from_page].get_last_frame()
        if last_frame == WelcomePage:
            self._frames[DepartmentSearchWindow].reset_search_var()
        if last_frame is not None:
            self.raise_frame(last_frame)

    def call_microservice(self):
        """
        Sends a request to the partner microservice to get a random object ID number.
        :return: nothing
        """
        while True:
            with open('DigiMetInput.txt', 'w') as file1:
                file1.write('get')
            file1.close()
            lucky_object = self.read_output_file()
            if lucky_object is True:
                break
        self.open_image_window()

    def read_output_file(self):
        """
        Reads the output file to check for microservice response.
        :return: lucky_object - boolean True or False to represent if the object is viable
        """
        while True:
            with open('DigiMetOutput.txt', 'r+') as file2:
                response = file2.readline()
                if response != '':
                    file2.seek(0)
                    file2.truncate()
                    file2.close()
                    lucky_object = self.get_lucky_object(response)
                    break
        return lucky_object

    def get_lucky_object(self, response):
        """
        Sends request to Met API to get info about a given Object ID
        :param response: Int - Represents Object ID for Met Object
        :return: Boolean - True or False - represents if the object is viable or not
        """
        lucky_object = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(response)).json()
        if 'message' in lucky_object.keys() or lucky_object['primaryImage'] == '':
            return False
        else:
            self.save_object_and_image(lucky_object)
            return True

    def save_object_and_image(self, object_dict):
        """
        Saves object info to windows data members for use elsewhere. If image exists, saves to jpeg.
        :param object_dict: Dictionary containing details about a give Met object
        :return: Returns nothing
        """
        self._picture_object = object_dict
        if self._picture_object['primaryImage'] != '':
            img_data = requests.get(object_dict['primaryImage']).content
            with open('met_image.jpg', 'wb') as handler:
                handler.write(img_data)
            image = Image.open('met_image.jpg')
            image.thumbnail((400, 400))
            image.save('image_thumbnail.jpg')

    def open_image_window(self):
        """
        Opens the image window to display the object info.
        :return: Returns nothing
        """
        image_window = Toplevel(bg=BACKGROUNDCOLOR)
        image_window.geometry('650x650')
        if self._picture_object['primaryImage'] == '':
            img_thumb = ImageTk.PhotoImage(Image.open('no_image.jpg'))
        else:
            img_thumb = ImageTk.PhotoImage(Image.open('image_thumbnail.jpg'))
        self.add_labels(image_window)
        image_panel = tk.Label(image_window, image=img_thumb)
        image_panel.place(relx=0.5, rely=0.4, anchor=CENTER)
        image_window.mainloop()

    def add_labels(self, image_window):
        """
        Adds labels to the image display window.
        :param image_window: Tkinter window object to display images
        :return: Returns nothing
        """
        if self._picture_object['primaryImage'] == '':
            public_domain_label = tk.Label(image_window, text=NOT_IN_PUBLIC_DOMAIN, wraplength=500, bg=BACKGROUNDCOLOR,
                                           font=(FONT, 15), fg=METCOLOR)
            public_domain_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        description = self.create_description()
        image_window.title(str(self._picture_object_title.get()))
        desc_label = tk.Label(image_window, text=description, wraplength=500, bg=BACKGROUNDCOLOR, font=(FONT, 15),
                              fg=METCOLOR)
        desc_label.place(relx=0.5, rely=0.85, anchor=CENTER)

    def create_description(self):
        """
        Creates description of a given Met Object
        :return: Str - Description to display
        """
        artist = 'Unknown' if self._picture_object['artistDisplayName'] == '' else self._picture_object['artistDisplayName']
        title = 'Untitled' if self._picture_object['title'] == '' else self._picture_object['title']
        date = 'Date Unknown' if self._picture_object['objectDate'] == '' else self._picture_object['objectDate']
        country = 'Location Unknown' if self._picture_object['artistNationality'] == '' else self._picture_object['artistNationality']
        medium = 'Medium Unknown' if self._picture_object['medium'] == '' else self._picture_object['medium']
        description = 'Artist/Creator: ' + artist + '\nTitle: ' + title + '\nDate: ' + date + \
                      '\nDepartment: ' + self._picture_object['department'] + '\nMedium: ' + medium + \
                      '\nArtist Nationality: ' + country
        self._picture_object_title.set('Met Object: ' + title)
        return description


class WelcomePage(tk.Frame):
    """
    WelcomePage frame class. This is the frame that is loaded on initial start-up and is the main hub of the program.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Widgets

        #Frame Background
        self._back_frame = Frame(self, bg=BACKGROUNDCOLOR, width=1000, height=700)
        self._back_frame.pack()

        #Welcome Text
        self._welcome_label = Label(self, text='Welcome to DigiMet', font=(FONT, 70), bg=BACKGROUNDCOLOR, fg=METCOLOR)
        self._welcome_label.place(relx=0.5, rely=0.25, anchor=CENTER)

        #Welcome Subtext
        self._desc_label = Label(self, text="Digital Access to the Metropolitan Museum of Art's Collection",
                                 font=(FONT, 30), bg=BACKGROUNDCOLOR, fg=METCOLOR)
        self._desc_label.place(relx=0.5, rely=0.35, anchor=CENTER)

        #Welcome Page Help Button
        self._help_button = Button(self, text='HELP', padx=5, pady=5, highlightbackground=METCOLOR, highlightthickness=1,
                                   fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                   command=lambda: controller.go_forward(WelcomePage, HelpWindow))
        self._help_button.place(x=915, y=3)

        #Search Button
        self._search_button = Button(self, text='Search Collection', padx=5, pady=5, highlightbackground=METCOLOR,
                                     command=lambda: controller.go_forward(WelcomePage, DepartmentSearchWindow),
                                     highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 30))
        self._search_button.place(relx=0.5, rely=0.55, anchor=CENTER)

        #Surprise Me Button
        self._lucky_button = Button(self, text='Surprise Me!', padx=5, pady=5, highlightbackground=METCOLOR,
                                    highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 30),
                                    command=controller.call_microservice)
        self._lucky_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        #Load Time Information Label
        self._load_label = Label(self, text="It may take a few seconds for result to load.",
                                 bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 10))
        self._load_label.place(relx=0.5, rely=0.7, anchor=CENTER)


class HelpWindow(tk.Frame):
    """
    HelpWindow frame class. This frame will display information about the software and the Met. This page is accessed by
    clicking on the help button on each page.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Data members to store info during program and
        self._last_frame = []

        #Widgets

        #Frame background
        self._back_frame = Frame(self, bg=BACKGROUNDCOLOR, width=1000, height=700)
        self._back_frame.pack()

        #Help Title Label
        self._help_label = Label(self, text='About DigiMet', fg=METCOLOR, bg=BACKGROUNDCOLOR, font=(FONT, 30))
        self._help_label.place(relx=0.5, rely=0.05, anchor=CENTER)

        #Help Page Home Button
        self._home_button_help_page = Button(self, text="HOME", padx=5, pady=5, highlightbackground=METCOLOR,
                                             highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                             command=controller.load_home)
        self._home_button_help_page.place(x=3, y=3)

        #Top Frame Container
        self._top_frame = Frame(self, width=950, height=200, padx=5, pady=5, highlightbackground=METCOLOR,
                                highlightthickness=5, relief=RAISED, bg=BACKGROUNDCOLOR)
        self._top_frame.place(relx=0.5, rely=0.23, anchor=CENTER)

        #Top Frame Title
        self._top_text_1 = Label(self._top_frame, text=TOP_TEXT_TITLE, bg=BACKGROUNDCOLOR, fg=METCOLOR,
                                 font=(FONTBOLD, 18))
        self._top_text_1.place(x=0, y=0)

        #Top Frame Description Text
        self._top_text_2 = Label(self._top_frame, text=TOP_TEXT_BODY_1, wraplength=900, justify=LEFT,
                                 bg=BACKGROUNDCOLOR,
                                 fg=METCOLOR, font=(FONT, 15))
        self._top_text_2.place(x=0, y=32)

        #Middle Frame Container
        self._middle_frame = Frame(self, width=950, height=250, padx=5, pady=5, highlightbackground=METCOLOR,
                                   highlightthickness=5, relief=RAISED, bg=BACKGROUNDCOLOR)
        self._middle_frame.place(relx=0.5, rely=0.57, anchor=CENTER)

        #Middle Frame Title
        self._middle_text_1 = Label(self._middle_frame, text=MIDDLE_TEXT_TITLE, wraplength=900, justify=LEFT,
                                    bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONTBOLD, 18))
        self._middle_text_1.place(x=0, y=0)

        #Middle Frame Description Text
        self._middle_text_2 = Label(self._middle_frame, text=MIDDLE_TEXT_BODY_1, wraplength=900, justify=LEFT,
                                    bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 15))
        self._middle_text_2.place(x=0, y=32)

        #Bottom Frame Container
        self._bottom_frame = Frame(self, width=950, height=100, padx=5, pady=5, highlightbackground=METCOLOR,
                                   highlightthickness=5, relief=RAISED, bg=BACKGROUNDCOLOR)
        self._bottom_frame.place(relx=0.5, rely=0.84, anchor=CENTER)

        #Bottom Frame Title
        self._bottom_text_1 = Label(self._bottom_frame, text=BOTTOM_TITLE, wraplength=900, justify=LEFT,
                                    bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONTBOLD, 18))
        self._bottom_text_1.place(x=0, y=0)

        #Bottom Frame Description Text
        self._bottom_text_2 = Label(self._bottom_frame, text=BOTTOM_BODY, wraplength=900, justify=LEFT,
                                    bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 15))
        self._bottom_text_2.place(x=0, y=32)

        #Help Page Back Button
        self._back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground=METCOLOR,
                                   highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                   command=lambda: controller.go_back(HelpWindow))
        self._back_button.place(x=97, y=3)

    def set_last_frame(self, page):
        """
        Adds the name of the page passed to the method to the last_frame member. This is used during backing tracking
        to the last page.
        :param page: The class name of the frame to be added to the last_Frame data member.
        :return: Returns nothing
        """
        self._last_frame.append(page)

    def get_last_frame(self):
        """
        Pops the name of the last frame visited out of the last_frame data member and returns it.
        :return: The class name of the last frame visited before this frame.
        """
        if len(self._last_frame) != 0:
            last_frame = self._last_frame.pop()
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

        self._controller = controller
        self._last_frame = []
        self._depts, self._codes = self.load_departments()
        self._search_var = tk.StringVar()

        #Widgets

        #Department Search Back Frame
        self._back_frame = Frame(self, bg=BACKGROUNDCOLOR, width=1000, height=700)
        self._back_frame.pack()

        #Department Search Home Button
        self._home_button_search_dept = Button(self, text="HOME", padx=5, pady=5, highlightbackground=METCOLOR,
                                               highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                               command=controller.load_home)
        self._home_button_search_dept.place(x=3, y=3)

        #Department Search Help Button
        self._help_button_search_dept = Button(self, text='HELP', padx=5, pady=5, highlightbackground=METCOLOR,
                                               highlightthickness=1,
                                               fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                               command=lambda: controller.go_forward(DepartmentSearchWindow, HelpWindow))
        self._help_button_search_dept.place(x=915, y=3)

        #Search Button
        self._search_button = Button(self, text='Search Department',
                                     command=lambda: self.search_department(self._search_var.get()), padx=5, pady=5,
                                     highlightbackground=METCOLOR,
                                     highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 30))
        self._search_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        #Department Search Back Button
        self._back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground=METCOLOR,
                                   highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                   command=lambda: controller.go_back(DepartmentSearchWindow))
        self._back_button.place(x=97, y=3)

        #Search Text Label
        self._search_label = Label(self, text="Search", bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 90))
        self._search_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Load Time Info Label
        self._load_label = Label(self, text="It may take a few seconds for results to load.",
                                 bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 10))
        self._load_label.place(relx=0.5, rely=0.55, anchor=CENTER)

        #DropDown Text Label
        self._dropdown_label = Label(self, text="Select a Department:", bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 20))
        self._dropdown_label.place(relx=0.335, rely=0.35, anchor=CENTER)

        # DropDown Combo Box
        self._style = ttk.Style()
        self._style.theme_use('classic')
        self._search_dropdown = ttk.Combobox(self, width=27, height=20, textvariable=self._search_var)
        self._search_dropdown.place(relx=0.555, rely=0.35, anchor=CENTER)
        self.option_add("*TCombobox*Listbox*Font", (FONT, 15))
        self._style.configure("TCombobox", fieldbackground="white", background=METCOLOR, arrowcolor=METCOLOR,
                              bordercolor=METCOLOR, arrowsize='20', selectforeground=METCOLOR, lightcolor=METCOLOR,
                              insertcolor=METCOLOR, selectbackground=BACKGROUNDCOLOR)
        self._search_dropdown['value'] = self._depts
        self._search_dropdown.current()

    @staticmethod
    def load_departments():
        """
        Loads the department names and codes by sending a request to the Met API and then saves that info in data members.
        :return: Returns two arrays. If the API request was successful, they will hold the department names and codes, otherwise,
        they will be empty.
        """
        depts = []
        codes = []
        dept_data = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/departments').json()
        dept_data = dept_data['departments']
        if dept_data:
            for ind in range(len(dept_data)):
                depts.append(dept_data[ind]['displayName'])
                codes.append(dept_data[ind]['departmentId'])
        return depts, codes

    def search_department(self, search_var):
        """
        When a department is selected in the dropdown box and the search button is hit, this method passes that information
        to the ObjectSearchWindow frame, tells that frame to begin searching that department's objects, and then raises
        that frame.
        :param search_var: Name of department to be searched
        :return: Returns nothing
        """
        for ind in range(len(self._depts)):
            if self._depts[ind] == search_var:
                frames = self._controller.get_frames()
                frames[ObjectSearchWindow].set_search_var(search_var, self._codes[ind])
                frames[ObjectSearchWindow].search_by_department()
                self._controller.go_forward(DepartmentSearchWindow, ObjectSearchWindow)

    def set_last_frame(self, page):
        """
        Adds the name of the page passed to the method to the last_frame member. This is used during backing tracking
        to the last page.
        :param page: The class name of the frame to be added to the last_Frame data member.
        :return: Returns nothing
        """
        self._last_frame.append(page)

    def get_last_frame(self):
        """
        Pops the name of the last frame visited out of the last_frame data member and returns it.
        :return: The class name of the last frame visited before this frame.
        """
        if len(self._last_frame) != 0:
            last_frame = self._last_frame.pop()
        else:
            last_frame = None
        return last_frame

    def reset_search_var(self):
        """Resets the search_var data member."""
        self._search_var.set('')


class ObjectSearchWindow(tk.Frame):
    """
    ObjectSearchWindow frame class. This frame is used to display search results 10 objects at a time.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Container data members to store data
        self._last_frame = []
        self._controller = controller
        self._code = ''
        self._search_var = ''
        self._results = {}
        self._total = 0
        self._depts = []
        self._start = 0
        self._end = 9
        self._list_box_details = []
        self._curr_objects = []
        self._objects_searched = []
        self._load_label_text = self.create_load_label_text()

        #Widgets

        #Object Search Results Frame
        self._back_frame = Frame(self, bg=BACKGROUNDCOLOR, width=1000, height=700)
        self._back_frame.pack()

        #Object Search Results Home Button
        self._home_button_search_dept = Button(self, text="HOME", padx=5, pady=5, highlightbackground=METCOLOR,
                                               highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                               command=controller.load_home)
        self._home_button_search_dept.place(x=3, y=3)

        #Object Search Results Help Button
        self._help_button_search_dept = Button(self, text='HELP', padx=5, pady=5, highlightbackground=METCOLOR,
                                               highlightthickness=1,
                                               fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                               command=lambda: controller.go_forward(ObjectSearchWindow, HelpWindow))
        self._help_button_search_dept.place(x=915, y=3)

        #Search Results Title Lable
        self._search_results_label = Label(self, text="Search Results", bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 70))
        self._search_results_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        #Listbox Frame - Holds ListBox and Scrollbar
        self._listbox_frame = Frame(self, bg=BACKGROUNDCOLOR)
        self._listbox_frame.place(relx=0.5, rely=0.4, anchor=CENTER)

        # ScrollBar - Scrolls horizontally in Listbox
        self._scrollbar = Scrollbar(self._listbox_frame, orient=HORIZONTAL)
        self._scrollbar.pack(side=BOTTOM, fill=X)

        #ListBox - Displays Results
        self._listbox_label = Label(self, text='Select a result:', bg=BACKGROUNDCOLOR, fg=METCOLOR, font=(FONT, 20))
        self._listbox_label.place(relx=0.18, rely=0.21)
        self._listbox = Listbox(self._listbox_frame, width=80, height=10, font=(FONT, 15), bg=BACKGROUNDCOLOR,
                                fg=METCOLOR, selectbackground=METCOLOR, highlightbackground=METCOLOR,
                                highlightthickness=1, xscrollcommand=self._scrollbar.set)
        self._listbox.pack(expand=True, fill=X)
        self._listbox.select_set(0)
        self._scrollbar.config(command=self._listbox.xview)

        #Results back button - Load prior 10 results
        self._result_back_button = Button(self, text='Previous', padx=5, pady=5, highlightbackground=METCOLOR,
                                          highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                          state=DISABLED, command=self.load_prev)
        self._result_back_button.place(relx=0.2, rely=0.6, anchor=CENTER)

        #Results next button - Loads next 10 results
        self._result_forward_button = Button(self, text='Next', padx=5, pady=5, highlightbackground=METCOLOR,
                                             highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED,
                                             font=(FONT, 15), command=self.load_more)
        self._result_forward_button.place(relx=0.8, rely=0.6, anchor=CENTER)

        #Object Search Results Page Back Button
        self._back_button = Button(self, text='BACK', padx=5, pady=5, highlightbackground=METCOLOR,
                                   highlightthickness=1, bg=BACKGROUNDCOLOR, fg=METCOLOR, relief=RAISED, font=(FONT, 15),
                                   command=lambda: controller.go_back(ObjectSearchWindow))
        self._back_button.place(x=97, y=3)

        #Search Button - Shows Object Details
        self._search_button = Button(self, text="View Object Details", padx=5, pady=5, highlightbackground=METCOLOR,
                                     highlightthickness=1, fg=METCOLOR, relief=RAISED, font=(FONT, 30),
                                     command=self.display_selected)
        self._search_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        #Time Information Label
        self._load_label = Label(self, text=self._load_label_text, bg=BACKGROUNDCOLOR, fg=METCOLOR,
                                 font=(FONT, 10))
        self._load_label.place(relx=0.5, rely=0.55, anchor=CENTER)

    def create_load_label_text(self):
        """
        Creates the text for the load label.
        :return: Str - returns string for label
        """
        text = "Total Number of Results: " + str(self._total) + ". It may take a few seconds for results to load."
        return text

    def set_search_var(self, new_search_var, new_code):
        """
        Sets the search_var and new_code data members. This method is called by the DepartmentSearchWindow class when a
        department is selected to be searched.
        :param new_search_var: New department to be searched
        :param new_code: New department code to be searched
        :return: Returns nothing
        """
        self._search_var = new_search_var
        self._code = new_code

    def search_by_department(self):
        """
        Based on the department code passed to the frame, an API request is sent to the Met and the results are saved.
        This method then calls the load_list_box() method to build out the entries in the display listbox.
        :return: Returns nothing
        """
        api_return = requests.get(DEPARTMENT_ID_SEARCH + str(self._code))
        api_return = api_return.json()
        self._results = api_return
        self._total = api_return['total']
        self._load_label.config(text="Total Number of Results: " + str(self._total) + ". It may take a few seconds for results to load.")
        self.load_list_box(self._start, self._end)

    def load_list_box(self, start, end):
        """
        Loads the list_box with a given range of Met objects.
        :param start: integer - starting index to be pulled/searched to display in the listbox
        :param end: integer - last index to be pulled/searched to display in the listbox
        :return: Returns nothing
        """
        self._curr_objects = []
        self.set_current_objects(start, end)
        self.fill_list_box(start)
        if end == len(self._objects_searched)-1:
            for num in range(start+10, end+11):
                self.pull_objects_from_met(num)

    def fill_list_box(self, start):
        """
        Fills the list box with new entries.
        :param start: Starting index of for the first object to be displayed in the list box.
        :return: Returns nothing
        """
        self.clear_list_box()
        listbox_index = 0
        display_index = start+1
        for met_object in self._curr_objects:
            display = self.create_entry_display(met_object, display_index)
            self._list_box_details.append(display)
            self._listbox.insert(listbox_index, display)
            listbox_index += 1
            display_index += 1

    def clear_list_box(self):
        """
        Deletes the entries in the current list box.
        :return: Returns nothing
        """
        self._listbox.delete(0, END)
        self._list_box_details = []

    @staticmethod
    def create_entry_display(met_object, display_index):
        """
        Creates the string that will be displayed for an entry in the list box.
        :param met_object: Dictionary for a given met_object
        :param display_index: Int - number representing the objects place in the display.
        :return: Returns nothing
        """
        display_name = met_object['artistDisplayName']
        if display_name == '':
            display_name = 'Unknown'
        title = met_object['title']
        if title == '':
            title = 'Untitled'
        display = str(display_index) + '. ' + str(title) + ' by ' + str(display_name)
        return display

    def set_current_objects(self, start, end):
        """
        Sets the new objects for the listbox to load.
        :param start: int - Starting index for
        :param end: int - Ending index to load
        :return:
        """
        self._curr_objects = []
        if end <= len(self._objects_searched):
            self._curr_objects = self._objects_searched[start:end+1]
        else:
            for num in range(start, end+1):
                object_info = self.pull_objects_from_met(num)
                self._curr_objects.append(object_info)

    def pull_objects_from_met(self, num):
        """
        Pulls new objects from Met API and saves to applicable data members
        :param num: Int - Index to pull the current object ID from the self._result data member
        :return: object_info: Dictionary containing info about a given object
        """
        object_id = self._results['objectIDs'][num]
        object_info = requests.get(OBJECT_ID_SEARCH + str(object_id)).json()
        self._objects_searched.append(object_info)
        return object_info

    def load_more(self):
        """
        Called when the Next button is selected to show 10 more results. Increments the start and end data members. If
        the end data member is greater than the length of the number of object IDs, it disables the Next button from
        being clicked and also sets the end index to the last index of the object IDs. If the Previous button is disabled,
        it enables it.
        :return: Returns nothing
        """
        self._start += 10
        self._end += 10
        if self._result_back_button['state'] == DISABLED:
            self._result_back_button['state'] = NORMAL
        if self._end >= self._total:
            self._end = self._total-1
            self._result_forward_button['state'] = DISABLED
        self.load_list_box(self._start, self._end)

    def load_prev(self):
        """
        Called when the Previous button is selected to show 10 prior results. Decrements the start and end data members. If
        the end data member is not cleanly divisible by 10 it rounds it sets it 9 indices higher than the start index.
        It disables the Previous button from being clicked if the start index. If the Next button is disabled, it enables it.
        :return:
        """
        self._start -= 10
        self._end = self._start + 9
        if self._result_forward_button['state'] == DISABLED:
            self._result_forward_button['state'] = NORMAL
        if self._start == 0:
            self._result_back_button['state'] = DISABLED
        self.load_list_box(self._start, self._end)

    def set_last_frame(self, page):
        """
        Adds the name of the page passed to the method to the last_frame member. This is used during backing tracking
        to the last page.
        :param page: The class name of the frame to be added to the last_Frame data member.
        :return: Returns nothing
        """
        self._last_frame.append(page)

    def get_last_frame(self):
        """
        Pops the name of the last frame visited out of the last_frame data member and returns it.
        :return: The class name of the last frame visited before this frame.
        """
        if len(self._last_frame) != 0:
            last_frame = self._last_frame.pop()
        else:
            last_frame = None
        return last_frame

    def reset_data_members(self):
        """
        Resets applicable data members when this page is navigated away from either, via the back button to the Search
        frame or when going to the Welcome Page.
        :return: Returns nothing
        """
        self._results = []
        self._depts = []
        self._start = 0
        self._end = 9
        self._list_box_details = []
        self._curr_objects = []
        self._objects_searched = []

    def display_selected(self):
        """
        Displays the selected Met object.
        :return: Returns nothing
        """
        for index in self._listbox.curselection():
            listing = str(self._listbox.get(index))
            number = self.pull_number(listing)
            self._controller.save_object_and_image(self._objects_searched[number])
            self._controller.open_image_window()

    @staticmethod
    def pull_number(listing):
        """
        Gets a given index number from the selected object in the list box. This index is used to pull the object info.
        :param listing: Str - String displayed from the current listing.
        :return: Int - Index of selected object to retrieve object info from self._objects_searched
        """
        number = ''
        for letter in listing:
            if letter == '.':
                break
            number += letter
        return int(number)-1


app = DigiMet()
app.mainloop()
