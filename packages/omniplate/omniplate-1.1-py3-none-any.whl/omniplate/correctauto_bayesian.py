"""A Bayesian version of the method in Lichten ... Swain, BMC Biophys 2014."""

# TODO
# why is the predicted fluorescence so low? refstrain at wrong OD?

import numpy as np
from scipy.optimize import minimize
from tqdm import tqdm

import omniplate.corrections as omcorr
import omniplate.omgenutils as gu
import omniplate.sunder as sunder

rng = np.random.default_rng()

# notation follows Lichten ... Swain
# GFP is denoted y; AutoFL is denoted z.
# The reference strain is denoted WT.


def de_nan(y, z):
    """Remove any replicates with NaN."""
    # NaNs are generated because experiments have different durations
    keep = ~np.any(np.isnan(y), axis=0)
    return y[:, keep], z[:, keep]


def sample_b(nosamples, bdata):
    """Sample background fluorescence assuming log normal distribution."""
    logbdata = np.log(bdata)
    u = np.mean(logbdata)
    sig = np.std(logbdata)
    samples = rng.lognormal(u, sig, nosamples)
    return samples


def get_background_samples(yn, zn, nosamples):
    """Get samples of background fluorescence for GFP and AutoFL."""
    by = sample_b(nosamples, yn)
    bz = sample_b(nosamples, zn)
    return by, bz


def set_up(y, z, ywt, zwt, yn, zn):
    """Define stats_dict."""
    stats_dict = {
        "x0": None,  # initial guess for g, ra, a
        "gmax": np.max(y),
        "amax": np.max(ywt),
        "ramin": 0,
        "ramax": 1,
        "seq_prior_mu": None,
        "seq_prior_hess": None,
    }
    return stats_dict


def minus_log_prob_array(theta, stats_dict):
    """Get log normal probability."""
    g, ra, a = theta
    rg = stats_dict["rg"]
    n = stats_dict["n"]
    sy = stats_dict["sy"]
    sz = stats_dict["sz"]
    sywt = stats_dict["sywt"]
    szwt = stats_dict["szwt"]
    by = stats_dict["by"]
    bz = stats_dict["bz"]
    bywt = stats_dict["by"]
    bzwt = stats_dict["bz"]
    ly = stats_dict["ly"]
    lz = stats_dict["lz"]
    lywt = stats_dict["lywt"]
    lzwt = stats_dict["lzwt"]
    mlp_v = np.sum(
        n * np.log(sy * sz * sywt * szwt)
        + (np.log(a + g + by) - ly) ** 2 / (2 * sy**2)
        + (np.log(a * ra + g * rg + bz) - lz) ** 2 / (2 * sz**2)
        + (np.log(a + bywt) - lywt) ** 2 / (2 * sywt**2)
        + (np.log(a * ra + bzwt) - lzwt) ** 2 / (2 * szwt**2),
        axis=0,
    )
    return mlp_v


def minus_log_prob(theta, stats_dict):
    """Find joint probability averaged over background fluorescence."""
    mlp_v = minus_log_prob_array(theta, stats_dict)
    mlp = average_background_fluorescence(mlp_v)
    return mlp


def average_background_fluorescence(mlp, deriv=None):
    """Average background fluorescence."""
    norm = np.min(mlp)
    # normalise to prevent underflows, exponentiate, then average
    norm_prob = np.exp(norm - mlp)
    if deriv is None:
        # revert normalisation and return -log(probability)
        minus_log_prob = norm - np.log(np.mean(norm_prob))
        return minus_log_prob
    else:
        # return weighted average of a derivative array
        # used for jacobian and hessian
        deriv_average = np.sum(deriv * norm_prob) / np.sum(norm_prob)
        return deriv_average


def jac_arrays(theta, stats_dict):
    """Get Jacobian of log normal probability."""
    g, ra, a = theta
    rg = stats_dict["rg"]
    sy = stats_dict["sy"]
    sz = stats_dict["sz"]
    sywt = stats_dict["sywt"]
    szwt = stats_dict["szwt"]
    by = stats_dict["by"]
    bz = stats_dict["bz"]
    bywt = stats_dict["by"]
    bzwt = stats_dict["bz"]
    ly = stats_dict["ly"]
    lz = stats_dict["lz"]
    lywt = stats_dict["lywt"]
    lzwt = stats_dict["lzwt"]
    jac_v = np.zeros(3, dtype="object")
    y_v = (np.log(a + g + by) - ly) / (sy**2 * (a + g + by))
    z_v = (np.log(a * ra + g * rg + bz) - lz) / (
        sz**2 * (a * ra + g * rg + bz)
    )
    ywt_v = (np.log(a + bywt) - lywt) / (sywt**2 * (a + bywt))
    zwt_v = (np.log(a * ra + bzwt) - lzwt) / (szwt**2 * (a * ra + bzwt))
    # with respect to g
    jac_v[0] = np.sum(y_v + rg * z_v, axis=0)
    # with respect to ra
    jac_v[1] = np.sum(a * (z_v + zwt_v), axis=0)
    # with respect to a
    jac_v[2] = np.sum(y_v + ywt_v + ra * (z_v + zwt_v), axis=0)
    return jac_v


def jac(theta, stats_dict, return_jac_v=False):
    """Get Jacobian averaged over background fluorescence."""
    jac_v = jac_arrays(theta, stats_dict)
    # average background fluorescence
    mlp_v = minus_log_prob_array(theta, stats_dict)
    av_jac = np.array(
        [average_background_fluorescence(mlp_v, jac_v[i]) for i in range(3)]
    )
    if return_jac_v:
        return av_jac, jac_v
    else:
        return av_jac


def hess_arrays(theta, stats_dict):
    """Get Hessian of log normal probability."""
    g, ra, a = theta
    rg = stats_dict["rg"]
    sy = stats_dict["sy"]
    sz = stats_dict["sz"]
    sywt = stats_dict["sywt"]
    szwt = stats_dict["szwt"]
    by = stats_dict["by"]
    bz = stats_dict["bz"]
    bywt = stats_dict["by"]
    bzwt = stats_dict["bz"]
    ly = stats_dict["ly"]
    lz = stats_dict["lz"]
    lywt = stats_dict["lywt"]
    lzwt = stats_dict["lzwt"]
    hess_v = np.zeros((3, 3), dtype="object")
    y_v = (1 - np.log(a + g + by) + ly) / (sy**2 * (a + g + by) ** 2)
    z_v = (1 - np.log(a * ra + g * rg + bz) + lz) / (
        sz**2 * (a * ra + g * rg + bz) ** 2
    )
    ywt_v = (1 - np.log(a + bywt) + lywt) / (sywt**2 * (a + bywt) ** 2)
    zwt_v = (1 - np.log(a * ra + bzwt) + lzwt) / (
        szwt**2 * (a * ra + bzwt) ** 2
    )
    z_vv = (np.log(a * ra + g * rg + bz) - lz) / (
        sz**2 * (a * ra + g * rg + bz)
    )
    zwt_vv = (np.log(a * ra + bzwt) - lzwt) / (szwt**2 * (a * ra + bzwt))
    # g, g
    hess_v[0, 0] = y_v + rg**2 * z_v
    # ra, ra
    hess_v[1, 1] = a**2 * (z_v + zwt_v)
    # a, a
    hess_v[2, 2] = y_v + ywt_v + ra**2 * (z_v + zwt_v)
    # g, ra
    hess_v[0, 1] = a * rg * z_v
    # g, a
    hess_v[0, 2] = y_v + ra * rg * z_v
    # ra, a
    hess_v[1, 2] = a * ra * (z_v + zwt_v) + z_vv + zwt_vv
    # sum over replicates
    for i in range(3):
        for j in range(i, 3):
            hess_v[i, j] = np.sum(hess_v[i, j], axis=0)
            if j > i:
                hess_v[j, i] = hess_v[i, j]
    return hess_v


def hess(theta, stats_dict):
    """Get Hessian averaged over background fluorescence."""
    mlp_v = minus_log_prob_array(theta, stats_dict)
    av_jac, jac_v = jac(theta, stats_dict, return_jac_v=True)
    hess_v = hess_arrays(theta, stats_dict)
    av_hess = np.empty((3, 3))
    for i in range(3):
        for j in range(i, 3):
            av_hess[i, j] = (
                average_background_fluorescence(mlp_v, hess_v[i, j])
                + av_jac[i] * av_jac[j]
                - average_background_fluorescence(mlp_v, jac_v[i] * jac_v[j])
            )
            if j > i:
                av_hess[j, i] = av_hess[i, j]
    return av_hess


def set_up_minimization(stats_dict):
    """Set up bounds and initial guess."""
    g_bounds = (0, stats_dict["gmax"])
    ra_bounds = (stats_dict["ramin"], stats_dict["ramax"])
    a_bounds = (0, stats_dict["amax"])
    bounds = [g_bounds, ra_bounds, a_bounds]
    x0_o = np.array(
        [
            np.median(np.exp(stats_dict["ly"])),
            np.median(np.exp(stats_dict["lzwt"] - stats_dict["lywt"])),
            np.median(np.exp(stats_dict["lywt"])),
        ]
    )
    if stats_dict["x0"] is None:
        x0 = x0_o
    else:
        x0 = stats_dict["x0"]
    return bounds, x0, x0_o


def find_mode(stats_dict, no_attempts):
    """Find most probable value of g, ra, and a."""
    # Tried with a sequential approach, using a Gaussian
    # approximation of the current posterior as the prior
    # for the future one, but performs worse, perhaps because
    # of the wide hessian.
    bounds, x0, x0_o = set_up_minimization(stats_dict)
    min_mlp = np.inf
    mode = None
    rands = rng.standard_normal((no_attempts, 3))
    for i in range(no_attempts):
        if i < int(no_attempts / 2):
            # start from proceeding optimum
            sampled_x0 = rands[i, :] * 10 * np.sqrt(x0) + x0
        else:
            # start from a new guess
            sampled_x0 = rands[i, :] * 10 * np.sqrt(x0_o) + x0_o
        sampled_x0[sampled_x0 < 0] = 0.01
        res = minimize(
            lambda x: minus_log_prob(x, stats_dict),
            x0=sampled_x0,
            bounds=bounds,
            jac=lambda x: jac(x, stats_dict),
            hess=lambda x: hess(x, stats_dict),
            method="L-BFGS-B",
        )
        if res.success:
            if res.fun < min_mlp:
                mode = res.x
                min_mlp = res.fun
                stats_dict["x0"] = res.x
    if mode is None:
        print(" Warning: Maximising posterior probability failed.")
        mode = np.nan * np.ones(3)
        stats_dict["x0"] = None
    return mode


def correctauto_bayesian(
    self,
    f,
    refstrain,
    flcvfn,
    bd,
    nosamples_for_bg,
    no_minimisation_attempts,
    nosamples,
    experiments,
    experimentincludes,
    experimentexcludes,
    conditions,
    conditionincludes,
    conditionexcludes,
    strains,
    strainincludes,
    strainexcludes,
):
    """
    Correct fluorescence for auto- and background fluorescence.

    Use a Bayesian method to correct for autofluorescence from fluorescence
    measurements at two wavelengths and for background fluorescence.

    Implement demixing following Lichten ... Swain, BMC Biophys 2014.
    Invert
        y = g + a
        z = g * r_g + a * r_a
        ywt = a
        zwt = a * r_a
    where we assume that awt = a.
    """
    print("Using Bayesian approach for two fluorescence wavelengths.")
    print(f"Correcting autofluorescence using {f[0]} and {f[1]}.")
    bname = "bc" + f[0]
    bd_default = {0: (-2, 8), 1: (-2, 4), 2: (2, 9)}
    if bd is not None:
        bdn = gu.mergedicts(original=bd_default, update=bd)
    else:
        bdn = bd_default
    for e in sunder.getset(
        self,
        experiments,
        experimentincludes,
        experimentexcludes,
        "experiment",
        nonull=True,
    ):
        for c in sunder.getset(
            self,
            conditions,
            conditionincludes,
            conditionexcludes,
            labeltype="condition",
            nonull=True,
            nomedia=True,
        ):
            # get data for reference strain
            # y for emission at 525; z for emission at 585
            _, (ywt, zwt) = sunder.extractwells(
                self.r, self.s, e, c, refstrain, f
            )
            ywt, zwt = de_nan(ywt, zwt)
            # get data for Null
            _, (yn, zn) = sunder.extractwells(self.r, self.s, e, c, "Null", f)
            yn, zn = de_nan(yn, zn)
            # check sufficient replicates
            if (ywt.shape[1] < 3) or (yn.shape[1] < 3):
                print(
                    f"There are less than three replicates for the {refstrain}"
                    f" or Null strains in {c}."
                )
                print("Abandoning correctauto.")
                continue
            for s in sunder.getset(
                self,
                strains,
                strainincludes,
                strainexcludes,
                labeltype="strain",
                nonull=True,
            ):
                if (
                    s != refstrain
                    and f"{s} in {c}" in self.allstrainsconditions[e]
                ):
                    # get data for tagged strain
                    t, (y, z, od) = sunder.extractwells(
                        self.r, self.s, e, c, s, f.copy() + ["OD"]
                    )
                    y, z = de_nan(y, z)
                    if y.size == 0 or z.size == 0:
                        print(f"Warning: No data found for {e}: {s} in {c}!!")
                        continue
                    if y.shape[1] < 3:
                        print(
                            "There are less than three replicates"
                            f" for {e}: {s} in {c}."
                        )
                        print("Abandoning correctauto.")
                        continue
                    print(f"{e}: {s} in {c}")
                    # check if predicted_fl already estimated
                    df = self.s.query(
                        "experiment == @e and condition == @c "
                        "and strain == @s"
                    )
                    if f"predicted_{f[0]}" in df.columns:
                        potential_predicted_fl = (
                            df[f"predicted_{f[0]}"].dropna().values
                        )
                    if (
                        "potential_predicted_fl" in locals()
                        and potential_predicted_fl.size == t.size
                    ):
                        print("Using existing predicted fluorescence.")
                        predicted_fl = potential_predicted_fl
                    else:
                        # correct autofluorescence for each time point
                        predicted_fl = np.zeros(t.size)
                        stats_dict = set_up(y, z, ywt, zwt, yn, zn)
                        stats_dict["rg"] = self._gamma
                        stats_dict["n"] = y.shape[1]
                        for i in tqdm(range(t.size)):
                            stats_dict["by"], stats_dict["bz"] = (
                                get_background_samples(
                                    yn[i, :], zn[i, :], nosamples_for_bg
                                )
                            )
                            stats_dict["sy"] = np.std(np.log(y[i, :]))
                            stats_dict["sz"] = np.std(np.log(z[i, :]))
                            stats_dict["sywt"] = np.std(np.log(ywt[i, :]))
                            stats_dict["szwt"] = np.std(np.log(zwt[i, :]))
                            stats_dict["ly"] = np.log(y[i, :])[:, None]
                            stats_dict["lz"] = np.log(z[i, :])[:, None]
                            stats_dict["lywt"] = np.log(ywt[i, :])[:, None]
                            stats_dict["lzwt"] = np.log(zwt[i, :])[:, None]
                            posterior_mode = find_mode(
                                stats_dict, no_minimisation_attempts
                            )
                            predicted_fl[i] = posterior_mode[0]
                    # smooth with GP and add to data frames
                    # gives better errors than smoothing samples of flperod
                    print("Smoothing...")
                    flperod = omcorr.sample_flperod_with_GPs(
                        self,
                        bname,
                        t,
                        predicted_fl,
                        od,
                        flcvfn,
                        bdn,
                        nosamples,
                        e,
                        c,
                        s,
                        max_data_pts=None,  # predicted_fl is 1D
                        figs=True,
                        logs=False,
                    )
                    # store results for fluorescence per OD
                    autofdict = {
                        "experiment": e,
                        "condition": c,
                        "strain": s,
                        "time": t,
                        f"predicted_{f[0]}": predicted_fl,
                        f"{bname}perOD": np.mean(flperod, 1),
                        f"{bname}perOD_err": omcorr.nanstdzeros2nan(
                            flperod, 1
                        ),
                    }
                    # add to data frames
                    omcorr.addtodataframes(self, autofdict)
                    print("---")
