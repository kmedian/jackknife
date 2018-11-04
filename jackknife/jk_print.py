
import scipy.special


def jk_print(pvalues, tscores, theta_jack, se_jack,
             theta_biased=None, theta_fullsample=None,
             varnames=None, N=None, d=None):
    # Title
    title = '\n'
    if d:
        title += 'Delete-' + str(d) + ' '
    title += 'Jackknife'
    if N:
        title += ', N=' + str(N)
    if d and N:
        if d > 1:
            title += ', C(N,d)=' + str(scipy.special.comb(N, d, exact=True))
    print(title)

    # column headers
    slen = 9
    fs0 = '{:32s}' + ''.join(
        ['{:^' + str(slen + 2) + 's}' for _ in range(len(pvalues))])
    if varnames:
        print(fs0.format('', *[v[:slen] for v in varnames]))
    else:
        print(fs0.format('', *['Var' + str(v) for v in range(len(pvalues))]))

    # first columns format
    s0 = '{:>30s}: '
    # data columns' format
    sn1 = '{:8.3f}   '
    sn2 = '  {:8.5f} '
    fs1 = s0 + ''.join([sn1 for _ in range(len(pvalues))])
    fs2 = s0 + ''.join([sn2 for _ in range(len(pvalues))])
    print(fs2.format('p-Values', *list(pvalues)))
    print(fs2.format('t-Scores', *list(tscores)))
    print(fs2.format('Jackknife Standard Error (SE)', *list(se_jack)))
    print(fs1.format('Jackknife Estimates (theta)', *list(theta_jack)))
    if theta_biased is not None:
        print(fs1.format('Jackknife Biased Estimate', *list(theta_biased)))
    if theta_fullsample is not None:
        print(fs1.format('Full Sample Estimate', *list(theta_fullsample)))

    # print('\n')
    return None
