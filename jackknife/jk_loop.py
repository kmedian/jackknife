
import scipy.special
import warnings
import itertools
import numpy as np


def jk_loop(func, data, d=1, combolimit=int(1e6)):
    """Generic Jackknife Subsampling procedure

    func : function
        A function pointer to a python function that
        - accept an <Observations x Features> matrix
            as input variable, and
        - returns an array/list or scalar value as
            estimate, metric, model parameter,
            jackknife replicate, etc.

    data : ndarray
        A <Observations x Features> numpy array

    d : int
        The number of observations to leave out for
        each Jackknife subsample, i.e. the subsample
        size is N-d. (The default is d=1 for the
        "Delete-1 Jackknife" procedure.)

    combolimit : int
        Maximum numbers of subsamples for binocoeff(N,d)
        combinations. (Default combolimit=1e6)

    Notes:
    ------
        Be aware that binom(N,d) can quickly exceed
        your computer's capabilities. The "Delete-d
        Jackknife" approaches are reasonable for
        small sample sizes, e.g. N=50 and d=3 result
        in 19600 subsamples to compute.

    Returns:
    --------
    theta_subs : ndarray
        The metrics, estimates, parameters, etc. of
        the model (see "func") for each subsample.
        It is a <C x M> matrix, i.e. C=binocoeff(N,d)
        subsamples, and M parameters that are returned
        by the model.

    theta_full : ndarray
        The metrics, estimates, parameters, etc. of
        the model (see "func") for the full sample.
        It is a <1 x M> vecotr with the M parameters
        that are returned by the model.
    """
    # How many observations contains data?
    N = data.shape[0]

    # throw a warning!
    numcombos = scipy.special.comb(N, d, exact=True)  # binocoeff
    if numcombos > 1e5:
        warnings.warn((
            "N={0:d} and d={1:d} result in {2:d} "
            "combinations to compute").format(N, d, numcombos))
    if numcombos > combolimit:
        raise Exception("Number of combinations exceeds 'combolimit'.")

    # list of tuples that contain all combinations of
    # row indicies to leave out
    leaveout = list(itertools.combinations(range(N), d))

    # store all metrics, estimates, model parameters
    # as list/array or scalar in one list
    theta_subsample = []

    # loop over all combinations
    idx = np.arange(0, N)

    for c in range(numcombos):
        # create true/false index for the c-th subsample
        # i.e. all true except the d leaveout indicies
        subidx = np.isin(idx, leaveout[c], assume_unique=True, invert=True)

        # compute metrics and store them
        theta_subsample.append(func(data[subidx, :]))

    # compute metrics on the full sample
    theta_fullsample = func(data)

    # done
    return np.array(theta_subsample), np.array(theta_fullsample)
