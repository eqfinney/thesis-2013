# Writes a file that contains lots of different cluster values

import numpy
import pickle

delta = 0
alpha = 1
pfrac = 0
sigma = 5

# creates input indexes and determines overall number of trials
delta_input = numpy.arange(0,95,5)
alpha_input = numpy.arange(1,2,0.5)
pfrac_input = numpy.arange(0,100,5)
len_arrays = len(delta_input) * len(alpha_input) * len(pfrac_input)

# creates empty arrays
array = numpy.zeros((len_arrays,4))

# have to re-figure out how range works
index = 0
for delta in delta_input:
    for alpha in alpha_input:
        for pfrac in pfrac_input:
            array[index][0] = delta
            array[index][1] = alpha
            array[index][2] = pfrac
            array[index][3] = sigma
            # increase pfrac
            pfrac = pfrac + 1
            # increases the index
            index = index + 1
        # increase alpha
        alpha = alpha + 1
    # increase delta
    delta = delta + 1

# writing everything to file
filename = 'simulated_clusters.pickle'
F = open(filename, 'w')
pickle.dump(array,F)
F.close()
filename = 'prob_clusters.pickle'
prob_array = numpy.ones(len_arrays)
F = open(filename, 'w')
pickle.dump(prob_array,F)
F.close()
filename = 'angle_clusters.pickle'
F = open(filename,'w')
print range(numpy.shape(array)[0])
array_new = numpy.zeros(len_arrays)
for j in range(numpy.shape(array)[0]):
    array_new[j] = array[j][0]
pickle.dump(array_new,F)
F.close()
