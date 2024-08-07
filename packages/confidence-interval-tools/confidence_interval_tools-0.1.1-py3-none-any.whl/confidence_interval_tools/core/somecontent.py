# seaborn.lineplot(data=newdata, x=newdata.index, y='y mean', color='lavender', alpha=0.7)

### figure size
fig = plt.figure(figsize=(8, 6))
### grid
plt.grid(visible=True, which="both", color="gray", alpha=0.2)

### CI
# seaborn.lineplot(data=newdata, x=newdata.index, y=newdata['y mean']+1*newdata['y std'], color='lightpink', linestyle='--', alpha=0.5)
# seaborn.lineplot(data=newdata, x=newdata.index, y=newdata['y mean']-1*newdata['y std'], color='lightpink', linestyle='--', alpha=0.5)
###
plt.vlines(
    x=newdata.index,
    ymin=newdata["y mean"] - 1 * newdata["y std"],
    ymax=newdata["y mean"] + 1 * newdata["y std"],
    color="gray",
    linestyles="dotted",
    alpha=0.5,
)
ci_ends_width = (
    (numpy.max(newdata.index) - numpy.min(newdata.index) + 1) / len(newdata.index) * 0.4
)
plt.hlines(
    y=newdata["y mean"] - 1 * newdata["y std"],
    xmin=newdata.index - ci_ends_width / 2,
    xmax=newdata.index + ci_ends_width / 2,
    color="gray",
    linestyles="solid",
    alpha=0.5,
)
plt.hlines(
    y=newdata["y mean"] + 1 * newdata["y std"],
    xmin=newdata.index - ci_ends_width / 2,
    xmax=newdata.index + ci_ends_width / 2,
    color="gray",
    linestyles="solid",
    alpha=0.5,
)
###
plt.fill_between(
    x=newdata.index,
    y1=newdata["y mean"] - 1 * newdata["y std"],
    y2=newdata["y mean"] + 1 * newdata["y std"],
    color="lavender",
    alpha=0.4,
)

### scatterplot
seaborn.scatterplot(
    data=newdata,
    x=newdata.index,
    y="y mean",
    hue="origin cluster",
    palette="rainbow_r",
    marker=".",
    s=100,
    alpha=1,
)


linregress = sps.linregress
genpareto = sps.genpareto


# Function for normalizing data
def normalize(
    data: pandas.DataFrame | numpy.ndarray | list | numpy.float64 | int,
    data_min: int | numpy.float64 | None = None,
    data_max: int | numpy.float64 | None = None,
) -> pandas.DataFrame | numpy.ndarray | int | numpy.float64:
    """Apply minmax normalization on the given data (pandas.DataFrame or numpy.array or list or single number)."""
    if isinstance(data_min, type(None)):
        if isinstance(data, pandas.DataFrame):
            data_min = data.min()
        else:
            data_min = numpy.min(data)
    if isinstance(data_max, type(None)):
        if isinstance(data, pandas.DataFrame):
            data_max = data.max()
        else:
            data_max = numpy.max(data)
    return (data - data_min) / (data_max - data_min)


# Function for "denormalizing" data after normalization
def denormalize(
    normalized_x_or_y_data: (
        pandas.DataFrame | numpy.ndarray | list | numpy.float64 | int
    ),
    data_min: int | numpy.float64,
    data_max: int | numpy.float64,
) -> pandas.DataFrame | numpy.ndarray | int | numpy.float64:
    """Apply minmax denormalization. Minimum and maximum values are not optional here."""
    return normalized_x_or_y_data * (data_max - data_min) + data_min


# test : output clustering function
def clustering(input, size=None, offset=0):
    if len(numpy.asarray([input]).T) >= 2:
        # print("this is an array")
        output = numpy.asarray(input).copy()
        if not isinstance(size, type(None)):
            output = (
                numpy.round((numpy.asarray(output) - offset) * (1 / size))
                + (offset / size)
            ) / (1 / size)
    else:
        # print("this is a number")
        output = input
        if not isinstance(size, type(None)):
            output = (numpy.round((output - offset) * (1 / size)) + (offset / size)) / (
                1 / size
            )
    return output


# test : min_max filter
def min_max_filter(input, min_filter=None, max_filter=None):
    if len(numpy.asarray([input]).T) >= 2:
        # print("this is an array")
        output = numpy.asarray(input).copy()
        if not isinstance(min_filter, type(None)):
            output[numpy.where(numpy.asarray(output) < min_filter)] = min_filter
        if not isinstance(max_filter, type(None)):
            output[numpy.where(numpy.asarray(output) > max_filter)] = max_filter
    else:
        # print("this is a number")
        output = input
        if not isinstance(min_filter, type(None)):
            if output < min_filter:
                output = min_filter
        if not isinstance(max_filter, type(None)):
            if output > max_filter:
                output = max_filter
    return output


# minimum difference between any two numbers in a numpy array
def min_abs_diff(a):
    if len(a) > 2:
        return numpy.min(
            numpy.array(
                [
                    numpy.abs(a - numpy.roll(a, i))
                    for i in range(1, int(numpy.ceil(len(a) / 2)))
                ]
            )
        )
    else:
        return numpy.abs(a[1] - a[0])


# average difference between any two numbers in a numpy array
def mean_abs_diff(a):
    if len(a) > 2:
        return numpy.mean(
            numpy.array(
                [
                    numpy.abs(a - numpy.roll(a, i))
                    for i in range(1, int(numpy.ceil(len(a) / 2)))
                ]
            )
        )
    else:
        return numpy.abs(a[1] - a[0])


# Data
v = pandas.Series([1, 1, 1, 2, 3, 3, 5, 5, 5, 6, 6, 7, 7, 7, 7, 9, 11, 15, 21])
# v = pandas.Series([3, 15])

threshold_list = []
mean_excess_list = []
tail_start = 0.5
for i in numpy.arange(tail_start, 1 - 0.001, 0.025):
    # print(i)
    threshold = v.quantile(i)
    excess = v[v > threshold] - threshold
    mean_excess = excess.mean()
    threshold_list.append(threshold)
    mean_excess_list.append(mean_excess)

seaborn.scatterplot(x=threshold_list, y=mean_excess_list)

result = linregress(x=threshold_list, y=mean_excess_list)

xrange = numpy.arange(
    numpy.min(threshold_list), numpy.max(threshold_list) + 0.001, 0.05
)
seaborn.lineplot(x=xrange, y=result.slope * xrange + result.intercept)

evi = result.slope
k = result.intercept


plt.figure()
qrange = numpy.arange(0, 1.001, 0.01)
seaborn.lineplot(
    x=qrange,
    y=denormalize(
        genpareto.cdf(v.quantile(qrange) - v.quantile(tail_start), evi, 0, k),
        tail_start,
        1,
    ),
)
seaborn.lineplot(
    x=qrange,
    y=denormalize(
        genpareto.cdf(
            v.quantile(qrange) - v.quantile(tail_start),
            numpy.quantile([evi - 1.96 * result.stderr, evi + 1.96 * result.stderr], 0),
            0,
            numpy.quantile(
                [
                    k - 1.96 * result.intercept_stderr,
                    k + 1.96 * result.intercept_stderr,
                ],
                0,
            ),
        ),
        tail_start,
        1,
    ),
)
seaborn.lineplot(
    x=qrange,
    y=denormalize(
        genpareto.cdf(
            v.quantile(qrange) - v.quantile(tail_start),
            numpy.quantile([evi - 1.96 * result.stderr, evi + 1.96 * result.stderr], 1),
            0,
            numpy.quantile(
                [
                    k - 1.96 * result.intercept_stderr,
                    k + 1.96 * result.intercept_stderr,
                ],
                1,
            ),
        ),
        tail_start,
        1,
    ),
)


print(
    v.quantile(tail_start),
    v.quantile(tail_start)
    + genpareto.ppf(
        normalize(0.975, tail_start, 1),
        numpy.quantile([evi - 1.96 * result.stderr, evi + 1.96 * result.stderr], 0.5),
        0,
        numpy.quantile(
            [k - 1.96 * result.intercept_stderr, k + 1.96 * result.intercept_stderr],
            0.5,
        ),
    ),
)


### Quantiles with Hutson (2002) ####
### According to Banfi, F., Cazzaniga, G. & De Michele, C. (2022). https://doi.org/10.1007/s00477-021-02102-0

### Data
v = pandas.Series([1, 1, 1, 2, 3, 3, 5, 5, 5, 6, 6, 7, 7, 7, 7, 9, 11, 15, 21])
# v = pandas.Series([3, 15])
n = len(v)
print("n =", n)

Y = v.sort_values(ascending=False).reset_index(drop=True)

u = 0.975
u1 = 1 - 1 / (len(v) + 1)  ## where the current maximum will be placed, it seems


### different extrapolations or interpolations, depending on whether we are within the range of observed data or not
if (u > 0) and (u <= 1 / (n + 1)):
    Y_h = Y[n - 1] + (Y[n - 2] - Y[n - 1]) * numpy.log((n + 1) * u)
elif (u > 1 / (n + 1)) and (u < n / (n + 1)):
    print((n) - numpy.floor((n + 1) * u), (n - 1) - numpy.floor((n + 1) * u))
    Y_h = (1 - ((n + 1) * u - numpy.floor((n + 1) * u))) * Y[
        (n) - numpy.floor((n + 1) * u)
    ] + ((n + 1) * u - numpy.floor((n + 1) * u)) * Y[(n - 1) - numpy.floor((n + 1) * u)]
elif (u >= n / (n + 1)) and (u < 1):
    Y_h = Y[0] - (Y[0] - Y[1]) * numpy.log((n + 1) * (1 - u))
else:
    Y_h = numpy.nan  ## undefined for u values below 0 or beyond 1


print(Y.values, [Y.quantile(q=u)], [Y_h])

### Note: this seems to rely on the assumption that a new datapoint would be equally likely to be placed
### anywhere in the sorted data list. This might be quite an "acceptable" assumption for large datasets,
### but for smaller datasets this might be misleading... TODO: read more about this method and correct if necessary.

### Note 2: this method does not seem to rely on the cumulative probability distribution at all.
### It "automatically" scales down the observed quantiles, by associating q=1 to q=(1 - 1/(n+1)).
### This implies that the probability of future data lying beyond the currently observed maximum
### is estimated to be 1/(n+1) in all cases.
### Furthermore, it seems the estimated probability distribution is asymmetric and doesn't conserve the
### location of the median.


#### Quantiles with  Scholz (1995) ####
### According to Banfi, F., Cazzaniga, G. & De Michele, C. (2022). https://doi.org/10.1007/s00477-021-02102-0
### Here, the estimate is (approximately) the center of the confidence interval for the expected location of u

### Note: it is unclear how to estimate small quantile values with this method.
### Inverting the order of the sorted data seems to work, so this will be used until a more precise method is implemented

### Note 2: in its current form, this method requires at least 12 replicates (y values) for each x

# Data
v = pandas.Series([1, 1, 1, 2, 3, 3, 5, 5, 5, 6, 6, 7, 7, 7, 7, 9, 11, 15, 21])
# v = pandas.Series(numpy.random.default_rng().normal(10, 5, 20))
n = len(v)
u = pandas.Series([0.025, 0.05, 0.5, 0.90, 0.95, 0.975])
print(v.std())

SC0 = pandas.DataFrame(index=[1], columns=["EVI", "b1", "b2", "R2"])
SC7 = pandas.DataFrame(index=[1], columns=["EVI", "b1", "b2", "R2"])
Y_s_0 = pandas.DataFrame()
Y_s_7 = pandas.DataFrame()

gamma = 0.50
prob = 1 - (numpy.arange(1, n + 1) - 1 / 3) / (n + 1 / 3)
data_median = v.median()
Y = v.sort_values(ascending=False).reset_index(drop=True)
Y_tilde = Y - data_median

### Define the k values that are tested
K1 = numpy.floor(numpy.max([6, 1.3 * numpy.sqrt(n)]))
K2 = 2 * numpy.floor(numpy.log10(n) * numpy.sqrt(n))
if (K2 - K1 + 1) % 2 == 0:
    n_k = K2 - K1
else:
    n_k = K2 - K1 + 1
k_trial = pandas.DataFrame(
    index=range(1, int(n_k + 1)), columns=["k", "R2", "b1", "b2", "c"]
)
print(K1, K2, n_k, Y_tilde.values)

### Parameters' estimation for each k
for index in range(1, int(n_k + 1)):
    k_trial.loc[index, "k"] = K1 + index - 1
    k = k_trial.loc[index, "k"]
    ### EVI estimation
    Y_tilde_k = Y_tilde[k - 1]
    Y_log_ratio = numpy.log(Y_tilde[range(0, int((k - 1)))] / Y_tilde_k)
    M1_k = (1 / (k - 1)) * numpy.sum(Y_log_ratio)
    M2_k = (1 / (k - 1)) * numpy.sum((Y_log_ratio) ** 2)
    if (
        (not numpy.isnan(M2_k)) and (M2_k != 0) and (numpy.isfinite(M2_k))
    ):  ## added condition to avoid value warning
        c_hat_k = M1_k + 1 - 0.5 * (1 - ((M1_k) ** 2 / M2_k)) ** (-1)
        k_trial.loc[index, "c"] = c_hat_k
        ### Covariance matrix of order statistic
        S = pandas.DataFrame(
            index=range(1, int(k + 1)), columns=range(1, int(k + 1))
        ).astype(float)
        for i in range(1, int(k + 1)):
            for j in range(1, int(i + 1)):
                S.loc[i, j] = i ** (-c_hat_k - 1) * j ** (-c_hat_k)
                S.loc[j, i] = S.loc[i, j]
            # end of for loop
        # end of for loop
        ### Least squares solution
        fc_k = (((-n * numpy.log(prob)) ** (-c_hat_k)) - 1) / c_hat_k
        X = pandas.DataFrame(
            {1: [1] * int(k), 2: fc_k[0 : int(k)]}, index=range(1, int(k + 1))
        ).astype(float)
        if (
            numpy.linalg.det(S.values) != 0
        ):  ## Least squares are solved only if S is invertible
            ### TODO: simplify the equation for b with existing fitting libraries?
            ### TODO: use regression stderr to estimate a confidence interval for b1 and b2
            b = numpy.matmul(
                numpy.linalg.inv(
                    numpy.matmul(
                        numpy.matmul(X.T.values, numpy.linalg.inv(S.values)), X.values
                    )
                ),
                numpy.matmul(
                    numpy.matmul(X.T.values, numpy.linalg.inv(S.values)),
                    (Y[0 : int(k)]),
                ),
            )
            print("b =", b)
            k_trial.loc[index, "b1"] = b[0]
            k_trial.loc[index, "b2"] = b[1]
            est = pandas.Series((b[0] + fc_k[0 : int(k)] * b[1]))
            obs = pandas.Series(Y[0 : int(k)])
            TSS = ((obs - obs.mean()) ** 2).sum(skipna=False)
            RSS = ((obs - est) ** 2).sum(skipna=False)
            k_trial.loc[index, "R2"] = 1 - (RSS / TSS)
            print("R2 =", k_trial.loc[index, "R2"])
        else:
            k_trial.loc[index, "R2"] = (
                numpy.nan
            )  ## unnecessary, as pandas already fills with Nan, but kept as it is in the original code
            k_trial.loc[index, "b1"] = numpy.nan
            k_trial.loc[index, "b2"] = numpy.nan
    else:  ## none of the values of interest can be calculated, as c_hat_k is NaN
        k_trial.loc[index, "c"] = numpy.nan
        k_trial.loc[index, "R2"] = numpy.nan
        k_trial.loc[index, "b1"] = numpy.nan
        k_trial.loc[index, "b2"] = numpy.nan
# end of for loop

### Compute optimum EVI and linear regression parameters for SC0
threshold = 0
k_trial = k_trial.loc[k_trial["R2"] > threshold]

### Memorize if no optimum EVI is found for SC0
if k_trial["R2"].isna().all():
    SC0_check_R2 = False
    SC7_check_R2 = False  ## If no optimum EVI is found for SC0, no optimum EVI will be found also for SC7
else:
    SC0_check_R2 = True
    c_mean = k_trial["c"].mean(skipna=True)
    SC0.loc[1, "EVI"] = c_mean
    b1_mean = k_trial["b1"].mean(skipna=True)
    b2_mean = k_trial["b2"].mean(skipna=True)
    SC0.loc[1, "b1"] = b1_mean
    SC0.loc[1, "b2"] = b2_mean
    fc_k = (((-n * numpy.log(prob)) ** (-c_mean)) - 1) / c_mean
    est = pandas.Series((b1_mean + fc_k[0 : int(k)] * b2_mean))
    obs = pandas.Series(Y[0 : int(k)])
    TSS = ((obs - obs.mean()) ** 2).sum(skipna=False)
    RSS = ((obs - est) ** 2).sum(skipna=False)
    SC0.loc[1, "R2"] = 1 - (RSS / TSS)
    Y_s_0 = SC0.loc[1, "b1"] + SC0.loc[1, "b2"] * (
        (((-n * numpy.log(u)) ** (-SC0.loc[1, "EVI"])) - 1) / SC0.loc[1, "EVI"]
    )

if SC0_check_R2 == True:
    ### Compute optimum EVI and linear regression parameters for SC7
    threshold = 0.7
    k_trial = k_trial.loc[k_trial["R2"] > threshold]
    ### Memorize if no optimum EVI is found for SC7
    if k_trial["R2"].isna().all():
        SC7_check_R2 = False
    else:
        SC7_check_R2 = True
        c_mean = k_trial["c"].mean(skipna=True)
        SC7.loc[1, "EVI"] = c_mean
        b1_mean = k_trial["b1"].mean(skipna=True)
        b2_mean = k_trial["b2"].mean(skipna=True)
        SC7.loc[1, "b1"] = b1_mean
        SC7.loc[1, "b2"] = b2_mean
        fc_k = (((-n * numpy.log(prob)) ** (-c_mean)) - 1) / c_mean
        est = pandas.Series((b1_mean + fc_k[0 : int(k)] * b2_mean))
        obs = pandas.Series(Y[0 : int(k)])
        TSS = ((obs - obs.mean()) ** 2).sum(skipna=False)
        RSS = ((obs - est) ** 2).sum(skipna=False)
        SC7.loc[1, "R2"] = 1 - (RSS / TSS)
        ### Calculate extrapolated quantiles for SC0 and SC7 only if optimum EVIs are found
        Y_s_7 = SC7.loc[1, "b1"] + SC7.loc[1, "b2"] * (
            (((-n * numpy.log(u)) ** (-SC7.loc[1, "EVI"])) - 1) / SC7.loc[1, "EVI"]
        )

print(
    u.values,
    v.quantile(q=u.values).values,
    "\nR2>0.0:",
    Y_s_0.values,
    "\nR2>0.7:",
    Y_s_7.values,
)
print("expected (t):", sps.t.ppf(0.975, df=len(v) - 1, loc=v.mean(), scale=v.std()))


v = pandas.Series([1, 1, 1, 2, 3, 3, 5, 5, 5, 6, 6, 7, 7, 7, 7, 9, 11, 15, 21])
v = pandas.Series(numpy.random.default_rng().normal(10, 5, 10))

n = len(v)
t = 0.5
p = 0.975

# print(len(v[v <= v.quantile(p)].values), '|', len(v[v > v.quantile(p)].values))


# Function for normalizing data
def normalize(
    data: pandas.DataFrame | numpy.ndarray | list | numpy.float64 | int,
    data_min: int | numpy.float64 | None = None,
    data_max: int | numpy.float64 | None = None,
) -> pandas.DataFrame | numpy.ndarray | int | numpy.float64:
    """Apply minmax normalization on the given data (pandas.DataFrame or numpy.array or list or single number)."""
    if isinstance(data_min, type(None)):
        if isinstance(data, pandas.DataFrame):
            data_min = data.min()
        else:
            data_min = numpy.min(data)
    if isinstance(data_max, type(None)):
        if isinstance(data, pandas.DataFrame):
            data_max = data.max()
        else:
            data_max = numpy.max(data)
    return (data - data_min) / (data_max - data_min)


# Function for "denormalizing" data after normalization
def denormalize(
    normalized_x_or_y_data: (
        pandas.DataFrame | numpy.ndarray | list | numpy.float64 | int
    ),
    data_min: int | numpy.float64,
    data_max: int | numpy.float64,
) -> pandas.DataFrame | numpy.ndarray | int | numpy.float64:
    """Apply minmax denormalization. Minimum and maximum values are not optional here."""
    return normalized_x_or_y_data * (data_max - data_min) + data_min


### sub-functions for calculating different types of confidence intervals
def scale_and_extrapolate_quantile_value_linear(
    v: pandas.Series,
    q,
    q_scale_min,
    q_scale_max,
    fixed_min=False,
    fixed_max=False,
    fixed_median=False,
    binomial_ci_policy=0.5,
):
    """Linear scaling and extrapolation for quantiles greater than 1 or lower than 0"""
    if fixed_min:
        q_scale_min = 0
    if fixed_max:
        q_scale_max = 1
    if fixed_median:
        ### q_scale_min = 1 - q_scale_max, but we need to decide whether to use q_scale_min or q_scale_max as a reference
        ### use the binomial_ci_policy to extrapolate the extent to which the minimum and maximum contribute to the final scale? (conservative=0, optimistic=1)
        q_scale_max = numpy.quantile(
            [q_scale_min, 1 - q_scale_max], q=(1 - binomial_ci_policy)
        )
        q_scale_min = 1 - q_scale_max
    print(f"q scale: [0, 1] --> [{q_scale_min}, {q_scale_max}]")
    if (normalize(q, q_scale_min, q_scale_max) >= 0) and (
        normalize(q, q_scale_min, q_scale_max) <= 1
    ):
        print(f"q ({q} --> {normalize(q, q_scale_min, q_scale_max)}) in range [0, 1]")
        return v.quantile(normalize(q, q_scale_min, q_scale_max))
    elif (
        normalize(q, q_scale_min, q_scale_max) > 1
    ):  ## references are the last two points
        print(f"q ({q} --> {normalize(q, q_scale_min, q_scale_max)}) > 1")
        ### A = (yb-ya)/(xb-xa); B = (ya - A xa) or (yb - A xb); return A x + B = (yb-ya)/(xb-xa) x + yb - (yb-ya)/(xb-xa) xb = (yb-ya)/(xb-xa)*(x - xb) + yb
        yb, ya = v.quantile(1), v.quantile((len(v) - 2) / (len(v) - 1))
        xb, xa = denormalize(1, q_scale_min, q_scale_max), denormalize(
            (len(v) - 2) / (len(v) - 1), q_scale_min, q_scale_max
        )
        return (yb - ya) / (xb - xa) * (q - xb) + yb
    ## case q < 0 , references are the first two points
    print(f"q ({q} --> {normalize(q, q_scale_min, q_scale_max)}) < 0")
    yb, ya = v.quantile(0), v.quantile((1) / (len(v) - 1))
    xb, xa = denormalize(0, q_scale_min, q_scale_max), denormalize(
        (1) / (len(v) - 1), q_scale_min, q_scale_max
    )
    return (yb - ya) / (xb - xa) * (q - xb) + yb


print("#### Strategy 3.1 ####")

a, b, c, d = t * p * n, t * (1 - p) * n, (1 - t) * p * n, (1 - t) * (1 - p) * n
OddsRatio = (a * d) / (b * c)
logOR = numpy.log(OddsRatio)
SElogOR = numpy.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
logOR_low, logOR_high = (
    logOR - sps.norm.ppf(0.975) * SElogOR,
    logOR + sps.norm.ppf(0.975) * SElogOR,
)
OddsRatio_low, OddsRatio_high = numpy.exp(logOR_low), numpy.exp(logOR_high)
print("OR low/hogh:", (OddsRatio_low, OddsRatio_high))
dk1_l = p / (1 - p) * (OddsRatio_low - 1) / (OddsRatio_low**2 + 1)
k1_l = p / (1 - p) + dk1_l
qh_l = k1_l / (1 + k1_l)
##
dk1_h = p / (1 - p) * (OddsRatio_high - 1) / (OddsRatio_high**2 + 1)
k1_h = p / (1 - p) + dk1_h
qh_h = k1_h / (1 + k1_h)
print("p low/high:", qh_l, qh_h)


print("\n#### Strategy 3.2 ####")

p = 0.975
a, b, c, d = (p**2) * n, p * (1 - p) * n, ((1 - p) ** 2) * n, p * (1 - p) * n
OddsRatio = (a * d) / (b * c)
logOR = numpy.log(OddsRatio)
SElogOR = numpy.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
logOR_low, logOR_high = (
    logOR - sps.norm.ppf(0.975) * SElogOR,
    logOR + sps.norm.ppf(0.975) * SElogOR,
)
OddsRatio_low, OddsRatio_high = numpy.exp(logOR_low), numpy.exp(logOR_high)
print("OR low/hogh:", (OddsRatio_low, OddsRatio_high))
qh_l = numpy.sqrt(OddsRatio_low) / (1 + numpy.sqrt(OddsRatio_low))
qh_h = numpy.sqrt(OddsRatio_high) / (1 + numpy.sqrt(OddsRatio_high))
print(p, "low/high:", qh_l, qh_h)

p = 0.025
a, b, c, d = (p**2) * n, p * (1 - p) * n, ((1 - p) ** 2) * n, p * (1 - p) * n
OddsRatio = (a * d) / (b * c)
logOR = numpy.log(OddsRatio)
SElogOR = numpy.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
logOR_low, logOR_high = (
    logOR - sps.norm.ppf(0.975) * SElogOR,
    logOR + sps.norm.ppf(0.975) * SElogOR,
)
OddsRatio_low, OddsRatio_high = numpy.exp(logOR_low), numpy.exp(logOR_high)
print("OR low/hogh:", (OddsRatio_low, OddsRatio_high))
ql_l = numpy.sqrt(OddsRatio_low) / (1 + numpy.sqrt(OddsRatio_low))
ql_h = numpy.sqrt(OddsRatio_high) / (1 + numpy.sqrt(OddsRatio_high))
print(p, "low/high:", ql_l, ql_h)

print("")
print(v.sort_values().values)
print(
    scale_and_extrapolate_quantile_value_linear(
        v,
        1,
        numpy.quantile([ql_l, ql_h], 1 / (n + 1)),
        numpy.quantile([qh_l, qh_h], 1 - 1 / (n + 1)),
        fixed_min=False,
        fixed_median=False,
        binomial_ci_policy=0,
    ),
    "|",
    v.mean() + 1.96 * v.std(),
)
