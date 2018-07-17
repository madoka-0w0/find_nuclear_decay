import json
import sys
import tkinter as tk
import tkinter.filedialog

import os

from calc import *
from data import *
from constants import *


class Manager:
    def __init__(self, in_file, out_file, inputs, regex=Constants.regex):
        self.in_file = in_file
        self.out_file = out_file
        self.calc = calc(self.conform(inputs))
        self.regex = regex

    def run(self):
        with open(self.out_file, "w", encoding=Constants.encoding) as out_f:
            self.write_setting(out_f)
            with open(self.in_file, "r", encoding=Constants.encoding) as in_f:
                for line in in_f.readlines():
                    strings = line.strip().split(self.regex)
                    if len(strings) > 5:
                        data = data_set(strings)
                        self.calc.classify(data)
                        if data.event_num % 1500 == 0:  # clean check time(lines) span
                            self.clean(out_f, data)
                        if data.event_num % 10000 == 0:
                            print(str(data.event_num) + "  ,parents_size=" + str(len(self.calc.parents)))
            self.flush(out_f)

    def clean(self, out_f, data):
        for index, parent in enumerate(self.calc.parents):
            if data.event_num - parent.event_num > 50000:  # number of avoid data tokoroten
                children = self.calc.childrens[index]
                if len(children) > 0:
                    self.write(out_f, parent, children)
                del self.calc.parents[index]
                del self.calc.childrens[index]

    def write_setting(self, out_f):
        out_f.write("---setting---\n")
        for daughter, values in sorted(self.calc.energy_range.items(), key=lambda x: x[0]):
            out_f.write(str(daughter) + " : " + str(values[Constants.min]) + " ~ " + str(
                values[Constants.max]) + ", time=" + str(
                self.s2ten_ns(self.calc.duration[daughter], reverse=True)) + "[s]\n")
        out_f.write("-------------\n")
        out_f.write("-------------\n")

    def write(self, out_f, parent, children):
        out_f.write(str(parent) + "\n")
        parent_time = parent.time
        for child in children:
            diff = self.s2ten_ns(child.time - parent_time, reverse=True)
            out_f.write(str(child) + ", decay=" + str(diff) + "[s]" + "\n")
        out_f.write('---------\n')

    def flush(self, out_f):
        parents = self.calc.parents
        childrens = self.calc.childrens
        for i in range(len(parents)):
            if len(childrens[i]) > 0:
                self.write(out_f, parents[i], childrens[i])
        self.calc.parents = list()
        self.calc.childrens = list()

    @staticmethod
    def s2ten_ns(num, reverse=False):
        if reverse:
            return int(num) * (10 ** (-8))
        else:
            return float(num) * (10 ** 8)

    def conform(self, inputs):
        for daughter, values in inputs.items():
            value = values[Constants.time]
            if value:
                values[Constants.time] = self.s2ten_ns(float(value))
        return inputs


class Display(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.geometry("900x250")

        self.in_file_entry = tk.Entry()

        self.settings = self.load_settings()
        self.entry_map = self.create_entry_map([Constants.D1, Constants.D2, Constants.D3, Constants.D4, Constants.D5],
                                               [Constants.min, Constants.max, Constants.time], self.settings)
        self.info = tk.StringVar()
        self.info.set("")

        self.menubar = tk.Menu(self)
        master.configure(menu=self.menubar)
        self.menu(self.menubar)
        self.widgets()

    def load_settings(self):
        with open(Constants.settings_file, "r", encoding=Constants.encoding) as f:
            return json.load(f)

    def widgets(self):
        next_row = self.create_daughter_row(1, self.entry_map)
        self.put_row(next_row, [tk.Label(text=Constants.in_file), self.in_file_entry,
                                tk.Button(text="reference", command=self.open_filedialog)], 2)
        self.run_btn = tk.Button(text="  run  ", command=self.run)
        self.run_btn.grid(row=next_row + 3, column=1)
        tk.Label(textvariable=self.info).grid(row=next_row + 4, column=1)

    def menu(self, menu):
        save_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="SAVE", underline=0, menu=save_menu)
        save_menu.add_command(label='SAVE NOW SETTINGS', command=self.save_settings)

    def save_settings(self):
        var = self.get_entries()
        var[Constants.in_dir] = self.settings[Constants.in_dir]
        var[Constants.out_dir] = self.settings[Constants.out_dir]
        with open(Constants.settings_file, "w", encoding=Constants.encoding) as f:
            json.dump(var, f, indent=2, sort_keys=True, separators=(',', ': '))

    def create_daughter_row(self, start_row_num, daughter_entries):
        row_num = start_row_num
        for label1, entries in sorted(daughter_entries.items(), key=lambda x: x[0]):
            elems = list()
            elems.append(tk.Label(text=label1))
            for label2, entry in sorted(entries.items(), key=lambda x: x[0]):
                elems.append(tk.Label(text=label2))
                elems.append(entry)
            self.put_row(row_num, elems)
            row_num += 1
        return row_num

    def put_row(self, row_num, elements, from_column=1):
        for index, element in enumerate(elements):
            element.grid(row=row_num, column=index + from_column)

    def open_filedialog(self):
        filetypes = [("dec file", "*.dec")]
        initdir = (Constants.in_dir in self.settings and self.settings[Constants.in_dir]) or os.path.join("~",
                                                                                                          "Desktop")
        file = tk.filedialog.askopenfilename(filetypes=filetypes, initialdir=initdir)
        self.in_file_entry.insert(tk.END, file)

    def save_filedialog(self, in_path):
        filetypes = [("all file", "*.*")]
        initdir, initfile = self.candidate_out_path(in_path)
        return tk.filedialog.asksaveasfilename(filetypes=filetypes, initialdir=initdir, initialfile=initfile)

    def candidate_out_path(self, in_path):
        in_dir = (Constants.out_dir in self.settings and self.settings[Constants.out_dir]) or os.path.dirname(in_path)
        out_file_temp = os.path.basename(in_path).split('.')[0]
        out_file = out_file_temp + Constants.out_ext
        return in_dir, out_file

    def run(self):
        self.set_running()
        in_file = self.in_file_entry.get()
        inputs = self.get_entries()
        try:
            man = Manager(in_file, Constants.out_temp, inputs)
            man.run()
            out_file = self.save_filedialog(in_file)
            if out_file:
                os.rename(Constants.out_temp, out_file)
        except:
            self.info.set("Unexpected error:" + sys.exc_info()[0])
        self.info.set("")
        self.run_btn.configure(state=tk.NORMAL)

    def set_running(self):
        self.run_btn.configure(state=tk.DISABLED)
        self.info.set("  running...")

    def create_entry_map(self, d_list, inputs, settings):
        entry_map = {}
        for daughter in d_list:
            daughter_elem = {}
            for input in inputs:
                e = tk.Entry()
                setting = settings[daughter][input]
                e.insert(0, setting)
                daughter_elem[input] = e
            entry_map[daughter] = daughter_elem
        return entry_map

    def get_entries(self):
        var = {}
        for daughter, values in self.entry_map.items():
            daughter_elem = {}
            for input, value in values.items():
                daughter_elem[input] = value.get()
            var[daughter] = daughter_elem
        return var


if __name__ == '__main__':
    frame = Display(tk.Tk())
    frame.mainloop()
