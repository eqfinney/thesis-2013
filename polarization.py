#
#
# EQ Finney
#
#

"""
Notes prior to beginning on the polarization code:
R = (alpha + 1)/(alpha - 0.5) [Ensslin et al. 1998 (3)]
gamma = 2*alpha + 1 [Ensslin et al. 1998 section 3.1]

Since we're going with the most conservative estimate, we're going to be using
the strong field case, which is given by equation (23):
<P> = ((gamma + 1)/(gamma + (7./3)))
        *((math.sin(delta))^2)/((2/15)*(13*R-7)/(R-1)) - (math.sin(delta))^2))

The weak field case is similar, except that the compression ratio term is
different (given by equation (22)).
"""

import math
import numpy
import pickle
import scipy.special as sci
import matplotlib.pyplot as plt

def exp_pfrac(delta, alpha):
    """ Determines fractional polarization expected from a model of given
        viewing angle and spectral index.
        Input:
        delta: the inclination angle provided by the model (in degrees)
        alpha: the spectral index as determined in the literature, used to
               calculate the expected polarization of a model viewed from a
               certain angle
        Output:
        pfrac_expected: the fractional polarization of the radio relic, as
                        determined by the relationship in Ensslin et al. 2008
    """
    Rexp = (alpha + 1)/(alpha - 0.5) # shock compression ratio
    gamma = 2*alpha + 1 # spectral index of the electrons

    # Calculating the strong field expected polarization
    gammacoeff = (gamma + 1)/(gamma + (7./3))
    ratioterm = ((2.0/15)*(13.0*Rexp-7)/(Rexp-1))
    deltarad = delta*math.pi/180.0
    angleterm = (math.sin(deltarad))**2
    pfrac_expected = gammacoeff*(angleterm/(ratioterm - angleterm))
    return pfrac_expected


def wlikelihood(pfrac_expected, pfrac, sigma):
    """ Given an expected fractional polarization and an array size and spacing,
        computes the value of the error function in a range around the expected
        value. Need to have a standard deviation value for this to work.
        Inputs:
        pfrac_expected: the fractional polarization of the radio relic, as
                        determined by the relationship outlined in Ensslin et
                        al. 2008 and carried out by the uwlikelihood function
                        above
        pfrac: the fractional polarization of the radio relic, as determined
               from the literature values
        sigma: the standard deviation of the fractional polarization - I have
               no idea how this would be determined yet
        Outputs:
        z: the number of standard deviations from the expected value to pfrac
        likelihood: the probability that pfrac is consistent with pfrac_expected
    """
    # This constraint is REALLY conservative.
    z = (pfrac_expected-pfrac)/sigma
    if (z>0):
        likelihood = 1
    else:
        #print "The number of standard deviations away is:", z
        likelihood = sci.erfc(math.fabs(z))
    return z, likelihood


def probability(delta, alpha, pfrac, sigma):
    """ Incorporates the above two functions into a main function that
        determines the likelihood of an inclination angle given how it compares
        to the expected fractional polarization.
        Inputs:
        delta: the inclination angle provided by the model (in degrees)
        alpha: the spectral index as determined in the literature, used to
               calculate the expected polarization of a model viewed from a
               certain angle
        pfrac: the fractional polarization of the radio relic, as determined
               from the literature values
        sigma: the standard deviation of the fractional polarization - I have
               no idea how this would be determined yet
    """
 
    # Checking to see if the parameters fit the code
    if (delta > 90) or (delta < 0):
        print "delta must be between zero and ninety degrees! Exiting."
        sys.exit()

    # Calculating the expected fractional polarization
    pfrac_expected = exp_pfrac(delta, alpha)
    
    # Calculating the likelihood of seeing this system given actual data
    z, likelihood = wlikelihood(pfrac_expected, pfrac, sigma)
    if (delta > 70):
        print "The inclination angle is:", delta
        print "The expected fractional polarization is:", pfrac_expected
        print "The actual fractional polarization is: ", pfrac
        print "The actual polarization is", z, "sigma from the expected value."
        print "The likelihood is:", likelihood
    return likelihood

def main(prob_MCMC, angle_MCMC, spectral_index, pfrac, sigma=0.05, prefix=''):
    """ Takes in Will's pickle files (which contain hundreds of MCMC results)
        and then for each result uses the angle from MCMAC to compute a
        likelihood (with radio prior) using my probability function. This is
        subsequently multiplied by the probability obtained from MCMAC to
        get an overall probability, which is written to pickle file for future
        use and plotting.
        Inputs:
        prob_MCMC: the name of a pickle file containing an array of
                   probabilities (string)
        angle_MCMC: the name of a pickle file containing an array of viewing
                   angles (string)
        spectral_index: the spectral index of the system as determined from
                   literature (float)
        pfrac: the polarization fraction of the system as determined from the
               literature (float)
        sigma: the standard deviation of the fractional polarization, which I
               don't know how to determine yet (float)
        prefix: a prefix of the pickle file to be written (float)
        No outputs, but an array of probabilities is written to file
    """

    # loading pickle arrays from file
    array_prob = pickle.load(open(prob_MCMC,'rb'))
    array_angle = pickle.load(open(angle_MCMC,'rb'))

    # Making certain that information is in the correct form
    if (spectral_index < 0):
        spectral_index = math.fabs(spectral_index)

    if (pfrac > 1) or (pfrac < 0):
        print "pfrac must be between 0 and 1! Exiting."
        sys.exit()

    # Running the actual code
    size = numpy.size(array_angle)
    mod_prob_array = numpy.zeros(size)
    init_prob_array = numpy.zeros(size)

    for index in range(size):
        # accounting for differences between Dawson 2012 and Ensslin 1998
        angle = (90 - array_angle[index])
        
        likelihood = probability(angle, spectral_index, pfrac, sigma)
        init_prob_array[index] = likelihood
        mod_prob_array[index] = likelihood*array_prob[index]

    # Then do something like pfrac vs. inclination angle, with different colors
    # for different likelihood values, and see where they fall.
    i = [(90-x) for x in array_angle]
    if numpy.size(i) == numpy.size(init_prob_array):
        plt.scatter(i,init_prob_array, marker='s')
        plt.title('Probability of system, given polarization')
        plt.xlim(0,90)
        plt.ylim(0,1)
        plt.xlabel('inclination angle')
        plt.ylabel('probability')
        plt.savefig(prefix+'_radio_fig.png')
        F = open(prefix + '_radio_fig.png')
        F.close()
        plt.close()
        
    filename = prefix+'_radio_prob.pickle'
    F = open(filename, 'w')
    pickle.dump(init_prob_array,F)
    F.close()
    filename = prefix+'_mod_prob.pickle'
    F = open(filename, 'w')
    pickle.dump(mod_prob_array,F)
    F.close()
    return
    
