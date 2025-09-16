"""
A simple command-line spreadsheet program that aims to be more user-friendly and capable than
traditional spreadsheets. It provides a menu driven interface for performing common
spreadsheet tasks such as loading data, viewing and editing cells, calculating
aggregates, filtering rows and generating charts.

The program is built on top of pandas and matplotlib, which means it can scale
beyond the limits of conventional spreadsheets and perform computations on
larger data sets. It also allows users to build charts directly from the data
with a single command. This script is intended as an illustrative example
rather than a fully fledged replacement for tools like Excel or Google Sheets.

Usage:
    python excel_like_program.py

The program will display a menu of options. Users can load a CSV file, create
a new blank sheet, add rows or columns, compute sums and averages, filter rows
by conditions, plot data, and save changes back to a file.
"""

import os
import sys
from typing import List, Optional

try:
    import pandas as pd
except ImportError:
    print("This program requires the pandas library. Please install it via 'pip install pandas'.")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("This program requires the matplotlib library. Please install it via 'pip install matplotlib'.")
    sys.exit(1)


class Spreadsheet:
    """A simple spreadsheet class wrapping a pandas DataFrame."""

    def __init__(self, df: Optional[pd.DataFrame] = None):
        self.df = df if df is not None else pd.DataFrame()

    def load_csv(self, path: str) -> None:
        """Load data from a CSV file into the spreadsheet."""
        try:
            self.df = pd.read_csv(path)
            print(f"Loaded data with {len(self.df)} rows and {len(self.df.columns)} columns.")
        except FileNotFoundError:
            print(f"Error: File '{path}' not found.")
        except pd.errors.EmptyDataError:
            print("Error: The CSV file is empty.")
        except Exception as exc:
            print(f"Failed to load CSV: {exc}")

    def save_csv(self, path: str) -> None:
        """Save the current spreadsheet to a CSV file."""
        try:
            self.df.to_csv(path, index=False)
            print(f"Saved data to '{path}'.")
        except Exception as exc:
            print(f"Failed to save CSV: {exc}")

    def view(self, n: int = 5) -> None:
        """Display the top n rows of the spreadsheet."""
        if self.df.empty:
            print("The spreadsheet is empty.")
            return
        print(self.df.head(n))

    def add_row(self, values: List[str]) -> None:
        """Add a new row to the spreadsheet. Values should match number of columns."""
        if not self.df.empty and len(values) != len(self.df.columns):
            print(f"Error: Expected {len(self.df.columns)} values but got {len(values)}.")
            return
        if self.df.empty:
            # create column names if the sheet is empty
            self.df = pd.DataFrame([values])
        else:
            self.df.loc[len(self.df)] = values
        print("Row added.")

    def add_column(self, name: str, values: List[str]) -> None:
        """Add a new column to the spreadsheet."""
        if not self.df.empty and len(values) != len(self.df):
            print(f"Error: Expected {len(self.df)} values but got {len(values)}.")
            return
        self.df[name] = values
        print(f"Column '{name}' added.")

    def sum_column(self, col: str) -> None:
        """Calculate and print the sum of a column."""
        if col not in self.df.columns:
            print(f"Column '{col}' does not exist.")
            return
        try:
            total = pd.to_numeric(self.df[col], errors='coerce').sum()
            print(f"Sum of '{col}': {total}")
        except Exception as exc:
            print(f"Failed to compute sum: {exc}")

    def average_column(self, col: str) -> None:
        """Calculate and print the average of a column."""
        if col not in self.df.columns:
            print(f"Column '{col}' does not exist.")
            return
        try:
            avg = pd.to_numeric(self.df[col], errors='coerce').mean()
            print(f"Average of '{col}': {avg}")
        except Exception as exc:
            print(f"Failed to compute average: {exc}")

    def filter_rows(self, col: str, value: str) -> None:
        """Display rows where the column equals the specified value."""
        if col not in self.df.columns:
            print(f"Column '{col}' does not exist.")
            return
        filtered = self.df[self.df[col].astype(str) == value]
        if filtered.empty:
            print(f"No rows found where {col} == {value}.")
        else:
            print(filtered)

    def plot(self, x_col: str, y_col: str, kind: str = 'line') -> None:
        """Generate a simple chart using two columns."""
        if x_col not in self.df.columns or y_col not in self.df.columns:
            print("Error: one or both columns do not exist.")
            return
        try:
            x = pd.to_numeric(self.df[x_col], errors='coerce') if kind in ('line', 'bar') else self.df[x_col]
            y = pd.to_numeric(self.df[y_col], errors='coerce')
            plt.figure()
            if kind == 'line':
                plt.plot(x, y)
            elif kind == 'bar':
                plt.bar(x, y)
            else:
                print("Unsupported chart type. Use 'line' or 'bar'.")
                return
            plt.title(f"{kind.title()} plot of {y_col} vs {x_col}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.show()
        except Exception as exc:
            print(f"Failed to generate plot: {exc}")


def display_menu() -> None:
    """Print the list of available commands."""
    print("\n--- Simple Spreadsheet Menu ---")
    print("1. Load CSV")
    print("2. Save CSV")
    print("3. View top rows")
    print("4. Add row")
    print("5. Add column")
    print("6. Sum column")
    print("7. Average column")
    print("8. Filter rows by value")
    print("9. Plot columns")
    print("0. Exit")


def main() -> None:
    sheet = Spreadsheet()
    while True:
        display_menu()
        choice = input("Select an option (0-9): ").strip()
        if choice == '1':
            path = input("Enter path to CSV file: ").strip()
            sheet.load_csv(path)
        elif choice == '2':
            path = input("Enter path to save CSV: ").strip()
            sheet.save_csv(path)
        elif choice == '3':
            try:
                n = int(input("Enter number of rows to view (default 5): ") or '5')
            except ValueError:
                n = 5
            sheet.view(n)
        elif choice == '4':
            if sheet.df.empty:
                cols = int(input("Sheet is empty. How many columns in new row? "))
                values = [input(f"Value for column {i+1}: ") for i in range(cols)]
            else:
                values = [input(f"Value for '{col}': ") for col in sheet.df.columns]
            sheet.add_row(values)
        elif choice == '5':
            name = input("Enter new column name: ")
            if sheet.df.empty:
                count = int(input("Sheet is empty. How many rows for this column? "))
                values = [input(f"Row {i+1} value: ") for i in range(count)]
            else:
                values = [input(f"Value for row {i+1}: ") for i in range(len(sheet.df))]
            sheet.add_column(name, values)
        elif choice == '6':
            col = input("Enter column name to sum: ")
            sheet.sum_column(col)
        elif choice == '7':
            col = input("Enter column name to average: ")
            sheet.average_column(col)
        elif choice == '8':
            col = input("Enter column name: ")
            val = input("Enter value to filter by: ")
            sheet.filter_rows(col, val)
        elif choice == '9':
            x_col = input("Enter x-axis column: ")
            y_col = input("Enter y-axis column: ")
            kind = input("Chart type (line/bar): ").strip().lower() or 'line'
            sheet.plot(x_col, y_col, kind)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose again.")


if __name__ == '__main__':
    main()
