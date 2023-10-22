from tkinter import *

digimet_window = Tk()
digimet_window.geometry('1000x700')
digimet_window.configure(background="white")
digimet_window.title('DigiMet: A Digital Art Collection')
font ="Times New Roman"

welcome_label = Label(digimet_window, text='Welcome to DigiMet', font=(font, 70), bg='white', fg='#d12d35')
desc_label = Label(digimet_window, text="Digital Access to the Metropolitan Museum of Art's Collection", font=(font, 30), bg='white', fg=
                   '#d12d35')

def closeProgram():
    digimet_window.destroy()

def helpWindow():
    help_button.destroy()
    search_button.destroy()
    lucky_button.destroy()
    my_artwork_button.destroy()
    welcome_label.destroy()
    desc_label.destroy()
    #help_window = Toplevel(digimet_window)
    #help_window.geometry('800x500')
    #help_window.configure(background='white')
    #help_window.title('About DigiMet')
    digimet_window.title('About DigiMet')





exit_button = Button(text='X', command= closeProgram, padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 15))
help_button = Button(text='HELP', padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 15), command=helpWindow)
search_button = Button(text='Search Collection', padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 30))
lucky_button = Button(text='Surprise Me!', padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 30))
my_artwork_button = Button(text='Saved Artworks', padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 30))

welcome_label.place(relx=0.5, rely=0.25, anchor=CENTER)
desc_label.place(relx=0.5, rely=0.35, anchor=CENTER)
search_button.place(relx=0.5, rely=0.55, anchor=CENTER)
lucky_button.place(relx=0.5, rely=0.65, anchor=CENTER)
my_artwork_button.place(relx=0.5, rely=0.75, anchor=CENTER)
exit_button.place(x=3, y=3)
help_button.place(x=915, y=3)


digimet_window.mainloop()