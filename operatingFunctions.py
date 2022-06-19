"""
File: operatingFunctions.py
Author: d4bd
Definitions of the functions invoked by the key words of the metalanguage
"""

from dataList import DList
from dataSet import DSet
from sympy import *
import numpy
import math
import genericFunctions
from sympy.parsing.sympy_parser import parse_expr
import re

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import sys

def operation(file):
    i=0
    #cicle over eery line of the file and execute the correspective command: each command must be the first word of a line
    while i < len(file):
        line = file[i].split()
        if line[0] in functionDict: 
            functionDict[line[0]](line[1:])
            i+=1
        elif line[0] == 'NEWDATA':
            for j in range(i,len(file)): #passes to the command everything between the command and END
                newLine = file[j].split()
                if newLine[0] == 'END':
                    data = file[i:j]
                    newData(data)
                    i=j+1
                    break
        elif line[0] == 'PLOT':
            for j in range(i,len(file)): #passes to the command everything between the command and END
                newLine = file[j].split()
                if newLine[0] == 'END':
                    info = file[i:j]
                    newPlot(info)
                    i=j+1
                    break
        elif line[0] == 'PLOTHISTO':
            for j in range(i,len(file)): #passes to the command everything between the command and END
                newLine = file[j].split()
                if newLine[0] == 'END':
                    info = file[i:j]
                    plotHisto(info)
                    i=j+1
                    break
        else:
            i+=1

def newData(data):
    names = data[0].split() #create a list conteinig all the value informations: name of the set and of the list with the associated unit
    num = len(data[1:])
    if names[1] == '-noerr': #creation list of data without errors, all equal to 0
        if names[2] not in dataSet_dict: #creation of the DSEt if not already existing
            dataSet_dict[names[2]] = DSet(names[2],num)
        dataSet = dataSet_dict[names[2]]
        lenght = dataSet_dict[names[2]]._lenght
        if lenght == num: #DLIsts in the same DSet must have same list lenght
            for i in range(0,len(names[3:]),2): #Create the various DList
                if names[i+3] not in dataSet._set: #check if this DList already exists
                    if names[i+4] == '#': #checks to see if the DList as no unit of measurement
                        dataSet._set[names[i+3]] = DList(names[i+3])
                    else:
                        dataSet._set[names[i+3]] = DList(names[i+3], names[i+4])
                    dataSet._set[names[i+3]]._valueList = np.zeros(lenght) #creates the arrey for conteining the values
                    dataSet._set[names[i+3]]._errorList = np.zeros(lenght) #creates the arrey for conteining the errors
                else:
                    sys.exit("ERROR: Trying to add data to and alrady existing list. Put the data referring to the same physical quantity in the same NEWDATA scope")
            for i in range(lenght): #fills the varius DList arrays with the value passed by the user
                value = data[i+1].split()
                j = 0
                for name in names[3::2]: #cicles over the names of the passed DList
                    if j < len(value): #to avoid acces out of range if some data is not specified
                        dataSet._set[name]._valueList[i] = value[j]
                    else:
                        print('ATTENTION: In the NEWDATA command relative to the set ', dataSet._name, ' in line ', i+1, ' of ', name, ' a value missis;  this value and his error will be set to zero.' )
                    j += 1
        else:
            sys.exit('ERROR: Trying to add list of datas with different lenght in the same set')
    else: #creation list of data with errors
        if names[1] not in dataSet_dict: #creation of the DSEt if not already existing
            dataSet_dict[names[1]] = DSet(names[1],num)
        dataSet = dataSet_dict[names[1]]
        lenght = dataSet_dict[names[1]]._lenght
        if lenght == num: #DLIsts in the same DSet must have same list lenght
            for i in range(0,len(names[2:]),2): #Create the various DList
                if names[i+2] not in dataSet._set: #check if this DList already exists
                    if names[i+3] == '#': #checks to see if the DList as no unit of measurement
                        dataSet._set[names[i+2]] = DList(names[i+2])
                    else:
                        dataSet._set[names[i+2]] = DList(names[i+2], names[i+3])
                    dataSet._set[names[i+2]]._valueList = np.zeros(lenght) #creates the arrey for conteining the values
                    dataSet._set[names[i+2]]._errorList = np.zeros(lenght) #creates the arrey for conteining the errors
                else:
                    sys.exit("ERROR: Trying to add data to and alrady existing list. Put the data referring to the same physical quantity in the same NEWDATA scope")
            for i in range(lenght): #fills the varius DList arrays with the value passed by the user
                value = data[i+1].split()
                j = 0
                for name in names[2::2]: #cicles over the names of the passed DList
                    if j < len(value): #to avoid acces out of range if some data is not specified
                        if value[j+1] == '#': #checks if the values as error  = 0
                            dataSet._set[name]._valueList[i] = value[j]
                        else:
                            dataSet._set[name]._valueList[i] = value[j]
                            dataSet._set[name]._errorList[i] = value[j+1]
                    else:
                        print('ATTENTION: In the NEWDATA command relative to the set ', dataSet._name, ' in line ', i+1, ' of ', name, ' a value missis; this value and his error will be set to zero.' )
                    j += 2
        else:
            sys.exit('ERROR: Trying to add list of datas with different lenght in the same set')

def randomData(name): #creating of an array of num random numbers whitouth errors between 0 and max
    if name[0] not in dataSet_dict: #creation of the DSEt if not already existing
        dataSet_dict[name[0]] = DSet(name[0],int(name[2]))
    dataSet = dataSet_dict[name[0]]
    lenght = dataSet_dict[name[0]]._lenght
    if name[1] not in dataSet._set: #check if this DList already exists
        dataSet._set[name[1]] = DList(name[1])
        dataSet._set[name[1]]._valueList = np.random.randint(int(name[3])+1,size=lenght) #creates the arrey for conteining the values
        dataSet._set[name[1]]._errorList = np.zeros(lenght) #creates the arrey for conteining the errors
    else:
        sys.exit("ERROR: Trying to add data to and alrady existing list. Put the data referring to the same physical quantity in the same NEWDATA scope")

def printData(set):
    dataSet = dataSet_dict[set[0]] #selects the DSet
    if len(set) == 1: #if only the DSet is specified prints all the DSet
        for i in dataSet._set: #prints the value name and error name
            print(dataSet._set[i]._name, ' ', dataSet._set[i]._unit, '\t\u03C3Err(', dataSet._set[i]._name, ')', end = '\t')
        print()
        for n in range(len(list(dataSet._set.values())[0]._valueList)): #print the values and errors
            for i in dataSet._set:
                print(dataSet._set[i]._valueList[n], '\t', dataSet._set[i]._errorList[n], end = '\t')
            print()
        print()
    else: #prints only the specified DList
        for i in set[1:]: #prints the value name and error name
            print(dataSet._set[i]._name, ' ', dataSet._set[i]._unit, '\t\u03C3Err(', dataSet._set[i]._name, ')', end = '\t')
        print()
        for n in range(len(list(dataSet._set.values())[0]._valueList)): #print the values and errors
            for i in set[1:]:
                print(dataSet._set[i]._valueList[n], '\t', dataSet._set[i]._errorList[n], end = '\t')
            print()
        print()

def function(expr):
    if analisy[0]: #cals the startanalisy funtcion it had never had been callen to instantiate the variables.
        startAnalisy(0)
        analisy[0] = False
    #select the correct data set
    dataSet = dataSet_dict[expr[0]]  #set the DSet of reference
    num = dataSet._lenght 
    #create a new DList to contain the new calculated value
    if expr[2] == '#': #checks if the unit of measure is defined
        newDList = DList(expr[1])
    else:
        newDList = DList(expr[1],expr[2])
    newDList._valueList = np.zeros(num) #creates the array for the values
    newDList._errorList = np.zeros(num) #creates the array fot the errors
    Symbol(expr[1]+'_s') #creates the variable for this new physical quantity
    #collect the math function
    expr = expr[3:] 
    expr = " ".join(expr)
    #define two list to contain the variables in wich the calculation will be made
    variable = []
    errVariable = []
    #creates the mathematical expression for the derivates -> this formula is the differential formula for error propagation
    for i in dataSet._set:
        if i in expr:
            expr = re.sub(i,i+'_s',expr) #changes the variable in the function to match the names assigned to them by the startvariable function
            variable.append(i+'_s') #add varibles to the correspective list
            errVariable.append(i+'_s')
            errVariable.append(i+'_s'+ '_error')
    expr1 = 'sqrt('
    for n in variable: #creates the formula for the error propagation
        expr1 = expr1 + '((' + str(diff(expr, n)) + ')' + '*(' + str(n) + '_error)**2)' + ' + '
    expr1 = ' '.join(expr1.split(' ')[:-2]) + ')'
    #creates the solvable expressions for sympy using numpy   
    variable_dict = {}
    errVariable_dict = {}
    func = parse_expr(expr) #parse the custom function expression
    func1 = parse_expr(expr1) #parse the function for the error propagation
    for j in range(num):
        for i in variable: #cicles to create the dictionari in which at each variable is associated his value
            variable_dict[i] = dataSet._set[i.split('_')[0]]._valueList[j]
        for i in errVariable: #cicles to create the dictionari in which at each variable is associated his value
            if '_error' not in i:
                errVariable_dict[i] = dataSet._set[i.split('_')[0]]._valueList[j]
            else: 
                errVariable_dict[i] = dataSet._set[i.split('_')[0]]._errorList[j]
        newDList._valueList[j] = func.evalf(subs=variable_dict) #evalute the funciton
        newDList._errorList[j] = func1.evalf(subs=errVariable_dict) #evalute the error for the function
    dataSet._set[newDList._name] = newDList #adds the new DList to the DSet

def startAnalisy(null):
    for i in dataSet_dict:
        for j in dataSet_dict[i]._set:
            Symbol(dataSet_dict[i]._set[j]._name +'_s') #creates the variable adding an _s to the end
       
       #need to add sorting of data before plotting with argsort from numpy
def newPlot(info):
    if info[0].split()[1] == '-show': #If the -show flag
        dataSet = dataSet_dict[info[0].split()[2]] #set the DSet of reference
    else:
        dataSet = dataSet_dict[info[0].split()[1]] #set the DSet of reference
    title = info[1] #set graph title
    title1 = ''.join(info[1].split()) #creates the name which will be use to save the graph
    #creates the x-axis
    #creates the x-axis name
    if dataSet._set[info[2].split()[1]]._unit == '': #checks to see if the DList as no unit of measurement
        xname = info[2].split()[0]
    else:
        xname = info[2].split()[0] + ' (' + dataSet._set[info[2].split()[1]]._unit + ')'
    x = dataSet._set[info[2].split()[1]]._valueList #gets x-axis values
    #create y-axis 
    #crate y-axis name
    if dataSet._set[info[3].split()[2]]._unit == '': #checks to see if the DList as no unit of measurement
        yname = info[3].split()[0]
    else:
        yname = info[3].split()[0] + ' (' + dataSet._set[info[3].split()[2]]._unit + ')'
    ylabel = info[3].split()[1] #create y-axis label for this set of data
    y = dataSet._set[info[3].split()[2]]._valueList #gets y-axis values
    
    #array sorting before plotting (the sort is based on the xvalues)
    inds = x.argsort()
    x = x[inds] #sort x
    y = y[inds] #sort y

    #plotting
    plt.figure()
    plt.plot(x,y,label=ylabel, linestyle='-', marker='o')
    plt.title(title)
    plt.xlabel(xname)
    plt.ylabel(yname)
    for i in range(len(info[4:])): #checks if the function is not just the standatd -> if more commands need to be executed
        if info[4+i].split()[0] == 'FUNCTION': #check if the user whant a functin to be plotted
            expr = ''.join(info[4+i].split()[2:]) #create function expression
            expr = re.sub(info[2].split()[1],info[2].split()[1]+'_s',expr) #substitute the variable 
            func = lambdify(info[2].split()[1]+'_s', expr, "numpy") #cretes the function
            y1 = func(x) #evaluate the function
            ylabel1 = info[4+i].split()[1]
            plt.plot(x,y1,label=ylabel1)
        else:
            if dataSet._set[info[4+i].split()[1]]._unit == dataSet._set[info[3].split()[2]]._unit: #checks if the unit of measure is the same for the two yvalues
                ylabel1 = info[4+i].split()[0]
                y1 = dataSet._set[info[4+i].split()[1]]._valueList
                y1 = y1[inds] #sort the y1 values 
                plt.plot(x,y1,label=ylabel1)
            else:
                print("Can't plot ", dataSet._set[info[3].split()[2]]._name, " with ", dataSet._set[info[4+i].split()[1]]._name, " because don't have the same unit of measurement")
    plt.grid()
    plt.legend()
    plt.savefig(title1, dpi=100)
    if info[0].split()[1] == '-show': #If the -show flag his activated plt.show() it's executed
        plt.show()
    plt.close()

def plotHisto(info):
    norm=True
    #check if the user gaved a userdefined ylabel
    try: 
        info[2].split()[2]
    except:
        ylabel = 'Probability'
    else: 
        ylabel = info[2].split()[2]

    if info[0].split()[1] == '-show': #If the -show flag
        dataSet = dataSet_dict[info[0].split()[2]] #set the DSet of reference
    else:
        dataSet = dataSet_dict[info[0].split()[1]] #set the DSet of reference   
    title = info[1] #set graph title
    title1 = ''.join(info[1].split()) #creates the name which will be use to save the graph
    if dataSet._set[info[2].split()[0]]._unit == '': #checks to see if the DList as no unit of measurement
        xname = info[2].split()[0]
    else:
        xname = info[2].split()[0] + ' (' + dataSet._set[info[2].split()[0]]._unit + ')'
    x = dataSet._set[info[2].split()[0]]._valueList #gets x-axis values
    plt.hist(x, density=norm, bins=int(info[2].split()[1]))
    plt.title(title)
    plt.xlabel(xname)
    plt.ylabel(ylabel)
    plt.savefig(title1, dpi=100)
    if info[0].split()[1] == '-show': #If the -show flag his activated plt.show() it's executed
        plt.show()
    plt.close()

#creation of the dictionari that will contain all the dataSet
dataSet_dict = {} #dictionary containing all the DSet
analisy = [True]  #awful way to have a global variable to check if the varaibles have alrady been instantitated

functionDict = {'PRINTDATA': printData, 'FUNCTION': function, 'RANDOMDATA': randomData} #dictionary of all the exacutable functions
colorDict = {'red': '#000000'}