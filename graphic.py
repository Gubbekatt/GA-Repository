from matplotlib import pyplot as plt

def plot_score_lists(fitness_list, marker1='o', marker2='s',marker3='x'):

    #Plottar fram en graf som visar alla fittnes värden
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
     #Plottar fram var alla dog på den sista generationen

    plt.style.use('fivethirtyeight')
    bins = [ i  for i in range(0,12000,100) ]
    plt.hist(death_list, bins=bins, edgecolor='black')

    plt.title('death_distrubution')
    plt.xlabel('frames survives')
    plt.ylabel('amount of player')

    plt.tight_layout()
    plt.show()

def plot_gene(gene_list, marker1='o'):
    #Plottar den genetiska variationen över generationernas gång, samt för alla vikter

    gene_lines = list(zip(*gene_list))  # Transpose the list
    x_values = range(len(gene_list))  # X-axis should match the number of sublists
    colors = ['r', 'b', 'k', 'y',
              'orange', 'deeppink', 'limegreen', 'dodgerblue',
              'gold', 'mediumvioletred', 'turquoise',
              'slateblue', 'orangered', 'darkcyan']

    for i in range(len(gene_lines)):  # Iterate over transposed lists
        plt.plot(x_values, gene_lines[i], label=f'Gene {i}',
                 linestyle='-', color=colors[i % len(colors)])  # Cycle colors

    plt.xlabel('Generation')
    plt.ylabel('Gene Value')
    plt.title("Genetic Variation Graph")
    plt.legend()
    plt.grid()
    plt.show()

def plot_mean(mean_list,marker1='o'):
    #Plottar fram den gentiska medelvärdet för samtliga vikter över generationernas gång

    gene_list=list(zip(*mean_list))
    x_values=range(len(mean_list))
    colors = ['r', 'b', 'k', 'y',
              'orange', 'deeppink', 'limegreen', 'dodgerblue',
              'gold', 'mediumvioletred', 'turquoise',
              'slateblue', 'orangered', 'darkcyan']

    for i in range(len(gene_list)):  # Iterate over transposed lists
        plt.plot(x_values, gene_list[i], label=f'Gene {i}',
                 linestyle='-', color=colors[i % len(colors)])  # Cycle colors

    plt.xlabel('Generation')
    plt.ylabel('Gene Value')
    plt.title("Genetic mean Graph")
    plt.legend()
    plt.grid()
    plt.show()
