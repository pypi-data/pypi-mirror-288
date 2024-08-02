import numba as nb
import numpy as np
from numbalsoda import lsoda_sig, lsoda, dop853

RTOL = 100 * np.finfo(np.float64).eps
import pandas as pd
from scipy.optimize import minimize, fsolve

N_U_STEPS = int(1e6)

STATE_K = 'state'
TI = 'ti'

MIN_VALUE = np.log(np.finfo(np.float64).eps + 1)
MAX_VALUE = np.log(np.finfo(np.float64).max)


def state_frequencies(MU, LA, PSI):
    """
    Calculates equilibrium state frequencies for given rate values.

    :param MU: an array of state transition rates
    :param LA: an array of transmission rates
    :param PSI:  an array of removal rates
    :return: an array of equilibrium state frequencies [pi_0, ..., pi_m]
    """
    m = len(PSI)

    def func(PI):
        SIGMA = PI.dot(LA.sum(axis=1) - PSI)
        res = [PI.sum() - 1]
        for k in range(m - 1):
            pi_k = PI[k]
            res.append(pi_k * SIGMA + pi_k * (PSI[k] + MU[k, :].sum()) - PI.dot(MU[:, k] + LA[:, k]))
        return res

    PI = fsolve(func, np.ones(m) / m)
    if np.any(PI < 0) or np.any(PI > 1):
        return np.ones(m) / m
    return PI


c_sig_find_time_index = nb.types.int64(nb.types.double, nb.types.Array(nb.types.double, 1, 'C', readonly=True),
                                       nb.types.int64, nb.types.int64)


@nb.cfunc(c_sig_find_time_index)
def find_time_index(v, tt, start, stop):
    """
    Searches for an index i in time array tt, such that tt[i] <= v < tt[i + 1], using a binary search.

    :param v: a time value for which the index is searched for
    :param tt: a time array [t_0, ..., t_n] such that t_{i + 1} > t_i.
    :param start: start index for the search (inclusive)
    :param stop: stop index for the search (exclusive)
    :return: an index i, such that tt[i] <= v < tt[i + 1].
    """
    while start < stop:
        i = start + ((stop - start) // 2)
        if tt[i] <= v:
            if (i == stop - 1) or tt[i + 1] > v:
                return i
            start = i + 1
        else:
            if i == start:
                return i
            if tt[i - 1] <= v:
                return i - 1
            stop = i
    return start


def make_lsoda_func_U(MU, LA, PSI, RHO, SIGMA):

    PSI_NOT_RHO = PSI * (1 - RHO)
    m = len(RHO)

    @nb.cfunc(lsoda_sig)
    def pdf_U(t, U, dU, data):
        # LSODA integrates over ascending time array,
        # so we will assume time going from the last sampled tip (t=0) till the root (t=T) for U.
        # Note that the sign of the derivative here is the opposite,
        # due to the reversed time direction (from the last tip to root)

        U_ = nb.carray(U, m, dtype=np.float64)
        dU_ = nb.carray(dU, m, dtype=np.float64)

        dU_[:] = -(SIGMA - LA.dot(U_)) * U_ + MU.dot(U_) + PSI_NOT_RHO

        # dU[0] = -mu * (U[0] - U[1])
        # dU[1] = -(la + psi) * U[1] + la * U[0] * U[1] + psi * (1 - p)

    return pdf_U


def compute_U_lsoda(T, MU, LA, PSI, RHO, SIGMA=None, nsteps=N_U_STEPS):
    """
    Calculates a function get_U which for a given time t: 0 <= t <= T, would return
    an array of unobserved probabilities [U_1(t), ..., U_m(t)].

    U_k(t) are calculated by
    (1) solving their ODEs numerically for an array tt of nsteps times equally spaced between t=T and t=0,
    producing an array of solutions sol of length nstep (for corresponding times in tt)s.
    (2) creating a linear approximation which for a given time t (2a) find an index i such that tt[i] >= t > tt[i+1];
    (2b) returns sol[i + 1] + (sol[i] - sol[i + 1]) * (tt[i] - t) / (tt[i] - tt[i + 1]).


    :param T: time at end of the sampling period
    :param MU: an array of state transition rates
    :param LA: an array of transmission rates
    :param PSI: an array of removal rates
    :param RHO: an array of sampling probabilities
    :param SIGMA: an array of rate sums: MU.sum(axis=1) + LA.sum(axis=1) + PSI
    :return: a function that for a given time t returns the array of corresponding unsampled probabilities:
        t ->  [U_1(t), ..., U_m(t)].
    """
    if SIGMA is None:
        SIGMA = MU.sum(axis=1) + LA.sum(axis=1) + PSI

    # Note that LSODA needs the time interval to be ascending: we will therefore use reversed time for it,
    # going from the last sampled tip till the root
    tt = np.linspace(0, T, nsteps)
    y0 = np.ones(LA.shape[0], np.float64)

    ufunc = make_lsoda_func_U(MU, LA, PSI, RHO, SIGMA)
    ufuncptr = ufunc.address  # address to ODE function
    # integrate with lsoda method
    sol, success = lsoda(ufuncptr, y0, tt)
    return np.minimum(np.maximum(sol, 0), 1), tt


def get_value(t, sol, tt):
    """
    Approximates the value of a function at time t,
    given a descending array of its values at ascending times tt.
    """
    tt_len = len(tt)
    if t == tt[0]:
        return sol[0]
    if t == tt[-1]:
        return sol[-1]
    i = find_time_index(t, tt, 0, tt_len)
    sol_prev = sol[i, :]
    if i == (len(tt) - 1) or t == tt[i]:
        return sol_prev
    sol_next = sol[i + 1, :]
    if t == tt[i + 1]:
        return sol_next
    return sol_next + (sol_prev - sol_next) * (tt[i + 1] - t) / (tt[i + 1] - tt[i])


def make_lsoda_func_P(u_sol, u_tt, MU, LA, SIGMA, T):
    m = len(MU)
    tt_len = len(u_tt)

    @nb.cfunc(lsoda_sig)
    def pdf_Pany_l(t, P, dP, data):
        # LSODA integrates over ascending time array,
        # so we will assume time going from the last sampled tip (t=0) till the root (t=T) for P and U.
        t = max(0, min(t, T))
        i = find_time_index(t, u_tt, 0, tt_len)
        sol_prev = u_sol[i, :]
        if i == (tt_len - 1) or t == u_tt[i]:
            U = sol_prev
        else:
            sol_next = u_sol[i + 1, :]
            if t == u_tt[i + 1]:
                U = sol_next
            else:
                U = sol_next + (sol_prev - sol_next) * (t - u_tt[i]) / (u_tt[i + 1] - u_tt[i])
        P_ = nb.carray(P, m, dtype=np.float64)
        dP_ = nb.carray(dP, m, dtype=np.float64)
        # Note that the sign of the derivative here is the opposite,
        # due to the reversed time direction (from the last tip to root)
        dP_[:] = -(SIGMA - LA.dot(U)) * P_ + (MU + U * LA).dot(P_)
    return pdf_Pany_l


def get_P_lsoda(ti, l, t0, u_sol, u_tt, MU, LA, SIGMA, T):
    """
    Calculates P_{kl}^{(i)}(t0) for k in 1:m, where the initial condition is specified at time ti >= t0 (time of node i):
    P_{kl}^{(i)}(ti) = 0 for all k=l;
    P_{ll}^{(i)}(ti) = 1.

    :param ti: time for the initial condition (at node i)
    :param l: state of node i (the only state for which the initial condition is non-zero)
    :param t0: time to calculate the values at (t0 <= ti)
    :param u_sol: an array of unsampled probabilities
    :param u_tt: an of times corresponding to the array of unsampled probabilities
    :param MU: an array of state transition rates
    :param LA: an array of transmission rates
    :param SIGMA:  an array of rate sums: MU.sum(axis=1) + LA.sum(axis=1) + PSI, where PSI is the array of removal rates
    :return: a tuple containing an array of (potentially rescaled) branch evolution probabilities at time t0:
        [CP^{(i)}_{0l}(t0), .., CP^{(i)}_{ml}(t0)] and a log of the scaling factor: logC
    """
    y0 = np.zeros(LA.shape[0], np.float64)
    y0[l] = 1

    if t0 == ti:
        return y0

    # Note that LSODA needs the time interval to be ascending: we will therefore use reversed time for it,
    # going from the last sampled tip till the root

    u_tt_len = len(u_tt)
    u_i_start = find_time_index(T - ti, u_tt, 0, u_tt_len)
    u_i_stop = min(find_time_index(T - t0, u_tt, u_i_start, u_tt_len) + 1, u_tt_len - 1)

    rhs = make_lsoda_func_P(u_sol[u_i_start: u_i_stop + 1], u_tt[u_i_start: u_i_stop + 1], MU, LA, SIGMA, T)
    funcptr = rhs.address # address to ODE function
    # integrate with lsoda method
    y0[l] = 1048576
    const = [y0[l]]

    while True:
        tt = np.linspace(T - ti, T - t0, 2)
        sol, success = lsoda(funcptr, y0, tt)

        t_mid = t0
        while not success or np.any(sol[-1, :] <= 0) or np.any(np.log(sol[-1, :]) - np.sum(np.log(const)) >= 0) \
                or np.any(np.isnan(sol[-1, :])):
            t_mid = ti - (ti - t_mid) / 2
            print(ti, t_mid, t0, np.log(sol[-1, :]) - np.sum(np.log(const)))
            tt = np.linspace(T - ti, T - t_mid, 2)
            sol, success = lsoda(funcptr, y0, tt)
        print(ti, t_mid, t0, np.log(sol[-1, :]) - np.sum(np.log(const)))
        if t_mid == t0:
            # return np.minimum(np.maximum(sol[-1, :] / y0[l], 0), 1)
            return sol, const
        else:
            ti = t_mid
            y0 = sol[-1, :]
            const.append(1 / max(y0))
            y0 *= 1048576 / max(y0)
        # const = [y0[l]]
        # y0 = sol[-1, :]
        # const.append(1048576 / max(y0))
        # y0 *= 1048576 / max(y0)
        # tt = np.linspace(T - t_mid, T - t0, 2)
        # sol, success = lsoda(funcptr, y0, tt)
        # print(y0, sol)
        # return sol / const


    # while (not success or np.any(sol[-1, :] <= 0) or np.any(sol[-1, :] >= y0[l]) or np.any(np.isnan(sol[-1, :]))) \
    #         and y0[l] < np.power(2, 10):
    #     y0[l] *= 128
    #     sol, success = lsoda(funcptr, y0, tt)
    # return np.minimum(np.maximum(sol[-1, :] / y0[l], 0), 1)
    return sol / y0[l]


def get_rescale_factors(loglikelihood_array):
    """
    Checks if the input (log)array is too small/large, and return a factor of e to multiply it by.

    :param loglikelihood_array: numpy array containing the loglikelihood to be rescaled
    :return: float, factor of e by which the likelihood array should be multiplied.
    """

    max_limit = MAX_VALUE
    min_limit = MIN_VALUE

    non_zero_loglh_array = loglikelihood_array[loglikelihood_array > -np.inf]
    min_lh_value = np.min(non_zero_loglh_array)
    max_lh_value = np.max(non_zero_loglh_array)

    factors = 0

    if max_lh_value > max_limit:
        factors = max_limit - max_lh_value - 1
    elif min_lh_value < min_limit:
        factors = min(min_limit - min_lh_value + 1, max_limit - max_lh_value - 1)
    return factors


@nb.njit(parallel=True)
def calc_node_Ps(tis, t0s, ls, m, T, funcptr):

    n = len(tis)
    result = np.zeros((n, m), np.float64)

    for i in nb.prange(n):
        ti = tis[i]
        l = ls[i]
        t0 = t0s[i]

        y0 = np.zeros(m, np.float64)
        y0[l] = 1

        if t0 == ti:
            result[i] = y0
        else:
            y0[l] = 16384
            # Note that LSODA needs the time interval to be ascending: we will therefore use reversed time for it,
            # going from the last sampled tip till the root
            tt = np.linspace(T - ti, T - t0, 5)
            # integrate with lsoda method
            sol, success = lsoda(funcptr, y0, tt)

            # while not success or np.any(sol[-1, :] <= 0) or np.any(sol[-1, :] >= y0[l]) or np.any(np.isnan(sol[-1, :])):
            #
            #
            #     y0[l] *= 16
            #     sol, success = lsoda(funcptr, y0, tt)
            # TODO: if there is a problem, try to restart from the rescaled middle point
            result[i] = np.minimum(np.maximum(sol[-1, :] / y0[l], 0), 1)
            if not success or np.any(sol[-1, :] <= 0) or np.any(sol[-1, :] >= y0[l]) or np.any(np.isnan(sol[-1, :])):
                print('Weird:', ti, t0, T, sol / y0[l], success, '\n')

    return result


def loglikelihood_known_states(forest, T, MU, LA, PSI, RHO, u=-1, ls=None, nodes=None, t0s=None, tis=None):
    """
    Calculates loglikelihood for a given forest of trees,
    whose nodes are annotated with their state ids in 1:m (via feature STATE_K),
    and their times (via feature TI), under given MTBD model parameters.

    :param forest: a list of ete3.Tree trees
    :param T: time at end of the sampling period
    :param MU: an array of state transition rates
    :param LA: an array of transmission rates
    :param PSI: an array of removal rates
    :param RHO: an array of sampling probabilities
    :param u: number of hidden trees, where no tip got sampled
    :return: the value of loglikelihood
    """
    PI = state_frequencies(MU, LA, PSI)
    LOG_PSI_RHO = np.log(PSI) + np.log(RHO)
    SIGMA = MU.sum(axis=1) + LA.sum(axis=1) + PSI
    u_sol, u_tt = compute_U_lsoda(T, MU=MU, LA=LA, PSI=PSI, RHO=RHO, SIGMA=SIGMA)

    # if threads < 1:
    #     threads = max(os.cpu_count(), 1)

    if ls is None or nodes is None or t0s is None or tis is None:
        ls, nodes, t0s, tis = get_node_metrics(forest)

    rhs = make_lsoda_func_P(u_sol, u_tt, MU, LA, SIGMA, T)
    funcptr = rhs.address  # address to ODE function
    Ps = calc_node_Ps(tis, t0s, ls, len(MU), T, funcptr)
    n2p = dict(zip(nodes, Ps))

    # def _work(args):
    #     n, MU, LA, SIGMA, T, u_sol, u_tt = args
    #     ti = getattr(n, TI)
    #     l = getattr(n, STATE_K)
    #     t0 = ti - n.dist
    #     P = get_P_lsoda(ti=ti, l=l, t0=t0, u_sol=u_sol, u_tt=u_tt, MU=MU, LA=LA, SIGMA=SIGMA, T=T)
    #     return n, P
    #
    # iterable = chain(*(((n, MU, LA, SIGMA, T, u_sol, u_tt) for n in tree.traverse()) for tree in forest))
    #
    # if threads > 1:
    #     with ThreadPool(processes=threads) as pool:
    #         acr_results = \
    #             pool.map(func=_work, iterable=iterable)
    # else:
    #     acr_results = [_work(args) for args in iterable]
    #
    # n2p = dict(acr_results)
    # print(n2p)

    hidden_probability = PI.dot(get_value(T, u_sol, u_tt))
    if u < 0:
        u = len(forest) * hidden_probability / (1 - hidden_probability)

    res = 0 if not u else u * np.log(hidden_probability)
    for tree in forest:
        for n in tree.traverse('preorder'):
            k = getattr(n, STATE_K)
            if n.is_root() and n.dist:
                P = n2p[n]
                res += np.log(PI.dot(P))
            if n.is_leaf():
                res += LOG_PSI_RHO[k]
            else:
                LA_k = LA[k, :]
                lc, rc = n.children
                P_lc, P_rc = n2p[lc], n2p[rc]
                # res += np.log(P_lc[k] * LA_k.dot(P_rc) + P_rc[k] * LA_k.dot(P_lc))
                left_donor = np.log(P_lc[k]) + np.log(LA_k.dot(P_rc))
                right_donor = np.log(P_rc[k]) + np.log(LA_k.dot(P_lc))
                max_factors = max(get_rescale_factors(left_donor), get_rescale_factors(right_donor))
                res += np.log(np.exp(left_donor + max_factors) + np.exp(right_donor + max_factors)) - max_factors

            if np.isnan(res):
                break

    if np.isnan(res):
        res = -np.inf
    return res


def get_node_metrics(forest):
    nodes, tis, t0s, ls = [], [], [], []
    for tree in forest:
        for n in tree.traverse():
            nodes.append(n)
            ti = getattr(n, TI)
            tis.append(ti)
            t0s.append(ti - n.dist)
            ls.append(getattr(n, STATE_K))
    nodes = np.array(nodes)
    tis = np.array(tis, dtype=np.float64)
    t0s = np.array(t0s, dtype=np.float64)
    ls = np.array(ls, dtype=np.int)
    return ls, nodes, t0s, tis


def optimize_likelihood_params(forest, model, T, optimise, u=-1, bounds=None):
    """
    Optimizes the likelihood parameters for a given forest and a given MTBD model.


    :param forest: a list of ete3.Tree trees, annotated with node states and times via features STATE_K and TI.
    :param T: time at end of the sampling period
    :param model: MTBD model containing starting parameter values
    :param optimise: MTBD model whose rates indicate which parameters need to optimized:
        positive rates correspond to optimized parameters
    :param u: number of hidden trees, where no tip got sampled
    :return: the values of optimized parameters and the corresponding loglikelihood: (MU, LA, PSI, RHO, best_log_lh)
    """
    MU, LA, PSI, RHO = model.transition_rates, model.transmission_rates, model.removal_rates, model.ps

    opt_transition_rates = (optimise.transition_rates > 0)
    opt_transmission_rates = (optimise.transmission_rates > 0)
    opt_removal_rates = (optimise.removal_rates > 0)
    opt_ps = (optimise.ps > 0)
    n_mu = opt_transition_rates.sum()
    n_la = opt_transmission_rates.sum()
    n_psi = opt_removal_rates.sum()
    n_p = opt_ps.sum()

    if bounds is None:
        bounds = []
        bounds.extend([[1e-3, 1e2]] * (n_mu + n_la + n_psi))
        bounds.extend([[1e-3, 1 - 1e-3]] * n_p)
    bounds = np.array(bounds, np.float64)

    def get_real_params_from_optimised(ps):
        ps = np.maximum(np.minimum(ps, bounds[:, 1]), bounds[:, 0])
        MU[opt_transition_rates] = ps[:n_mu]
        LA[opt_transmission_rates] = ps[n_mu: n_mu + n_la]
        PSI[opt_removal_rates] = ps[n_mu + n_la: n_mu + n_la + n_psi]
        RHO[opt_ps] = ps[n_mu + n_la + n_psi:]

    def get_optimised_params_from_real():
        return np.append(
            np.append(
                np.append(MU[opt_transition_rates],
                          LA[opt_transmission_rates]),
                PSI[opt_removal_rates]),
            RHO[opt_ps])

    ls, nodes, t0s, tis = get_node_metrics(forest)

    def get_v(ps):
        if np.any(pd.isnull(ps)):
            return np.nan
        get_real_params_from_optimised(ps)
        res = loglikelihood_known_states(forest, T, MU, LA, PSI, RHO, u=u, ls=ls, nodes=nodes, t0s=t0s, tis=tis)
        # print(ps, "\t-->\t", res)
        return -res

    x0 = get_optimised_params_from_real()
    x0 = np.maximum(np.minimum(x0, bounds[:, 1]), bounds[:, 0])
    best_log_lh = -get_v(x0)

    for i in range(5):
        if i == 0:
            vs = x0
        else:
            vs = np.random.uniform(bounds[:, 0], bounds[:, 1])

        fres = minimize(get_v, x0=vs, method='Powell', bounds=bounds)
        # fres = minimize(get_v, x0=vs, method='L-BFGS-B', bounds=bounds)
        if not np.any(np.isnan(fres.x)):
            if -fres.fun >= best_log_lh:
                x0 = fres.x
                best_log_lh = -fres.fun
                # break
            print('Attempt {} of trying to optimise the parameters: {} -> {} ({}).'
                  .format(i, fres.x, -fres.fun, fres.message))
    get_real_params_from_optimised(x0)
    return MU, LA, PSI, RHO, best_log_lh
