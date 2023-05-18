#comments are used by using # symbol at the beginning 
a, b = 17, 3.0 # variables must be defined before being used 

division = a / b #simple calculations
floordivision = a // b
remainder = a % b
squared = a ** b

#print automatically makes new lines (unless specified otherwise)
print('the remainder of a divided by b is', remainder) # see results with print statement
print("the divison of a by b is ", division) # both '' and "" can be used
print("the floor division of a by b is", floordivision)
print("a to the power of b", squared) 

print(""" remainder is 2
floor division is 5
division is 5.6667
and finally, a squared b is 4913
""") #multiple line print -> """ """

#use of arrays with strings 
text = "python"
length = len(text) #calculates length

#print does not work with strings 
#print("first letter is" text[0])
#print("last letter is", text[5])
#print("first to 2nd last letter", text[0:5]) #excludes the last array
#print("whole letter", text[0:6]) 
#print("add first letter and second letter", text[0] + text[1])
#print("do not assign what the start array", text[:6]) #automatic start at 0
#print("do not assign the last array", text[1:]) #automatic finds the end of array

print("the length of the text is", length)
#strings cannot be modified once declared but characters/integers/floats can be modified
cubes = [1,8,27,65,125] 
print("before modification", cubes)
cubes[3] = 64 #modification
print("after modification", cubes)
cubes.append(216) #add extra element at the end of the array 
print("after append", cubes)

#same for characters
characters = ['p', 'y', 't', 'h', 'o', 'n']
print("before modification", characters)
characters[1:3] = ['Y', 'T'] #modification 
print("after modification", characters)

#Nested arrays:
x = [characters, cubes] #nest the two arrays together
print("nested arrays look like", x)
print("lets point to one specific element", x[0][1])

#putting a "end=','" in the printf results in putting a comma instead of new line 