# Writes a file that contains lots of different cluster values

import numpy
import pickle
import random

def ahm(angle, size):
    """ Taking in a guiding angle, creates simulated MCMC output of variations
        on that angle and the associated probabilities of those systems.
        Wicked oversimplified but perfectly fine for a first go-around.
        Input:
        angle = an angle between 0 and 90 degrees
        Output:
        Writes the angles and their associated probabilities to PICKLE files.
    """

    array = numpy.zeros(size)
    prob = numpy.zeros(size)
    
    for i in range(size):
        array[i] = random.triangular(0,90,angle)
        # figure out the probability associated with such an angle
        prob[i] = (90-array[i])/5
        i = i + 1

    # writing everything to file
    filename = 'prob_clusters.pickle'
    F = open(filename, 'w')
    pickle.dump(prob,F)
    F.close()
    filename = 'angle_clusters.pickle'
    F = open(filename,'w')
    pickle.dump(array,F)
    F.close()

    return
