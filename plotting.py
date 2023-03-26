from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.models import Band, ColumnDataSource
import pandas as pd

'''
Here we have created the functions to visualize the datas using bokeh.
'''


def plot_ideal_functions(train_set, ideal_set):
    plots = []
    for i in range(1, 5):
        data_points = create_graph_chosen_ideal(ideal_set, train_set, i)
        plots.append(data_points)
    output_file("output/{}.html".format("plot_ideal_set"))
    # Shows the generated graph with file
    show(column(*plots))


def create_graph_chosen_ideal(ideal, train, index):
    # This function creates graph based on two data
    x_value = ideal['x']
    # ideal data and names
    ideal_data = ideal.iloc[:, index]
    ideal_name = ideal.columns[index]

    # train data and names
    train_data = train.iloc[:, index]
    train_name = train.columns[index]

    plot = figure(title="Graph for train {} vs ideal {}.".format(ideal_name, train_name),
                  x_axis_label='x', y_axis_label='y')
    plot.scatter(x_value, ideal_data, fill_color="red", legend_label="Train")
    plot.line(x_value, train_data, legend_label="Ideal", line_width=5)
    return plot


def plot_test_point_based_on_ideal(points, ideal):
    # this function creates plotting points based on Ideal functions and saves in html file
    plots = []
    for item in points.itertuples(index=True, name='Pandas'):
        if item.ideal_function is not None:
            p = plot_graph(item, ideal)
            plots.append(p)
    output_file("output/{}.html".format("plot_test_point_based_on_ideal"))
    show(column(*plots))


def plot_graph(point, ideal):
    if point.ideal_function is not None:
        # Get points of Y based on X
        point_string = "({},{})".format(point.x, round(point.y, 2))
        title = "point: {} with ideal: {}".format(point_string, point.ideal_function)

        graph_plot = figure(title=title, x_axis_label='x', y_axis_label='y')

        # draw lines from ideal data
        graph_plot.line(ideal.x, ideal[point.ideal_function],
                        legend_label="ideal point", line_width=2, line_color='black')

        # This one shows the deviations for the ideal function in the graph
        plot_data = pd.DataFrame()
        plot_data['y'] = ideal[point.ideal_function]
        plot_data['x'] = ideal['x']
        test_point_deviation = point.deviation
        plot_data['upper'] = ideal[point.ideal_function] + test_point_deviation
        plot_data['lower'] = ideal[point.ideal_function] - test_point_deviation

        data_src = ColumnDataSource(plot_data.reset_index())

        band = Band(base='x', lower='lower', upper='upper', source=data_src, level='underlay',
                    fill_alpha=0.5, line_width=4, line_color='blue', fill_color="blue")

        graph_plot.add_layout(band)
        graph_plot.scatter([point.x], [round(point.y, 4)], fill_color="red", legend_label="Test points",
                           size=8)

        return graph_plot
