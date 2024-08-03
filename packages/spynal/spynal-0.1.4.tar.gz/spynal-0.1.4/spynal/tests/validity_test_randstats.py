"""
Suite of tests to assess "face validity" of randomization statistic functions in randstats.py
Usually used to test new or majorly updated functions to ensure they perform as expected.

Includes tests that parametrically estimate statistics as a function of difference in distribution
means, assays of bias, etc. to establish methods produce expected pattern of results.

Plots results and runs assertions that basic expected results are reproduced

Function list
-------------
- test_randstats :          Contains tests of randomization statistic computation functions
- stat_test_battery :       Runs standard battery of tests of randomization stat functions

- test_confints :           Contains tests of confidence interval computation functions
- confint_test_battery :    Runs standard battery of tests of confidence interval functions
"""
import os
import time
from math import ceil
import numpy as np
import matplotlib.pyplot as plt

from spynal.tests.data_fixtures import simulate_dataset
from spynal.utils import set_random_seed
from spynal.randstats.randstats import one_sample_test, paired_sample_test, paired_sample_association_test, \
                                       two_sample_test, one_way_test, two_way_test, \
                                       one_sample_confints, paired_sample_confints, two_sample_confints


# =============================================================================
# Tests for functions computing statistics/statistical tests
# =============================================================================
def test_randstats(stat, method, test='gain', test_values=None, term=0, distribution='normal',
                   alpha=0.05, n_reps=100, seed=None, do_tests=True,
                   do_plots=False, plot_dir=None, **kwargs):
    """
    Basic testing for randomization statistic computation functions

    Generates synthetic data, computes statistics, p values, and significance using given method,
    and compares computed to expected values.

    For test failures, raises an error or warning (depending on value of `do_tests`).
    Optionally plots summary of test results.

    Parameters
    ----------
    stat : str
        Type of statistical test to evaluate: 
        'one_sample'|'paired_sample'|'paired_sample_assoc'| 'two_sample'|'one_way'|'two_way'

    method : str
        Resampling paradigm to use for test: 'permutation' | 'bootstrap'

    test : str, default: 'gain'
        Type of test to run. Options:
        
        - 'gain' : Tests multiple values for btwn-cond response difference (gain).
            Checks for monotonically increasing stat/decreasing p value.
        - 'spread' : Tests multiple values for distribution spread (SD).
            Checks for monotonically decreasing stat/increasing p value.
        - 'n' : Tests multiple values of number of trials (n).
            Checks that stat doesn't vary, but p value decreases, with n.
        - 'bias' : Tests multiple n values with 0 btwn-cond difference.
            Checks that stat doesn't vary and p value remains ~ 0 (unbiased).

    test_values : array-like, shape=(n_values,), dtype=str
        List of values to test. Interpretation and defaults are test-specific:
        
        - 'gain' :      Btwn-condition response differences (gains). Default: [1,2,5,10,20]
        - 'spread' :    Gaussian SDs for each response distribution. Default: [1,2,5,10,20]
        - 'n'/'bias' :  Trial numbers. Default: [25,50,100,200,400,800]

    term : int, default: 0
        Which model term to modify for testing 2-way stats (unused for other stats).
        0,1 = main effects, 2 = interaction. 

    distribution : str, default: 'normal'
        Name of distribution to simulate data from. Options: 'normal' | 'poisson'

    n_reps : int, default: 100
        Number of independent repetitions of tests to run

    alpha : float, default: 0.05
        Significance criterion "alpha"

    do_tests : bool, default: True
        Set=True to evaluate test results against expected values and raise an error if they fail

    do_plots : bool, default: False
        Set=True to plot test results

    plot_dir : str, default: None (don't save to file)
        Full-path directory to save plots to. Set=None to not save plots.

    seed : int, default: 1 (reproducible random numbers)
        Random generator seed for repeatable results. Set=None for fully random numbers.

    **kwargs :
        All other keyword args passed as-is to `simulate_dataset` or statistic computation
        function, as appropriate

    Returns
    -------
    means : dict, {str : ndarray. shape=(n_values,)}
        Mean results (across independent test runs) of variables output from randomization tests
        for each tested value. Each key/value pair corressponds to a computed statistic variable:
        
        - 'signif' :    Binary signficance decision (at criterion <alpha>)
        - 'p' :         p values
        - 'log_p' :     p values negative log-transformed -log10(p) to increase with effect size
        - 'stat_obs' :  Observed evaluatation statistic values
        - 'stat_resmp' :Mean resampled statistic values (across all resamples)

    sds : : dict, {str : ndarray. shape=(n_values,)}
        Standard deviation of results (across test runs) of variables output from rand tests for
        each tested value. Same fields as means.

    passed : bool
        True if all tests produce expected values; otherwise False.
    """
    # Note: Set random seed once here, not for every random data generation loop below
    if seed is not None: set_random_seed(seed)

    test = test.lower()
    method = method.lower()

    # Set defaults for tested values and set up data generator function depending on <test>
    # Note: Only set random seed once above, don't reset in data generator function calls
    if stat == 'two_way':       n_conds = 4         # Simulate 2-way design w/ 4 conds (2x2)
    elif stat == 'one_sample':  n_conds = 1
    else:                       n_conds = 2
    if stat == 'two_way':
        # Set gains for effect on 1st main effect, 2nd main effect, and interaction effect
        if term == 0:   gain_pattern = np.asarray([0,0,1,1])
        elif term == 1: gain_pattern = np.asarray([1,0,1,0])
        elif term == 2: gain_pattern = np.asarray([0,1,1,0])
    else:
        gain_pattern = 1
        
    sim_args = dict(gain=5.0*gain_pattern, offset=0.0, spreads=10.0, n_conds=n_conds, n=100,
                    distribution=distribution, correlation=0, seed=None)
    # Override defaults with any simulation-related params passed to function
    for arg in sim_args:
        if arg in kwargs: sim_args[arg] = kwargs.pop(arg)

    if test == 'gain':
        test_values = [1,2,5,10,20] if test_values is None else test_values
        del sim_args['gain']                        # Delete preset arg so uses arg to lambda below
        gen_data = lambda gain: simulate_dataset(**sim_args,gain=gain*gain_pattern)

    elif test in ['spread','spreads','sd']:
        test_values = [1,2,5,10,20] if test_values is None else test_values
        del sim_args['spreads']                     # Delete preset arg so uses arg to lambda below
        gen_data = lambda spreads: simulate_dataset(**sim_args,spreads=spreads)

    elif test in ['n','n_trials','bias']:
        test_values = [25,50,100,200,400,800] if test_values is None else test_values
        if test == 'bias': sim_args.update(offset=0, gain=0)    # Set gain,offset=0 for bias test
        del sim_args['n']                           # Delete preset arg so uses arg to lambda below
        # Set model correlation != 0 for paired_sample_assoc stat to see effects of changing n
        if test in ['n','n_trials'] and (stat == 'paired_sample_assoc'): sim_args['correlation'] = 0.2
        gen_data = lambda n_trials: simulate_dataset(**sim_args,n=n_trials)

    elif test == 'n_conds':
        test_values = [2,4,8] if test_values is None else test_values
        del sim_args['n_conds']                     # Delete preset arg so uses arg to lambda below
        gen_data = lambda n_conds: simulate_dataset(**sim_args,n_conds=n_conds)

    elif test == 'correlation':
        test_values = [0,0.25,0.5,0.75,1] if test_values is None else test_values
        del sim_args['correlation']                 # Delete preset arg so uses arg to lambda below
        gen_data = lambda correlation: simulate_dataset(**sim_args,correlation=correlation)

    else:
        raise ValueError("Unsupported value '%s' set for <test>" % test)

    # Set up function for computing randomization stats
    stat_func = _str_to_stat_func(stat)
    kwargs.update(return_stats=True)
    if 'n_resamples' not in kwargs: kwargs['n_resamples'] = 100

    n_terms = 3 if stat == 'two_way' else 1
    results = dict(signif = np.empty((n_terms,len(test_values),n_reps),dtype=bool),
                   p = np.empty((n_terms,len(test_values),n_reps)),
                   log_p = np.empty((n_terms,len(test_values),n_reps)),
                   stat_obs = np.empty((n_terms,len(test_values),n_reps)),
                   stat_resmp = np.empty((n_terms,len(test_values),n_reps)))

    resmp_axis = -1 if stat == 'two_way' else 0

    for i_value,test_value in enumerate(test_values):
        for i_rep in range(n_reps):
            # Generate simulated data with current test value
            data,labels = gen_data(test_value)

            # One-sample tests
            if stat == 'one_sample':
                p, stat_obs, stat_resmp = stat_func(data, method=method, **kwargs)

            # 1-way and 2-way ANOVA-like multi-level factorial tests
            elif stat in ['one_way','two_way']:
                # For 2-way tests, reorg labels from (n,) vector of values in set {0-3}
                # to (n,3) array where 1st 2 col's are 2 orthogonal factors, 3rd col is interaction
                if stat == 'two_way':
                    labels = np.stack((labels >= 2, (labels == 1) | (labels == 3), labels), axis=1)
                p, stat_obs, stat_resmp = stat_func(data, labels, method=method, **kwargs)

            # Paired-sample and two-sample tests
            else:
                p, stat_obs, stat_resmp = stat_func(data[labels==1], data[labels==0],
                                                    method=method, **kwargs)


            # Determine which values are significant (p < alpha criterion)
            results['signif'][:,i_value,i_rep]      = p < alpha
            results['p'][:,i_value,i_rep]           = p
            # Negative log-transform p values so increasing = "better" and less compressed
            results['log_p'][:,i_value,i_rep]       = -np.log10(p)
            results['stat_obs'][:,i_value,i_rep]    = stat_obs
            # Compute mean resampled stat value across all resamples
            results['stat_resmp'][:,i_value,i_rep]  = stat_resmp.mean(axis=resmp_axis)


    # Compute mean and std dev across different reps of simulation
    means   = {variable : values.mean(axis=-1) for variable,values in results.items()}
    sds     = {variable : values.std(axis=-1,ddof=0) for variable,values in results.items()}
    variables = ['signif','log_p','stat_obs','stat_resmp']

    if do_plots:
        plt.figure()
        for i_vbl,variable in enumerate(variables):
            for i_term in range(n_terms):
                mean = means[variable][i_term,:]
                sd = sds[variable][i_term,:]

                sp = i_term*len(variables) + i_vbl + 1
                plt.subplot(n_terms, len(variables), sp)
                plt.grid(axis='both',color=[0.75,0.75,0.75],linestyle=':')
                plt.errorbar(test_values, mean, sd, marker='o')
                if i_term == n_terms-1:
                    plt.xlabel('n' if test == 'bias' else test)
                    plt.ylabel('-log10(p)' if variable == 'log_p' else variable)
                if i_term == 0: plt.title(variable)
                if stat == 'two_way': plt.ylabel("Term %d" % i_term)

        if plot_dir is not None:
            filename = os.path.join(plot_dir,'stat-summary-%s-%s-%s' % (stat,method,test))
            if stat == 'two_way': filename += '-term%d' % term
            plt.savefig(filename)

    # Determine if test actually produced the expected values
    # 'gain' : Test if p values decrease and stat increases monotonically with between-group gain
    if test == 'gain':
        if stat != 'paired_sample_assoc':
            evals = [((np.diff(means['signif'][term,:]) >= 0).all(),
                        "Significance does not increase monotonically with btwn-cond mean diff"),
                    ((np.diff(means['log_p'][term,:]) >= 0).all(),
                        "p values do not decrease monotonically with btwn-cond mean diff"),
                    ((np.diff(means['stat_obs'][term,:]) > 0).all(),
                        "Statistic does not increase monotonically with btwn-cond mean diff"),
                    (means['stat_resmp'][term,:].ptp() <= sds['stat_resmp'][term,:].max(),
                        "Resampled stat has larger than expected range with btwn-cond mean diff")]
        else:
            evals = [] # todo should we test for no change here?
            
    # 'spread' : Test if p val's increase and stat decreases monotonically with within-group spread
    elif test in ['spread','spreads','sd']:
        if stat != 'paired_sample_assoc':
            evals = [((np.diff(means['signif'][term,:]) > 0).all(),
                        "Signif does not decrease monotonically with within-cond spread increase"),
                    ((np.diff(means['log_p'][term,:]) >= 0).all(),
                        "p values do not increase monotonically with within-cond spread increase"),
                    ((np.diff(means['stat_obs'][term,:]) < 0).all(),
                        "Statistic does not decrease monotonically with within-cond spread increase"),
                    (means['stat_resmp'][term,:].ptp() <= sds['stat_resmp'].max(),
                        "Resampled stat has > than expected range with within-cond spread increase")]
        else:
            evals = [] # todo should we test for no change here?

    # 'n' : Test if p values decrease, but statistic is ~ same for all values of n (unbiased by n)
    elif test in ['n','n_trials']:
        evals = [((np.diff(means['signif'][term,:]) >= 0).all(),
                    "Significance does not increase monotonically with n"),
                 ((np.diff(means['log_p'][term,:]) >= 0).all(),
                    "p values do not decrease monotonically with n"),
                 ((np.diff(means['stat_obs'][term,:]) >= 0).all(),
                    "Statistic does not decrease monotonically with n"),
                 (means['stat_resmp'][term,:].ptp() <= sds['stat_resmp'].max(),
                    "Resampled stat has > expected range across n's (likely biased by n)")]
        if stat == 'paired_sample_assoc': del evals[2]
        
    # 'bias': Test that statistic is not > 0 and p value ~ alpha if gain = 0, for varying n
    elif test == 'bias':
        evals = [(((np.abs(means['signif'][term,:].mean()) - alpha) < sds['signif'][term,:]).all(),
                    "Signif different from expected pct (%.1f) when no mean diff between conds"
                    % alpha),
                 (((np.abs(means['p'][term,:].mean()) - 0.5) < sds['p'][term,:]).all(),
                    "p values are different from expected (0.5) when no mean diff between conds"),
                 ((np.abs(means['stat_obs'][term,:]) < sds['stat_obs'][term,:]).all(),
                    "Statistic is above 0 when no mean diff between conds")]

    # 'correlation': Test that correlation stat monotonically increases with correction,
    # that other statistics are ~ same for all values of correlation
    elif test == 'correlation':
        if stat == 'paired_sample_assoc':
            evals = [((np.diff(means['signif'][term,:]) >= 0).all(),
                        "Significance does not increase monotonically with correlation"),
                    ((np.diff(means['log_p'][term,:]) >= 0).all(),
                        "p values do not decrease monotonically with correlation"),
                    ((np.diff(means['stat_obs'][term,:]) > 0).all(),
                        "Statistic does not increase monotonically with correlation"),
                    (means['stat_resmp'][term,:].ptp() <= sds['stat_resmp'][term,:].max(),
                        "Resampled stat has larger than expected range with correlation")]                     
        else:
            evals = [] # todo Should we test for no change otherwise
            
        
    passed = True
    for cond,message in evals:
        if not cond:    passed = False

        # Raise an error for test fails if do_tests is True
        if do_tests:    assert cond, AssertionError(message)
        # Just issue a warning for test fails if do_tests is False
        elif not cond:  print("Warning: " + message)

    return means, sds, passed


def stat_test_battery(stats=('one_sample','paired_sample','paired_sample_assoc',
                             'two_sample','one_way','two_way'),
                      methods=('permutation','bootstrap'),
                      tests=('gain','spread','n','bias','correlation'),
                      do_tests=True, **kwargs):
    """
    Run a battery of given tests on given randomization statistic computation methods

    Parameters
    ----------
    stats : array-like of str, default: ('one_sample','paired_sample','paired_sample_assoc',
        'two_sample','one_way','two_way')
        List of statistical tests to evaluate.

    methods : array-like of str, default: ('permutation','bootstrap') (all supported methods)
        List of resampling paradigms to run.
                
    tests : array-like of str, default: ('gain','spread','n','bias','correlation')
        List of tests to run.
                
    do_tests : bool, default: True
        Set=True to evaluate test results against expected values and raise an error if they fail

    **kwargs :
        Any other kwargs passed directly to test_randstats()
    """
    if isinstance(stats,str): stats = [stats]
    if isinstance(methods,str): methods = [methods]
    if isinstance(tests,str): tests = [tests]

    for stat in stats:
        for test in tests:
            for method in methods:
                # TEMP Bootstrap version of 1-way/2-way tests not coded up yet...
                if (stat in ['one_way','two_way']) and (method != 'permutation'): continue
                print("Running %s test on %s %s" % (test,stat,method))

                # Run separate tests for each term of 2-way stats (2 main effects and interaction)
                if stat == 'two_way':
                    passed = np.empty((3,))
                    for term in range(3):
                        _,_,passed[term] = test_randstats(stat, method, test=test, term=term,
                                                          do_tests=do_tests, **kwargs)
                    passed = passed.all()

                else:
                    _,_,passed = test_randstats(stat, method, test=test, do_tests=do_tests,
                                                **kwargs)

                print('%s' % 'PASSED' if passed else 'FAILED')
                if 'plot_dir' in kwargs: plt.close('all')


# =============================================================================
# Tests for functions computing confidence intervals
# =============================================================================
def test_confints(stat, test='gain', test_values=None, distribution='normal', confint=0.95,
                  n_reps=100, seed=None, do_tests=True, do_plots=False, plot_dir=None, **kwargs):
    """
    Basic testing for bootstrap confidence interval computation functions

    Generate synthetic data, computes statistics, confints, and significance using given method,
    and compare computed to expected values.

    For test failures, raises an error or warning (depending on value of `do_tests`).
    Optionally plots summary of test results.
    
    Parameters
    ----------
    stat : str
        Type of statistical test to evaluate: 'one_sample' | 'paired_sample' | 'two_sample'

    test : str, default: 'gain'
        Type of test to run. Options:
        
        - 'gain' : Tests multiple values for btwn-cond response difference (gain).
            Checks for monotonically increasing confints.
        - 'spread' : Tests multiple values for distribution spread (SD).
            Checks for monotonically decreasing confints.
        - 'n' : Tests multiple values of number of trials (n).
            Checks that confints decrease with n.
        - 'bias' : Tests multiple n values with 0 btwn-cond difference.
            Checks that stat doesn't vary and p value remains ~ 0 (unbiased).

    test_values : array-like, shape=(n_values,), dtype=str
        List of values to test. Interpretation and defaults are test-specific:
        
        - 'gain' :      Btwn-condition response differences (gains). Default: [1,2,5,10,20]
        - 'spread' :    Gaussian SDs for each response distribution. Default: [1,2,5,10,20]
        - 'n'/'bias' :  Trial numbers. Default: [25,50,100,200,400,800]

    distribution : str, default: 'normal'
        Name of distribution to simulate data from. Options: 'normal' | 'poisson'

    confint : float, default: 0.95 (95% CI)
        Confidence interval to compute (1-alpha). 

    do_tests : bool, default: True
        Set=True to evaluate test results against expected values and raise an error if they fail

    do_plots : bool, default: False
        Set=True to plot test results

    plot_dir : str, default: None (don't save to file)
        Full-path directory to save plots to. Set=None to not save plots.

    seed : int, default: 1 (reproducible random numbers)
        Random generator seed for repeatable results. Set=None for fully random numbers.

    **kwargs :
        All other keyword args passed as-is to `simulate_dataset` or confint computation
        function, as appropriate

    Returns
    -------
    means : dict, {str : ndarray. shape=(n_values,)}
        Mean results (across independent test runs) of variables output from randomization tests
        for each tested value. Each key/value pair corressponds to a computed statistic variable:
        
        - 'signif' :       Binary signficance decision (at criterion <alpha>)
        - 'p' :            p values (actually -log10(p) so increases with effect size)
        - 'stat_obs' :     Observed evaluatation statistic values
        - 'stat_resmp' :   Mean resampled statistic values (across all resamples)

    sds : {str : (n_values,) ndarray}
        Standard deviation of results (across test runs) of variables output from rand tests
        for each tested value. Same fields as means.

    passed : bool
        True if all tests produce expected values; otherwise False.
    """
    # HACK Hard-code term=0, but keep term for possible future extension to 1-way/2-way stats
    term = 0
    # Note: Set random seed once here, not for every random data generation loop below
    if seed is not None: set_random_seed(seed)

    test = test.lower()

    # Set defaults for tested values and set up data generator function depending on <test>
    # Note: Only set random seed once above, don't reset in data generator function calls
    if stat == 'two_way':       n_conds = 4         # Simulate 2-way design w/ 4 conds (2x2)
    elif stat == 'one_sample':  n_conds = 1
    else:                       n_conds = 2
    if stat == 'two_way':
        # Set gains for effect on 1st main effect, 2nd main effect, interaction effect
        if term == 0:   gain_pattern = np.asarray([0,0,1,1])
        elif term == 1: gain_pattern = np.asarray([1,0,1,0])
        elif term == 2: gain_pattern = np.asarray([0,1,1,0])
    else:
        gain_pattern = 1
    sim_args = dict(gain=5.0*gain_pattern, offset=0.0, spreads=10.0, n_conds=n_conds, n=100,
                    distribution=distribution, seed=None)
    # Override defaults with any simulation-related params passed to function
    for arg in sim_args:
        if arg in kwargs: sim_args[arg] = kwargs.pop(arg)

    if test == 'gain':
        test_values = [1,2,5,10,20] if test_values is None else test_values
        del sim_args['gain']                        # Delete preset arg so uses arg to lambda below
        gen_data = lambda gain: simulate_dataset(**sim_args,gain=gain*gain_pattern)

    elif test in ['spread','spreads','sd']:
        test_values = [1,2,5,10,20] if test_values is None else test_values
        del sim_args['spreads']                     # Delete preset arg so uses arg to lambda below
        gen_data = lambda spreads: simulate_dataset(**sim_args,spreads=spreads)

    elif test in ['n','n_trials','bias']:
        test_values = [25,50,100,200,400,800] if test_values is None else test_values
        if test == 'bias': sim_args.update(offset=0, gain=0)    # Set gain,offset=0 for bias test
        del sim_args['n']                           # Delete preset arg so uses arg to lambda below
        gen_data = lambda n_trials: simulate_dataset(**sim_args,n=n_trials)

    elif test == 'n_conds':
        test_values = [2,4,8] if test_values is None else test_values
        del sim_args['n_conds']                     # Delete preset arg so uses arg to lambda below
        gen_data = lambda n_conds: simulate_dataset(**sim_args,n_conds=n_conds)

    else:
        raise ValueError("Unsupported value '%s' set for <test>" % test)

    # Set up function for computing randomization stats
    confint_func = _str_to_confint_func(stat)
    kwargs.update(return_stats=True)
    kwargs.update(confint=confint)
    if 'n_resamples' not in kwargs: kwargs['n_resamples'] = 100

    n_terms = 3 if stat == 'two_way' else 1
    results = dict(confints = np.empty((n_terms,2,len(test_values),n_reps)),
                   ci_diff = np.empty((n_terms,len(test_values),n_reps)),
                   signif = np.empty((n_terms,len(test_values),n_reps),dtype=bool),
                   stat_obs = np.empty((n_terms,len(test_values),n_reps)),
                   stat_resmp = np.empty((n_terms,len(test_values),n_reps)))

    resmp_axis = -1 if stat == 'two_way' else 0

    for i_value,test_value in enumerate(test_values):
        for i_rep in range(n_reps):
            # Generate simulated data with current test value
            data,labels = gen_data(test_value)

            # One-sample tests
            if stat == 'one_sample':
                confints, stat_obs, stat_resmp = confint_func(data, **kwargs)

            # 1-way and 2-way ANOVA-like multi-level factorial tests
            elif stat in ['one_way','two_way']:
                # For 2-way tests, reorg labels from (n,) vector of values in set {0-3}
                # to (n,3) array where 1st 2 col's are 2 orthogonal factors, 3rd col is interaction
                if stat == 'two_way':
                    labels = np.stack((labels >= 2, (labels == 1) | (labels == 3), labels), axis=1)
                confints, stat_obs, stat_resmp = confint_func(data, labels, **kwargs)

            # Paired-sample and two-sample tests
            else:
                confints, stat_obs, stat_resmp = confint_func(data[labels==1], data[labels==0],
                                                              **kwargs)

            # Determine which values are significant (p < alpha criterion)
            results['signif'][:,i_value,i_rep] = (confints > 0).all()
            # Negative log-transform p values so increasing = "better" and less compressed
            results['confints'][:,:,i_value,i_rep] = confints
            results['stat_obs'][:,i_value,i_rep] = stat_obs
            # Compute mean resampled stat value across all resamples
            results['stat_resmp'][:,i_value,i_rep] = stat_resmp.mean(axis=resmp_axis)

    # Compute difference btwn each set of confidence intervals (upper - lower)
    results['ci_diff'] = np.diff(results['confints'], axis=1).squeeze(axis=1)

    # Compute mean and std dev across different reps of simulation
    means   = {variable : values.mean(axis=-1) for variable,values in results.items()}
    sds     = {variable : values.std(axis=-1,ddof=0) for variable,values in results.items()}
    variables = list(means.keys())

    if do_plots:
        plt.figure()
        for i_vbl,variable in enumerate(variables):
            for i_term in range(n_terms):
                mean = means[variable][i_term,:]
                sd = sds[variable][i_term,:]

                sp = i_term*len(variables) + i_vbl + 1
                plt.subplot(n_terms, len(variables), sp)
                plt.grid(axis='both',color=[0.75,0.75,0.75],linestyle=':')
                if variable == 'confints':
                    # Plot lower, upper confints separately
                    plt.errorbar(test_values, mean[0,:], sd[0,:], marker='o')
                    plt.errorbar(test_values, mean[1,:], sd[1,:], marker='o')
                else:
                    plt.errorbar(test_values, mean, sd, marker='o')
                if i_term == n_terms-1:
                    plt.xlabel('n' if test == 'bias' else test)
                    plt.ylabel(variable)
                if i_term == 0: plt.title(variable)
                if stat == 'two_way': plt.ylabel("Term %d" % i_term)

        if plot_dir is not None:
            filename = os.path.join(plot_dir,'stat-summary-%s-%s' % (stat,test))
            if stat == 'two_way': filename += '-term%d' % term
            plt.savefig(filename)

    # Determine if test actually produced the expected values
    # 'gain' : Test if statistic and significance increases monotonically with between-group gain
    if test == 'gain':
        evals = [((np.diff(means['signif'][term,:]) >= 0).all(),
                    "Significance does not increase monotonically with btwn-cond mean diff"),
                 (means['ci_diff'][term,:].ptp() < sds['ci_diff'][term,:].max(),
                    "Confints have larger than expected range with btwn-cond mean diff"),
                 ((np.diff(means['stat_obs'][term,:]) > 0).all(),
                    "Statistic does not increase monotonically with btwn-cond mean diff"),
                 ((np.diff(means['stat_resmp'][term,:]) > 0).all(),
                    "Resampled statistic does not increase monotonically with btwn-cond mean diff")]
        # Confidence intervals not expected to change with mean for 1-sample data, so remove test
        if stat == 'one_sample': evals.pop(1)

    # 'spread' : Test if confints increase and stat decreases monotonic with within-group spread
    elif test in ['spread','spreads','sd']:
        evals = [((np.diff(means['signif'][term,:]) > 0).all(),
                    "Signif does not decrease monotonically with within-cond spread increase"),
                 ((np.diff(means['ci_diff'][term,:]) > 0).all(),
                    "Confints do not increase monotonically with within-cond spread increase"),
                 ((np.diff(means['stat_obs'][term,:]) < 0).all(),
                    "Statistic does not decrease monotonically with within-cond spread increase"),
                 ((np.diff(means['stat_resmp'][term,:]) < 0).all(),
                    "Resampled stat does not decrease monotonic with within-cond spread increase")]

    # 'n' : Test if confints decrease, but statistic is ~ same for all values of n (unbiased by n)
    elif test in ['n','n_trials']:
        evals = [((np.diff(means['signif'][term,:]) >= 0).all(),
                    "Significance does not increase monotonically with n"),
                 ((np.diff(means['ci_diff'][term,:]) <= 0).all(),
                    "Confints do not decrease monotonically with n"),
                 (means['stat_obs'][term,:].ptp() <= sds['stat_obs'][term,:].max(),
                    "Statistic has larger than expected range with n"),
                 (means['stat_resmp'][term,:].ptp() <= sds['stat_resmp'][term,:].max(),
                    "Resampled statistic has larger than expected range with n")]

    # 'bias': Test that statistic is not > 0 and p value ~ alpha if gain = 0, for varying n
    elif test == 'bias':
        evals = [((means['confints'][term,0,:] < 0).all() & (0 < means['confints'][term,1,:]).all(),
                    "Confints don't overlap with 0 when no mean diff between conditions"),
                 ((np.abs(means['stat_obs'][term,:]) < sds['stat_obs'][term,:].max()).all(),
                    "Statistic is above 0 when no mean diff between conditions"),
                 ((np.abs(means['stat_resmp'][term,:]) < sds['stat_resmp'][term,:].max()).all(),
                    "Resampled statistic is above 0 when no mean diff between conditions")]

    passed = True
    for cond,message in evals:
        if not cond:    passed = False

        # Raise an error for test fails if do_tests is True
        if do_tests:    assert cond, AssertionError(message)
        # Just issue a warning for test fails if do_tests is False
        elif not cond:  print("Warning: " + message)

    return means, sds, passed


def confint_test_battery(stats=['one_sample','paired_sample','two_sample'],
                         tests=('gain','n','bias'), do_tests=True, **kwargs):
    """
    Run a battery of given tests on given bootstrap confidence interval computation methods

    Parameters
    ----------
    stats : array-like of str, default: ['one_sample','paired_sample','two_sample']
        List of statistical tests to evaluate.
                

    tests : array-like of str, default: ('gain','n','bias') (all supported tests)
        List of tests to run.
                
    tests : array-like of str, default: ('gain','spread','n','bias','correlation')
        List of tests to run.
                
    do_tests : bool, default: True
        Set=True to evaluate test results against expected values and raise an error if they fail

    **kwargs :
        Any other kwargs passed directly to test_confints()
    """
    if isinstance(stats,str): stats = [stats]
    if isinstance(tests,str): tests = [tests]

    for stat in stats:
        for test in tests:
            print("Running %s test on %s" % (test,stat))

            # Run separate tests for each term of 2-way stats (2 main effects and interaction)
            if stat == 'two_way':
                passed = np.empty((3,))
                for term in range(3):
                    _,_,passed[term] = test_confints(stat, test=test, term=term,
                                                     do_tests=do_tests, **kwargs)
                passed = passed.all()

            else:
                _,_,passed = test_confints(stat, test=test, do_tests=do_tests, **kwargs)

            print('%s' % 'PASSED' if passed else 'FAILED')
            if 'plot_dir' in kwargs: plt.close('all')


# =============================================================================
# Helper functions
# =============================================================================
def _str_to_stat_func(stat):
    """ Convert string specifier for statistic to function for computing it """
    stat = stat.lower()
    if stat == 'one_sample':            return one_sample_test
    elif stat == 'paired_sample':       return paired_sample_test
    elif stat == 'paired_sample_assoc': return paired_sample_association_test
    elif stat == 'two_sample':          return two_sample_test
    elif stat == 'one_way':             return one_way_test
    elif stat == 'two_way':             return two_way_test
    else:
        raise ValueError("Unknown stat type '%s'" % stat)


def _str_to_confint_func(stat):
    """ Convert string specifier for statistic to function for computing its confints """
    stat = stat.lower()
    if stat == 'one_sample':        return one_sample_confints
    elif stat == 'paired_sample':   return paired_sample_confints
    elif stat == 'two_sample':      return two_sample_confints
    else:
        raise ValueError("Unknown stat type '%s'" % stat)
