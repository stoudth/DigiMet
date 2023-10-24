
#Here is another simple answer, but without using classes.

from tkinter import *

font ="Times New Roman"

def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.geometry('1000x700')
root.title('DigiMet: A Digital Art Collection')

welcome_page = Frame(root, width=1000, height=700, bg='white')
f2 = Frame(root, width=1000, height=700, bg='white')
f3 = Frame(root)
f4 = Frame(root)

for frame in (welcome_page, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

def close_program():
    root.destroy()


#Welcome Page
welcome_label = Label(welcome_page, text='Welcome to DigiMet', font=(font, 70), bg='white', fg='#d12d35')
desc_label = Label(welcome_page, text="Digital Access to the Metropolitan Museum of Art's Collection",
                font=(font, 30), bg='white', fg=
                '#d12d35')
exit_button_welcome = Button(welcome_page, text='X', padx=5, pady=5, highlightbackground='#d12d35',
                        highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 15), command=close_program)
help_button = Button(welcome_page, text='HELP', padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1,
                             fg='#d12d35', relief=RAISED, font=(font, 15), command=lambda:raise_frame(f2))
search_button = Button(welcome_page, text='Search Collection', padx=5, pady=5, highlightbackground='#d12d35',
                               highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 30))
lucky_button = Button(welcome_page, text='Surprise Me!', padx=5, pady=5, highlightbackground='#d12d35', highlightthickness=1,
                              fg='#d12d35', relief=RAISED, font=(font, 30))
my_artwork_button = Button(welcome_page, text='Saved Artworks', padx=5, pady=5, highlightbackground='#d12d35',
                                   highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 30))
welcome_label.place(relx=0.5, rely=0.25, anchor=CENTER)
desc_label.place(relx=0.5, rely=0.35, anchor=CENTER)
search_button.place(relx=0.5, rely=0.55, anchor=CENTER)
lucky_button.place(relx=0.5, rely=0.65, anchor=CENTER)
my_artwork_button.place(relx=0.5, rely=0.75, anchor=CENTER)
exit_button_welcome.place(x=3, y=3)
help_button.place(x=915, y=3)
help_button.place(x=915, y=3)

help_label = Label(f2, text='About DigiMet', bg='white', fg='#d12d35')
exit_button_help = Button(f2, text='X', padx=5, pady=5, highlightbackground='#d12d35',
                        highlightthickness=1, fg='#d12d35', relief=RAISED, font=(font, 15), command=close_program)
exit_button_help.place(x=3, y=3)
help_label.pack()

Label(f3, text='FRAME 3').pack(side='left')
Button(f3, text='Go to frame 4', command=lambda:raise_frame(f4)).pack(side='left')

Label(f4, text='FRAME 4').pack()
Button(f4, text='Goto to frame 1', command=lambda:raise_frame(welcome_page)).pack()

raise_frame(welcome_page)
root.mainloop()