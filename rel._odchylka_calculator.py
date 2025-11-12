import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

#=========== Configuration ===========#
presnost_na_desatine_miesta = 5
background_color = "#D0F8FF"
button_color = "#66A9E0"
entry_and_list_color = "#EAFEFF"
text_color = 'black'
#=====================================#

button_hover = '#%02x%02x%02x' % tuple(int(int(c,16)*0.8) for c in [button_color[1:3], button_color[3:5], button_color[5:7]])

root = ctk.CTk(fg_color=background_color)
root.geometry("700x500")
root.title("Relatívna odchylka")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=100)

title = ctk.CTkLabel(root, text='Relatívna odchylka', text_color=text_color, font=('Arial', 30), anchor='center', fg_color=background_color)
title.grid(row=0, column=0, sticky='nsew', columnspan=2)

entry_frame = ctk.CTkFrame(root, fg_color=background_color)
entry_frame.grid(row=1, column=0, sticky='nsew', columnspan=2)
entry_frame.columnconfigure(0, weight=1)
entry_frame.columnconfigure(1, weight=1)
entry_frame.columnconfigure(2, weight=1)

data_frame = ctk.CTkFrame(root, fg_color=background_color)
data_frame.grid(row=2, column=0, sticky='nsew', columnspan=2)
data_frame.columnconfigure(0, weight=1)
data_frame.columnconfigure(1, weight=1)
data_frame.columnconfigure(2, weight=1)

entry = ctk.CTkEntry(entry_frame, text_color=text_color, font=('Arial', 20), fg_color=entry_and_list_color)
entry.grid(row=1, column=0, sticky='nsew', pady=50, padx=10)
entry.focus()

enter = ctk.CTkButton(entry_frame, text='Enter', hover_color=button_hover, text_color=text_color, font=('Arial', 20), fg_color=button_color)
enter.grid(row=1, column=1, sticky='nsew', pady=50)

clear = ctk.CTkButton(entry_frame, text='Clear', text_color=text_color, hover_color=button_hover, font=('Arial', 20), fg_color=button_color)
clear.grid(row=1, column=2, sticky='nsew', padx=10, pady=50)

datavar = tk.StringVar()
data_listbox = tk.Listbox(root, fg=text_color, font=('Arial', 20), listvariable=datavar, bg=entry_and_list_color)
data_listbox.grid(row=3, column=0, sticky='nsew',padx=30, pady=30)

deviationvar = tk.StringVar()
deviation_listbox = tk.Listbox(root, fg=text_color, font=('Arial', 20), listvariable=deviationvar, background=entry_and_list_color)
deviation_listbox.grid(row=3, column=1, sticky='nsew', padx=30, pady=30)

averagel = ctk.CTkLabel(data_frame, text='Priemerná hodnota\n', text_color=text_color, font=('Arial', 20), fg_color=background_color)
averagel.grid(row=0, column=0, sticky='nsew')
avg_deviationl = ctk.CTkLabel(data_frame, text='Priemerná odchylka\n', text_color=text_color, font=('Arial', 20), fg_color=background_color)
avg_deviationl.grid(row=0, column=1, sticky='nsew')
relative_deviationl = ctk.CTkLabel(data_frame, text='Relatívna odchylka\n', text_color=text_color, font=('Arial', 20), fg_color=background_color)
relative_deviationl.grid(row=0, column=2, sticky='nsew')

data_list = []

def list_to_stringvar(list = [], avg: float = 0, avg_deviation: float = 0, deviations = [], relative_deviation: float = 0):
    global datavar, deviationvar
    strdata = 'Údaje: \n'
    strdeviations = 'Odchylky: \n'
    for i in list:
        strdata += str(round(i, presnost_na_desatine_miesta)) + '\n'
    for i in deviations:
        strdeviations += '+' if i >= 0 else '- '
        strdeviations += str(round(abs(i), presnost_na_desatine_miesta)) + '\n'
    averagel.configure(text='Priemerná hodnota\n' + str(round(avg, presnost_na_desatine_miesta)))
    avg_deviationl.configure(text='Priemerná odchylka\n' + str(round(avg_deviation, presnost_na_desatine_miesta)))
    relative_deviationl.configure(text='Relatívna odchylka\n' + str(round(relative_deviation, presnost_na_desatine_miesta)) + "%")
    deviationvar.set(strdeviations)
    datavar.set(strdata)

def add_to_list(event = None):
    global data_list
    txt = entry.get()
    if txt:
        try:
            txt = float(txt)
            data_list.append(txt)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
        entry.delete(0, tk.END)
        calculate()

def calculate(event = None):
    global data_list
    if len(data_list) > 0:
        avg = sum(data_list) / len(data_list)
        deviations = []
        abs_deviations = []
        for i in data_list:
            deviations.append(i - avg)
            abs_deviations.append(abs(i - avg))
        avg_deviation = sum(abs_deviations) / len(abs_deviations)
        relative_deviation = avg_deviation / avg * 100
        
        list_to_stringvar(data_list, avg, avg_deviation, deviations, relative_deviation)

def clear_list(event = None):
    global data_list
    data_list = []
    list_to_stringvar(data_list)

enter.configure(command=add_to_list)
clear.configure(command=clear_list)
root.bind_all('<BackSpace>', clear_list)
root.bind_all('<Delete>', clear_list)
root.bind_all('<Return>', add_to_list)
list_to_stringvar()
root.mainloop()