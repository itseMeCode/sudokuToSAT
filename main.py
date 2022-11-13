import string
import math

nodes = string.ascii_lowercase[:16]
colors = ['1', '2', '3', '4']

row_length = math.sqrt(len(nodes))
box_length = math.sqrt((row_length))

rows = []
columns = []
boxes = []

sat_formula = ''

# create rows
current_row = 0
for node_index, node in enumerate(nodes):
    if node_index % row_length == 0:
        rows.append([])
        current_row = node_index / row_length
    rows[(int)(current_row)].append(node)

# create columns
for row_index, row in enumerate(rows):
    current_column = []
    for node_index, node in enumerate(row):
        current_column.append(rows[(int)(node_index)][(int)(row_index)])
    columns.append(current_column)

# create empty boxes
for i in range((int)(row_length)):
    boxes.append([])

# create boxes
current_box = 0
for row_index, row in enumerate(rows):
    if (row_index % box_length == 0) & (row_index != 0):
        current_box += box_length
    for column_index, column in enumerate(columns):
        if (column_index % box_length == 0) & (column_index != row_length) & (column_index != 0):
            current_box += 1
        boxes[(int)(current_box)].append(row[column_index])
        if column_index == row_length - 1:
            current_box -= box_length - 1


# give every node a color
for node_index, node in enumerate(nodes):
    sat_clause = '('
    for color_index, color in enumerate(colors):
        sat_clause += f'{node}_{color}'
        if color_index != len(colors) - 1:
            sat_clause += ' | '
    sat_clause += ')'
    sat_formula += sat_clause
    sat_formula += ' & '

# give every node only one color
for node_index, node in enumerate(nodes):
    sat_clause = '('
    for color_index, color in enumerate(colors):
        sat_clause += f'!{node}_{color}'
        if color_index != len(colors) - 1:
            sat_clause += ' | '
    sat_clause += ')'
    sat_formula += sat_clause
    sat_formula += ' & '

# add clauses for row edges
for row_index, row in enumerate(rows):
    for node_index, node in enumerate(row):
        for index in range(node_index, (int)(row_length)):
            for color in colors:
                if (node != row[index]):
                    sat_clause = f'(!{node}_{color} | !{row[index]}_{color}) & '
                    sat_formula += sat_clause

# add clauses for column edges
for column_index, column in enumerate(columns):
    for node_index, node in enumerate(column):
        for index in range(node_index, (int)(row_length)):
            for color in colors:
                if (node != column[index]):
                    sat_clause = f'(!{node}_{color} | !{column[index]}_{color}) & '
                    sat_formula += sat_clause

# add clauses for box edges
for box_index, box in enumerate(boxes):
    for node_index, node in enumerate(box):
        for index in range(node_index, (int)(row_length)):
            for color in colors:
                if (node != box[index]):
                    sat_clause = f'(!{node}_{color} | !{box[index]}_{color}) & '
                    sat_formula += sat_clause

# for sudokuXX.boole example
""" sat_formula += f'(i_1) & '
"""

# for unsat-sudokuXX.boole
""" for node in nodes:
    sat_formula += f'({node}_1) & ' """

sat_formula = sat_formula[:-2]
print(sat_formula)
