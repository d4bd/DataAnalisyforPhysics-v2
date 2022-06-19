# DataAnalisyforPhysics-v2
The aim of this project was to create a meta-language to automate data analisys in the laboratories of a bachelor degree in physics. The idea was to reach the same complexity of the workflow in a spreadsheets.

Precisely the idea was to create a python program that would act as an interpreter for the new language. The set of instructions would have been limited, substantially we would have liked to support the possibility to add data and generate from specific functions, make calculations of arbitrary frunctions from that data, plot it and eventually make best-fits.

There implemented features are:
- Creation of a file reader that can differentiate from commands, and their arguments, and comments. The file reader will also transfomat the user friendly version of the file, with comments and spaces, to the correct file format for the execution.
Each file must have on the first line the key words "DATA ANALISY" (case sensitive).
The multiline comments can be written between "@@#" (example: @@# comment @@#), while the inline comments follows the characters "@@" (example: @@ comment).
- Cretion of a table of data with "NEWDATA" command. The command is

  NEWDATA setName valueName1 unitMeasure1 valueName2 unitMeasure2 ....
  Data
  END

  where unitMearureN is the unit measure of the values in valueNameN column. All the inputs need to be separated by spaces or tabulations.

- Possibility to print a dataset with: PRINTDATA setName
- The keywork "STARTANALISY" is used to tell to the program that all the data was passed and the analisy is starting
- Possibility to apply functions to the data with error calculation. For the error propagations is used the simplified formula for non-linear combinations (it is calculated the root square of the square of the derivatives multiplied by the varience of the variable). This was achived using SymPy. 
The syntax is:

  FUNCTION setName resultName f(valueName1, ..., valueNameN)

  where resultName is the name of the column that will be added to the set named setName and f is a function of the other data in the same set. It is not required to specify a measure unit for the outcome since the program calculates it autonomously (this feature has not yet been implemented)

- Possibility to make simple non customizable plots. The colors are set by default:

  SIMPLEPLOT setName xValueName1 yValueName2 graphTitle 

  where graphTitle can contain space. The function consider part of the title everything that is passed after the y values

The progect was then abandoned due to lack of time.
