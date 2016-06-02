# -*- coding: utf-8 -*-

import pandas as pd
from oemof.network import Bus
from oemof.solph import Flow, Storage, LinearTransformer, Sink, Source


# %% new core interface

bel = Bus(label='el_balance')

bcoal = Bus(label='coalbus')

so = Source(label='coalsource', outputs={bcoal: Flow()})

wind = Source(label='wind',
              outputs={bel: Flow(actual_value=[1, 1, 2], nominal_value=2,
                                 fixed_costs=25)})
si = Sink(label='sink', inputs={bel: Flow(max=[0.1, 0.2, 0.9],
                                          nominal_value=10,
                                          fixed=True, actual_value=[1, 2, 3])})

trsf = LinearTransformer(label='trsf', inputs={bcoal: Flow()},
                         outputs={bel: Flow(nominal_value=10,
                                            fixed_costs=5,
                                            variable_costs=10,
                                            summed_max=4,
                                            summed_min=2)},
                         conversion_factors={bel: 0.4})

stor = Storage(label='stor', inputs={bel: Flow()}, outputs={bel: Flow()},
               nominal_capacity=50, inflow_conversion_factor=0.9,
               outflow_conversion_factor=0.8, initial_capacity=0.5,
               capacity_loss=0.001)

# %% approach to create objects by iterating over dataframe

nodes_flows = pd.read_csv('nodes_flows.csv', sep=',')
nodes_flows_seq = pd.read_csv('nodes_flows_seq.csv', sep=',', header=None)
nodes_flows_seq.drop(0, axis=1, inplace=True)
nodes_flows_seq = nodes_flows_seq.transpose()

for idx, row in nodes_flows.iterrows():

    # eval to be substituted due to security issues. but works for now..
    obj = eval(row['class'])
    obj_attrs = [attr for attr in dir(obj)]
    row_dc = dict(zip(row.index.values, row.values))

    # set attributes
    obj.label = row['label']

    if row['class'] == 'Source':
        obj.outputs = Bus(label=row['target'])
        print(obj.outputs, type(obj.outputs))

#    # only set attributes that exist and that have values
#    # problem: attributes (e.g. fixex, cap_loss, ...) are contained in dir(obj)
#    for attr in obj_attrs:
#        if attr in row_dc.keys() and row_dc[attr]:
#            print('Exists:', row_dc[attr])

    print(idx, obj)
