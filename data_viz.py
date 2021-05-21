import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches
import os
from collections import defaultdict
from functools import reduce
from itertools import chain


def remove_store_files() -> None:
    # removes all 'DS_Store files'
    path = os.getcwd()
    for root, dirs, files in os.walk(path):
        for currentFile in files:
            if currentFile.startswith('.DS'):
                os.remove(os.path.join(root, currentFile))


def build_test_table(path, test_no=1) -> tuple(pd.DataFrame, pd.DataFrame):
    # build a dataframe from the frequencies of ad categories
    control_pre = 'CATEGORIES_CONTROL/'
    exp_pre = 'CATEGORIES_EXPERIMENT/'
    categories = os.listdir(path + 'CATEGORIES_CONTROL/')

    # gather counts from directories
    exp_counts = []
    control_counts = []
    for c in categories:
        exp_counts.append(len(os.listdir(path + exp_pre + c)))
        control_counts.append(len(os.listdir(path + control_pre + c)))

    # make np array
    categories = np.array(categories)
    control_counts = np.array(control_counts)
    exp_counts = np.array(exp_counts)

    # make dfs
    exp_df = pd.DataFrame({'Categories':categories,'Frequency':exp_counts}, index=categories)
    control_df = pd.DataFrame({'Categories':categories, 'Frequency':control_counts}, index=categories)

    return control_df, exp_df


def bar_chart(df, title, categories) -> None:
    # save bar chart figure
    my_colors = [(217,100,90), (245, 207, 99), (95,172,136), (81,158,214), (125,83,151), (231, 153, 94)]
    my_colors = [tuple(map(lambda x: x/255, t)) for t in my_colors]

    plt.figure(dpi=140)
    df.plot.bar(x='Categories', y='Frequency',figsize=(20,20),fontsize=20, rot=0, colors=my_colors)

    plt.ylabel('Frequency', labelpad=4.0)
    plt.legend(loc=2, prop={'size': 24, 'weight':'bold'}, frameon=True)
    plt.suptitle(title, fontsize=48)
    plt.ylabel('Frequency', fontsize=24)

    plt.savefig(title, dpi = 140)
    plt.close()

def pie_chart(df, title, categories) -> None:
    # save pie chart figure
    my_colors = [(217,100,90), (245, 207, 99), (95,172,136), (81,158,214), (125,83,151), (231, 153, 94)]
    my_colors = [tuple(map(lambda x: x/255, t)) for t in my_colors]

    df.plot.pie(y='Frequency',figsize=(20,20),fontsize=20,labels=categories,colors=my_colors, explode=explode, shadow=False, rot=45)

    plt.ylabel('Frequency', labelpad=4.0)
    plt.legend(loc=2, prop={'size': 24, 'weight':'bold'}, frameon=True)
    plt.suptitle(title, fontsize=48)
    plt.ylabel('Frequency', fontsize=24)

    plt.savefig(title, dpi = 140)
    plt.close()

def main():

    ordered_exp_data = [["Far Conservative",1],["Far Liberal", 0], ["Far Liberal",1], ["Moderate Liberal", 0], ["Far Conservative", 1], ["Moderate Conservative",0],["Moderate Liberal", 1], ["Far Liberal", 0], ["Far Conservative",1], ["Moderate Conservative", 0]]


    # all data frames for each category, from each test
    dataframes = []
    control_path = '/CATEGORIES_CONTROL/'
    exp_path = '/CATEGORIES_EXPERIMENT/'

    DF_DICT = defaultdict(list)
    AFFILIATION_DICT = defaultdict(list)

    # Build dataframes for ad frequencies for each test
    for i in range(1,6):
        path = os.getcwd() + '/observations/' + 'test' + str(i) + '/'
        remove_store_files()
        categories = os.listdir(path + control_path)
        # build dataframes for each persona
        control, exp = build_test_table(path, i)



        title_control = 'Test' + str(i) + ': '  + ordered_exp_data[(i*2) -1][0]
        title_experiment = 'Test' + str(i) + ': ' + ordered_exp_data[(i-1) * 2][0]

        # save csv
        control.to_csv('./' + title_control + '.csv')
        exp.to_csv('./' + title_experiment + '.csv')


        # save png
        bar_chart(control, title_control + '_bar', categories)
        pie_chart(control, title_control, categories)
        bar_chart(exp, title_experiment + '_bar', categories)
        pie_chart(exp, title_experiment, categories)


        DF_DICT['EXP' + str(i)].append(exp)
        DF_DICT['CON' + str(i)].append(control)

        AFFILIATION_DICT['EXP' + str(i)].append(ordered_exp_data[(i-1) * 2][0])
        AFFILIATION_DICT['CON' + str(i)].append(ordered_exp_data[(i*2) -1][0])

        cur_test = [control, exp]
        dataframes.append(cur_test)

    # Sum of all tests
    flatten_dfs = list(chain.from_iterable(dataframes))
    sum_df = d = reduce(lambda x, y: x.add(y, fill_value=0), flatten_dfs)
    bar_chart(sum_df, "Total advertising of all experiments" + '_bar', categories)
    pie_chart(sum_df, "Total advertising of all experiments" + '_bar', categories)



if __name__ == '__main__':
    main()
