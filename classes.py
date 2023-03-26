import pandas as pd
from sqlalchemy import create_engine

''' 
SQL classes for creating and getting connections inserting the data into database is done in these classes.
This class also calculates largest deviation.
'''


class SQLClass:
    # Read csv
    def __init__(self, csv_path):
        self.dataFrames = []
        try:
            self.csv_data = pd.read_csv(csv_path)
        except FileNotFoundError:
            print("Issue while reading file {}".format(csv_path))
            raise

    def toSql(self, file_name, title):

        db_engine = create_engine('sqlite:///{}.db'.format(file_name), echo=False)

        # Using dbEngine and saving data
        csv_data = self.csv_data.copy()
        csv_data.columns = [name.capitalize() + title for name in csv_data.columns]
        csv_data.set_index(csv_data.columns[0], inplace=True)

        csv_data.to_sql(title, db_engine, if_exists="replace", index=True, )


class ParentFunction:

    def __init__(self, ideal, name):
        self._name = name
        self.ideal = ideal


class IdealFunction(ParentFunction):
    def __init__(self, ideal, train, name):
        self.train_function = train
        super().__init__(ideal, name)

    # Calculate the largest deviation between train and ideal
    def calculate_largest_deviation(self):
        deviation = self.train_function - self.ideal
        return max(deviation.abs())
