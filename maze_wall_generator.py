# x and y positions would be table[y][x]
from random import choice

width = 35
height = 25
starting_row = 13 - 1
starting_column = 0
ending_row = starting_row
ending_column = width - 1

def create_table(width,height):
    table = []
    sub_table = []
    for i in range(height):
        for i in range(width):
            sub_table.append(1)
        table.append(sub_table)
        sub_table = []
    return table


def move_right(table,row,column):
    table = table
    column += 1
    table[row][column] = 0
    return table, row, column
def move_left(table,row,column):
    table = table
    column -= 1
    table[row][column] = 0
    return table, row, column
def move_up(table,row,column):
    table = table
    row -= 1
    table[row][column] = 0
    return table, row, column
def move_down(table,row,column):
    table = table
    row += 1
    table[row][column] = 0
    return table, row, column

def clear_starting_zone(table):
    table = table
    for i in range(1,3):
        table[starting_row][starting_column + i] = 0
        table[starting_row + i][starting_column] = 0
        table[starting_row - i][starting_column] = 0
    table[starting_row + 1][starting_column + 1] = 0
    table[starting_row + 1][starting_column + 2] = 0
    table[starting_row + 2][starting_column + 1] = 0
    table[starting_row + 2][starting_column + 2] = 0
    table[starting_row - 1][starting_column + 1] = 0
    table[starting_row - 1][starting_column + 2] = 0
    table[starting_row - 2][starting_column + 1] = 0
    table[starting_row - 2][starting_column + 2] = 0 
    return table

def create_map():
    '''
    table = starting_table
    column = starting_column
    row = starting_row
    table[starting_row][starting_column] = 2
    '''
    ################
    '''
    for i in range(500):
        direction = choice(['left', 'right', 'up', 'down'])
        if direction == 'left' and column != 0:
            table, row, column = move_left(table,row,column)
        elif direction == 'right' and column != width - 1:
            table, row, column = move_right(table,row,column)
        elif direction == 'down' and row != height - 1:
            table, row, column = move_down(table,row,column)
        elif direction == 'up' and row != 0:
            table, row, column = move_up(table,row,column)    
    '''
    # MAKE SURE THIS NUMBER_OF_ONES THING WORKS ALL THE TIME BECAUSE IT DOESN'T SEEM TO
    number_of_ones = 0
    while number_of_ones < 200 or number_of_ones > 600:
        table = create_table(width,height)
        column = starting_column
        row = starting_row
        table[starting_row][starting_column] = 2
        while table[ending_row][ending_column] != 0:
            direction = choice(['left', 'right', 'up', 'down'])
            if direction == 'left' and column != 0:
                table, row, column = move_left(table,row,column)
            elif direction == 'right' and column != width - 1:
                table, row, column = move_right(table,row,column)
            elif direction == 'down' and row != height - 1:
                table, row, column = move_down(table,row,column)
            elif direction == 'up' and row != 0:
                table, row, column = move_up(table,row,column) 
        table = clear_starting_zone(table)
        number_of_ones = 0
        for item in table:
            for number in item:
                if number == 1:
                    number_of_ones += 1
        
    #print(number_of_ones)
    return table, number_of_ones


'''
table = create_map()

for item in table:
    print(item)
'''
# Starting position is 13x0 for the grid you have right now