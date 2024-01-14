import tkinter as tk
from tkinter import filedialog
import statistics
import math

class StatisticCalculator:
    def __init__(self, data, column_name):
        self.data = data
        self.column_name = column_name

    def get_column_data(self):
        # Get the column index based on the header
        header = self.data[0]
        try:
            column_index = header.index(self.column_name)
            column_data = [float(row[column_index]) for row in self.data[1:]]
            return column_data
        except ValueError:
            print(f"Column '{self.column_name}' not found.")
            return []

    def mean(self):
        return sum(self.get_column_data()) / len(self.get_column_data())

    def calculate_variance(self):
        column_data = self.get_column_data()
        n = len(column_data)
        mean = sum(column_data) / n
        squared_diff = [(x - mean) ** 2 for x in column_data]
        variance = sum(squared_diff) / n
        return variance

    def calculate_standard_deviation(self):
        variance = self.calculate_variance()
        standard_deviation = math.sqrt(variance)
        return standard_deviation

    def calculate_mode(self):
        try:
            column_data = self.get_column_data()
            mode = statistics.mode(column_data)
            return mode
        except statistics.StatisticsError:
            return None

    def get_min_max_indices(self):
        column_data = self.get_column_data()
        min_index = column_data.index(min(column_data))
        max_index = column_data.index(max(column_data))
        return min_index, max_index

    def get_min_max_info(self):
        min_index, max_index = self.get_min_max_indices()
        header = self.data[0]
        name_index = header.index("name")
        id_index = header.index("id")

        min_info = (self.data[min_index + 1][name_index], self.data[min_index + 1][id_index])
        max_info = (self.data[max_index + 1][name_index], self.data[max_index + 1][id_index])

        return min_info, max_info

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Statistics Calculator")

        self.filename_label = tk.Label(self.master, text="Select TXT file:")
        self.filename_label.pack()

        self.filename_var = tk.StringVar()
        self.filename_entry = tk.Entry(self.master, textvariable=self.filename_var)
        self.filename_entry.pack()

        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.column_label = tk.Label(self.master, text="Enter Column Name:")
        self.column_label.pack()

        self.column_var = tk.StringVar()
        self.column_entry = tk.Entry(self.master, textvariable=self.column_var)
        self.column_entry.pack()

        self.calculate_button = tk.Button(self.master, text="Calculate", command=self.calculate_statistics)
        self.calculate_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")])
        self.filename_var.set(file_path)

    def calculate_statistics(self):
        filename = self.filename_var.get()
        column_name = self.column_var.get()

        if filename and column_name:
            data = self.read_data_from_file(filename)
            calculator = StatisticCalculator(data, column_name)

            # List of statistics to calculate
            statistics_to_calculate = [
                ("Mean", calculator.mean),
                ("Variance", calculator.calculate_variance),
                ("Standard Deviation", calculator.calculate_standard_deviation),
                ("Mode", calculator.calculate_mode)
            ]

            # Display results
            result_text = ""
            for stat_name, stat_method in statistics_to_calculate:
                result_text += f"{stat_name}: {stat_method()}\n"

            min_info, max_info = calculator.get_min_max_info()
            result_text += f"Min: {min_info[0]} (ID: {min_info[1]})\n"
            result_text += f"Max: {max_info[0]} (ID: {max_info[1]})"

            result_label = tk.Label(self.master, text=result_text)
            result_label.pack()

            # Add a list or tuple of statistics for further use
            calculated_statistics = [stat_method() for stat_name, stat_method in statistics_to_calculate]
            print("Calculated Statistics:", calculated_statistics)

    def read_data_from_file(self, filename):
        with open(filename, 'r') as file:
            data = [line.strip().split(',') for line in file]
        return data

root = tk.Tk()
app = CalculatorApp(root)
root.mainloop()





