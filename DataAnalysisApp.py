import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    def __init__(self, path):
        self.filePath = path
        self.df = None

    def UploadData(self):
        try:
            if self.filePath.endswith(".xlsx"):
                self.df = pd.read_excel(self.filePath)
            elif self.filePath.endswith(".csv"):
                self.df = pd.read_csv(self.filePath)
            else:
                raise ValueError("Wrong File Format. Use .csv or .xlsx")
            print("Data Loaded Successfully.")
        except Exception as e:
            print(f"Failed to load file: {e}")

    def DisplayDatasetInfo(self):
        print("\n Dataset Info:")
        print(self.df.info())
        print("\n Summary Statistics:")
        print(self.df.describe())

    def VisualizeMissingValues(self):
        print("\n Missing Values:")
        print(self.df.isnull().sum())
        sns.heatmap(self.df.isnull(), cbar=False, cmap='viridis')
        plt.title("Missing Value Map")
        plt.show()

    def PlotDistributions(self):
        numeric_cols = self.df.select_dtypes(include='number').columns
        self.df[numeric_cols].hist(bins=30, figsize=(12, 8))
        plt.tight_layout()
        plt.show()

    def CorrelationMatrix(self):
        numeric_df = self.df.select_dtypes(include='number')
        if numeric_df.shape[1] < 2:
            print("❌ Not enough numeric columns to compute correlation.")
            return
        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title("Correlation Matrix")
        plt.show()



    def DropMissingValues(self):
        before = self.df.shape
        self.df.dropna(inplace=True)
        after = self.df.shape
        print(f"Dropped missing rows. Shape: {before} ➜ {after}")

    def FillMissingValues(self, method='mean'):
        numeric_cols = self.df.select_dtypes(include='number').columns
        if method == 'mean':
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            print("Filled missing numeric values with mean.")
        elif method == 'median':
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
            print("Filled missing numeric values with median.")
        else:
            print("Unsupported fill method. Use 'mean' or 'median'.")

    def SortData(self, column, ascending=True):
        if self.df is not None:
            if column in self.df.columns:
                self.df = self.df.sort_values(by=column, ascending=ascending)
                print(f"Data sorted by '{column}' ({'ascending' if ascending else 'descending'}).")
                print(self.df.head())
            else:
                print(f"Column '{column}' not found in the dataset.")
        else:
            print("No data loaded.")

    def SaveNewData(self, output_path="cleaned_data.csv"):
        self.df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")

    def FilterRows(self, column, operator, value):
        if self.df is not None:
            try:
                if operator == '==':
                    self.df = self.df[self.df[column] == value]
                elif operator == '!=':
                    self.df = self.df[self.df[column] != value]
                elif operator == '>':
                    self.df = self.df[self.df[column] > float(value)]
                elif operator == '<':
                    self.df = self.df[self.df[column] < float(value)]
                elif operator == '>=':
                    self.df = self.df[self.df[column] >= float(value)]
                elif operator == '<=':
                    self.df = self.df[self.df[column] <= float(value)]
                else:
                    print("Unsupported operator.")
                    return
                print(f"Filter applied on column '{column}' with condition '{operator} {value}'.")
                print(self.df.head())
            except Exception as e:
                print(f"Error applying filter: {e}")
        else:
            print("No data loaded.")

    def DropColumns(self, columns):
        if self.df is not None:
            try:
                self.df.drop(columns=columns, inplace=True)
                print(f"Dropped columns: {columns}")
            except Exception as e:
                print(f"Error dropping columns: {e}")
        else:
            print("No data loaded.")

def main():
    analyze = None

    print("Welcome to DataAnalysisAPP \n")

    while True:
        print("\nChoose from 1 to 11:")
        print("1 : Upload CSV or Excel file.")
        print("2 : Display basic dataset info.")
        print("3 : Visualize missing values.")
        print("4 : Plot distributions and correlations.")
        print("5 : Drop missing values.")
        print("6 : Fill missing values.")
        print("7 : Save cleaned data.")
        print("8 : Sort data by column.")
        print("9 : Filter rows by condition.")
        print("10 : Drop columns.")
        print("11 : Exit.")

        choice = input("\nEnter your choice: ")

        if choice not in [str(i) for i in range(1, 12)]:
            print("Invalid choice. Please enter a number from 1 to 11.")
            continue

        if choice == '1':
            path = input("Enter file path (.csv or .xlsx): ")
            analyze = DataAnalysis(path)
            analyze.UploadData()

        elif choice == '2':
            if analyze and analyze.df is not None:
                analyze.DisplayDatasetInfo()
            else:
                print("Load data first.")

        elif choice == '3':
            if analyze and analyze.df is not None:
                analyze.VisualizeMissingValues()
            else:
                print("Load data first.")

        elif choice == '4':
            if analyze and analyze.df is not None:
                analyze.PlotDistributions()
                analyze.CorrelationMatrix()
            else:
                print("Load data first.")

        elif choice == '5':
            if analyze and analyze.df is not None:
                analyze.DropMissingValues()
            else:
                print("Load data first.")

        elif choice == '6':
            if analyze and analyze.df is not None:
                method = input("Choose method (mean/median): ").lower()
                analyze.FillMissingValues(method)
            else:
                print("Load data first.")

        elif choice == '7':
            if analyze and analyze.df is not None:
                file_name = input("Enter filename to save (default: cleaned_data.csv): ").strip()
                if file_name == "":
                    file_name = "cleaned_data.csv"
                analyze.SaveNewData(file_name)
            else:
                print("Load data first.")

        elif choice == '8':
            if analyze and analyze.df is not None:
                print(f"Available columns: {list(analyze.df.columns)}")
                col = input("Enter column to sort by: ")
                order = input("Sort ascending? (yes/no): ").lower()
                ascending = order in ['yes', 'y']
                analyze.SortData(col, ascending)
            else:
                print("Load data first.")

        elif choice == '9':
            if analyze and analyze.df is not None:
                print(f"Available columns: {list(analyze.df.columns)}")
                column = input("Column to filter: ")
                operator = input("Operator (==, !=, >, <, >=, <=): ")
                value = input("Value to compare: ")
                analyze.FilterRows(column, operator, value)
            else:
                print("Load data first.")

        elif choice == '10':
            if analyze and analyze.df is not None:
                print(f"Available columns: {list(analyze.df.columns)}")
                cols = input("Enter columns to drop (comma-separated): ")
                columns_to_drop = [col.strip() for col in cols.split(',')]
                analyze.DropColumns(columns_to_drop)
            else:
                print("Load data first.")

        elif choice == '11':
            print("End Of Program.")
            break

if __name__ == "__main__":
    main()