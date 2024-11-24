# Rampes
#### Video Demo:  https://youtu.be/ZcsZssYfYVg
#### Description:
This application calculates the profile of a ramp so that a car does not touch the ground

The ramp profile is calculated in four stages:
1. Enter the dimensions of the ramp to modify
 two of the three requested data must be entered, ramp height, ramp length or ramp floor, the third data is automatically entered, all data is in mm
2. Write down the dimensions of the car.

    that must pass through the ramp
6 characteristic dimensions of the car must be entered, all of them in millimeters
you also have to enter the margin of safety you want to have, by default it is set to 40 mm (minimum distance to the floor)
3. Calculation of the profile.

    The result is a list of ramp sections, each section containing the length of the section and the height orthogonal to the top of the ramp.
4. Generate a pdf to export the data.

    The ramp name and author name must be entered to populate the report header.

    A pdf file is then created in the downloads directory containing all the entered data of both the ramp and the car and the result obtained

###structure of the program.

The program is made in Python, and is structured as follows.

the app.py file has all the functionality to build web pages using flask and the functions.py file contains all the functions necessary to run the program.

The requirements.txt file contains all the dependencies needed to install the program.

In the static directory are all the image files and the javascript files.

In the templates directory there are all the html files that serve as a template to generate the web plans.

#details of the calculation algorithm.

the initial length of the ramp section is the distance between the wheels of the car.

the initial slope for the sections that are convex is the angle formed between the height of the bottom of the car and half the distance between the wheels and is given by the following formula:

max center angle = 2* atan (distance car to ground/(distance between wheels/2)

the initial slope for the sections that are concave is the angle formed by the height of the front part and the distance from the front wheel to the front of the car and is given by the following formula:

max frontal angle = atan (height of the front part on the ground / distance from the wheel to the front part)
the same formula is used for the back of the car.

rear max angle = atan (height of the rear part on the ground / distance from the rear wheel to the rear part)

for the calculations the unfavorable month of the two is chosen.

the calculation method is to add sections alternately to the lower part of the ramp and the upper part of the ramp until all the angles that make up the sections are less than or equal to the two angles described above

if this does not happen and the sum of sections is greater than the original ramp, the calculation is repeated again, decreasing the length of the section by 100 mm, and it is repeated until the length of the section is lower than the minimum permissible section, if this passes, the calculation is aborted and no result is given, otherwise all sections are listed in the results table.
