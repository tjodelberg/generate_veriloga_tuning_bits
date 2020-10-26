#!/usr/bin/python

import sys

#Get file name

try:
        x = sys.argv[1]
except:
        print ''
        print 'Error: Include file name as target'
        print ''
try:
        filename = '{}.raw'.format(x)
        f = open(filename,'r')
except:
        print ''
        print 'Error: {}.raw file not found'.format(x)
        print ''

#Open veriloga output, change sys.stdout to write to file

orig_stdout = sys.stdout
fwrite = 'veriloga.generated.va'
ff = open(fwrite,'w')
sys.stdout = ff

reg_names = [] #Array of reg names
reg_vals = []  #Array of reg vals
bit_split = [] #Used to split reg val into array

#Read io row by row in .raw file

for i,row in enumerate(f):
        a = row.split()
        if i == 0:
                module_name = a[1];
                H = a[3]
                L = a[5]
        else:   
                try:
                        reg_names.append(a[0])
                        reg_vals.append(a[1])
                except:
                        pass

f.close

                
                #Start file header

print '//Generated by generate_veriloga.py script - Trevor'
print ''
print '`include "constants.vams"'
print '`include "disciplines.vams"'
print ''

print 'module {}('.format(module_name)

for i,val in enumerate(reg_names):
        if i == len(reg_names)-1:
                print'{}'.format(val)
        else:
                print'{},'.format(val)


print ');'
print ''

for i,reg in enumerate(reg_names):
        if len(reg_vals[i]) == 1:               
                print 'output {};'.format(reg)
        else:
                print 'output [{}:0] {};'.format(len(reg_vals[i])-1,reg)

print ''

for i,reg in enumerate(reg_names):
        if len(reg_vals[i]) == 1:
                print 'electrical {};'.format(reg)
        else:
                print 'electrical [{}:0] {};'.format(len(reg_vals[i])-1,reg)

print ''
print 'analog begin'

for i,bits in enumerate(reg_vals):
        bit_split[:] = bits
        bit_split = bit_split[::-1] #Reverse it
        print ''
        for ii,bit in enumerate(bit_split):
                if bit == '1':
                        logic = H
                else:
                        logic = L
                if len(reg_vals[i]) == 1:
                        print 'V({}) <+ {};'.format(reg_names[i],logic)
                else:
                        print 'V({}[{}]) <+ {};'.format(reg_names[i],ii,logic)

print('')
print 'end'
print('')
print 'endmodule'
        




