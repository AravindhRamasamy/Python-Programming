import numpy as np
from sqlalchemy import create_engine

from plotting import plot_ideal_functions, plot_test_point_based_on_ideal
from classes import SQLClass, IdealFunction

'''This Code imports the given csv data and performs the following operations:
* Using Lease square method finds the best fit ideal function.
* Iterates each test point and maps it with best ideal function based on given second criterion.
* Stores the test data along with new columns in sql table.
* visualizes the output
'''

idealCsvPath = "input/ideal.csv"
trainCsvPath = "input/train.csv"
testCsvPath = "input/test.csv"

# SQLClass accepts the csv path, reads the file and convert to dataset
# Also converts the uploaded csv file data into sql.
ideal_functions = SQLClass(csv_path=idealCsvPath)
train_datasets = SQLClass(csv_path=trainCsvPath)
test_datasets = SQLClass(csv_path=testCsvPath)

test_data = test_datasets.csv_data
test_data['ideal_function'] = ''
test_data['deviation'] = 0

ideal_functions.toSql(file_name="assignment", title="ideal")
train_datasets.toSql(file_name="assignment", title="train")

ideal_pos = {
    'x': [], 'y1': [], 'y2': [], 'y3': [], 'y4': []}


# Comparing train and ideal sets to find best fit
def find_ideal_functions(train_data, ideal_set):
    for train in train_data.columns:
        trains = []
        if train != 'x':
            for ideal in ideal_set.columns:
                if ideal != 'x':
                    # Calculating sum of squared deviations Σ (yi - yt)**2
                    deviation = ((ideal_set[ideal] - train_data[train]) ** 2).sum().sum()
                    trains.append(deviation)
            # Finding minimum value ideal for each train
            ideal_pos[train] = trains.index(min(trains)) + 1
    return ideal_pos


# Find 4 best fit ideal functions
chosen_functions = find_ideal_functions(train_datasets.csv_data, ideal_functions.csv_data)
chosen_functions['x'] = 0
best_fit = ideal_functions.csv_data.iloc[:, list(chosen_functions.values())]


# Locate ideal y for corresponding test point x
def locateY(x, ideal):
    key = ideal['x'] == x
    try:
        return ideal.loc[key].iat[0, 1]
    except IndexError:
        raise IndexError


# Find matching ideal set based on second criteria
def map_test_point(test_point, ideal):
    no_of_ideal = None
    delta = 0

    for i, ideal_set in enumerate(ideal.iloc[:, 1:5].columns):
        try:
            deviation = IdealFunction(best_fit[ideal_set], train_datasets.csv_data.iloc[:, i + 1], ideal_set)
            # Determine the largest deviation
            largest_deviation = deviation.calculate_largest_deviation()
            y_location = locateY(test_point[0], best_fit[['x', ideal_set]])
        except IndexError:
            print("Index Error")
            raise IndexError
        # Calculate deviation between test point and ideal
        deviation = abs(y_location - test_point[1])
        print('maximum deviation acceptable ' + ideal_set, largest_deviation * np.sqrt(2))
        if abs(deviation < largest_deviation * np.sqrt(2)):
            if (no_of_ideal is None) or (deviation < delta):
                no_of_ideal = ideal_set
                delta = deviation

    return no_of_ideal, delta


# iterate each test point calculate deviation and compare it with the largest deviation
for i, point in test_data.iterrows():
    ideal_function, yDelta = map_test_point([point['x'], point['y']], best_fit)
    test_data.loc[i, 'ideal_function'] = ideal_function
    test_data.loc[i, 'deviation'] = yDelta

engine = create_engine('sqlite:///assignment.db')
test_data.to_sql('test-data', con=engine, if_exists='replace', index=False)

# plot the chosen ideal functions against the training data
plot_ideal_functions(train_datasets.csv_data, best_fit)
plot_test_point_based_on_ideal(test_data, best_fit)
