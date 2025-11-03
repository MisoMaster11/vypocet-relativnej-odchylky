import tkinter as tk
from tkinter import messagebox

presnost_na_desatine_miesta = 5
background_color = 'gray95'

root = tk.Tk()
root.geometry("700x500")
root.title("Relatívna odchylka")
root.config(bg=background_color)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=100)

title = tk.Label(root, text='Relatívna odchylka', font=('Arial', 20), anchor='center', bg=background_color)
title.grid(row=0, column=0, sticky='nsew', columnspan=2)

entry_frame = tk.Frame(root, bg=background_color)
entry_frame.grid(row=1, column=0, sticky='nsew', columnspan=2)
entry_frame.columnconfigure(0, weight=1)
entry_frame.columnconfigure(1, weight=1)
entry_frame.columnconfigure(2, weight=1)

data_frame = tk.Frame(root, bg=background_color)
data_frame.grid(row=2, column=0, sticky='nsew', columnspan=2)
data_frame.columnconfigure(0, weight=1)
data_frame.columnconfigure(1, weight=1)
data_frame.columnconfigure(2, weight=1)

entry = tk.Entry(entry_frame, font=('Arial', 15))
entry.grid(row=1, column=0, sticky='nsew', pady=50, padx=10)
entry.focus()

enter = tk.Button(entry_frame, text='Enter', font=('Arial', 15))
enter.grid(row=1, column=1, sticky='nsew', pady=50)

clear = tk.Button(entry_frame, text='Clear', font=('Arial', 15))
clear.grid(row=1, column=2, sticky='nsew', padx=10, pady=50)

datavar = tk.StringVar()
data_listbox = tk.Listbox(root, font=('Arial', 15), listvariable=datavar)
data_listbox.grid(row=3, column=0, sticky='nsew',padx=10, pady=10)

deviationvar = tk.StringVar()
deviation_listbox = tk.Listbox(root, font=('Arial', 15), listvariable=deviationvar)
deviation_listbox.grid(row=3, column=1, sticky='nsew', padx=10, pady=10)

averagel = tk.Label(data_frame, text='Priemerná hodnota\n', font=('Arial', 15), bg=background_color)
averagel.grid(row=0, column=0, sticky='nsew')
avg_deviationl = tk.Label(data_frame, text='Priemerná odchylka\n', font=('Arial', 15), bg=background_color)
avg_deviationl.grid(row=0, column=1, sticky='nsew')
relative_deviationl = tk.Label(data_frame, text='Relatívna odchylka\n', font=('Arial', 15), bg=background_color)
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
    averagel.config(text='Priemerná hodnota\n' + str(round(avg, presnost_na_desatine_miesta)))
    avg_deviationl.config(text='Priemerná odchylka\n' + str(round(avg_deviation, presnost_na_desatine_miesta)))
    relative_deviationl.config(text='Relatívna odchylka\n' + str(round(relative_deviation, presnost_na_desatine_miesta)) + "%")
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

enter.config(command=add_to_list)
clear.config(command=clear_list)
root.bind_all('<BackSpace>', clear_list)
root.bind_all('<Delete>', clear_list)
root.bind_all('<Return>', add_to_list)
list_to_stringvar()
tk.mainloop()