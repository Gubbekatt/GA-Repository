import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles
from matplotlib import pyplot as plt
from numpy.ma.core import indices


def plot_score_lists(fitness_list, marker1='o', marker2='s',marker3='x'):
    working_fitness_list= list(zip(*fitness_list))
    x_values=range(len(fitness_list))
    plt.figure(figsize=(10,5))
    colors=['b','r','k']
    labels=['lowest_fitness','median_fitness','highest fitness']
    for i in range(0,len(working_fitness_list)):
        plt.plot(x_values,working_fitness_list[i],label=labels[i%len(colors)], marker='.',
                 color=colors[i%len(colors)])
    plt.xlabel('Generation')
    plt.ylabel('respective fitness values')
    plt.title("fitness graph")
    plt.legend()
    plt.grid()
    plt.show()
def plot_death(death_list):
    plt.style.use('fivethirtyeight')
    bins = [ i  for i in range(0,12000,100) ]
    plt.hist(death_list, bins=bins, edgecolor='black')

    plt.title('death_distrubution')
    plt.xlabel('frames survives')
    plt.ylabel('amount of player')

    plt.tight_layout()
    plt.show()
def plot_gene(gene_list, marker1='o'):
    gene_lines = list(zip(*gene_list))  # Transpose the list
    x_values = range(len(gene_list))  # X-axis should match the number of sublists
    colors = ['r', 'b', 'k', 'y']  # Limited colors

    for i in range(len(gene_lines)):  # Iterate over transposed lists
        plt.plot(x_values, gene_lines[i], label=f'Gene {i}',
                 linestyle='-', color=colors[i % len(colors)])  # Cycle colors

    plt.xlabel('Generation')
    plt.ylabel('Gene Value')
    plt.title("Genetic Variation Graph")
    plt.legend()
    plt.grid()
    plt.show()












# Example usage
list1 = [517, 590, 1808, 151482, 30300, 20097]
list2 = [118.06, 123.605, 197.505, 937.865, 453.47, 452.21]


