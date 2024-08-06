import math
import psutil
import random 
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.stats import qmc
from typing import Callable


# OPTIMIZATION ----------------------------------------------

def round_down_to_nearest_power_of_two(x: int) -> int:
    """rounds down to the nearest power of two"""
    return 1 << (x.bit_length() - 1)


def calculate_optimal_chunk(dimension: int) -> int:
    """given the integration_dim, returns the optimal chunk_size
    
    Args:
        dimensions (int): the number of dimensions over which
            you are storing values

    Returns: 
        int: the optimal chunk size given the available resources
    """
    memory_info = psutil.virtual_memory()
    memory_available_bytes = memory_info.available
    
    usable_memory_bytes = memory_available_bytes / 30
    
    memory_per_sample = 8 * (dimension + 1)
    chunk_size = int(usable_memory_bytes // memory_per_sample)
    
    return round_down_to_nearest_power_of_two(chunk_size)


def next_power_of_two(x: int) -> int:
    """returns the next power of two greater than or equal to x"""
    return 1 << (x - 1).bit_length()


def calculate_num_samples(integration_dim: int, hyperplane: object) -> int:
    """Custom scaling function for the number of samples.
    
    Args: 
        integration_dim (int): The number of dimensions over which you are integrating.
    
    Returns:
        int: The number of samples to use for integration.
    """
    dim_samples = {
        2: 131072,
        6: 16777216,  
    }
    
    if integration_dim <= 2:
        num_samples = dim_samples[2]
    elif integration_dim >= 6:
        num_samples = dim_samples[6]
    else:
        log_scale = (np.log(integration_dim) - np.log(2)) / (np.log(6) - np.log(2))
        num_samples = dim_samples[2] + (dim_samples[6] - dim_samples[2]) * log_scale
    
    num_samples = next_power_of_two(int(num_samples * (hyperplane.coef / 100)))
    
    return num_samples


def scale_binomial(exp: pd.Series, obs: pd.Series) -> pd.Series:
    """scales the observations to align with optimal conditions
    for approximating binomials with normals.
    
    Args: 
        exp (pd.Series): The expected (ground_truth) distribution.
        obs (pd.Series): The observed distribution.
    
    Returns:
        pd.Series: A scaled version of observations that fulfills 
            both np and nq > 10.
    """
    percent_exp = exp / exp.sum()
    total_obs = obs.sum()
    
    min_percent = min(percent_exp.min(), (1-percent_exp).min())
    min_exp = min_percent * total_obs

    scaled_obs = obs * (10 / min_exp)

    return scaled_obs
    

# -----------------------------------------------------------


# OBJECTS ---------------------------------------------------

class Hyperplane():
    """Hyperplane object and functionality"""
    def __init__(self, normal: np.array, coef: float):
        self.normal = normal
        self.coef = coef

    def project_point(self, *point: float) -> np.array:
        """projects a point onto the hyperplane
        
        Args:
            point (floats): the vector/point to project

        Returns:
            np.array: the projected point
        """
        vector = np.array(list(point))

        k = (self.coef - np.dot(self.normal, vector)) / (np.dot(self.normal, self.normal))

        return vector + (k * self.normal)

# -----------------------------------------------------------


# PROBABILITY AND RANDOM VARIABLES --------------------------

def permutate(n: int, r: int) -> int:
    """
    Args:
        n (int): number of objects
        r (int): number you are choosing where order matters

    Returns: 
        int: n permutate r
    """
    return math.factorial(n) / math.factorial(n-r)


def combinate(n: int, r: int) -> int:
    """
    Args:
        n (int): number of objects
        r (int): number you are choosing (order does not matter)

    Returns: 
        int: n combinate r
    """
    return permutate(n=n, r=r) / math.factorial(r)


def discrete_distribution_prob(exp: pd.Series, obs: pd.Series) -> float:
    """takes in the expected distribution and returns the exact probability
    of the observation
    
    Args:
        exp (pd.Series): the ground truth (expected) distribution
        obs (pd.Series): the observed distribution

    Returns:
        float: the probability of observing the observed distribution
            given the expected distribution
    """
    percent_exp = exp / exp.sum()

    prob_freq_df = pd.concat([percent_exp, obs], axis=1)
    prob_freq_df.columns = ['Probability', 'Frequency']

    individual_seq_prob = (prob_freq_df['Probability'] ** prob_freq_df['Frequency']).product()

    to_combinate = obs.sum()
    combinations = 1

    for freq in prob_freq_df['Frequency']:
        combinations *= combinate(n=to_combinate, r=freq)
        to_combinate -= freq

    return (combinations * individual_seq_prob)


def generate_combinations(num_classes: int, num_obs: int) -> set:
    """returns a set of all possible combinations of num_classes integers that 
    add up to num_obs
    
    Args: 
        num_classes (int): number of classes to choose from
        num_obs (int): total number the classes should sum 

    Returns: 
        set: the set of all possible combinations of class values that 
            add up to num_obs
    """
    memo = {(0, 0): {()}}

    for i in range(1, num_classes + 1):
        for (_, errors), seqs in {k: v for k, v in memo.items() if k[0] == i-1}.items():
            for error_amt in range(0, num_obs - errors + 1):

                if (i, errors + error_amt) in memo:
                    memo[(i, errors + error_amt)].update({(error_amt,) + combo for combo in seqs})
                else:
                    memo[(i, errors + error_amt)] = {(error_amt,) + combo for combo in seqs}

    return memo[(num_classes, num_obs)]


def generate_normal_exponent(mean: float, std_dev: float) -> Callable:
    """given a mean and standard deviation, returns a function equal to the 
    exponent of a normal distribution
    
    Args:
        mean (float): mean (mu) of the normal distribution
        std_dev (float): standard deviation (sigma) of the normal distribution

    Returns: 
        function: a function representing the exponent of a normal with the 
            specified properties
    """
    def normal_exponent(x: float) -> float:
        """takes in a value and returns the exponent value of a normal
        
        Args: 
            x (float): value at which to evaluate

        Returns: 
            float: the exponent evaluated at x
        """
        return (-1/2) * (((x - mean) / std_dev) ** 2)

    return normal_exponent


def generate_joint_pdf(exp: pd.Series, num_obs: int) -> Callable:
    """given the expected distribution and the total number of observations, returns a joint
    pdf for all possible outcomes
    
    Args: 
        exp (pd.Series): the ground truth (expected) distribution
        num_obs (int): the number of observations

    Returns: 
        function: the joint pdf function of the observation distributions given 
            the expected distribution and the total number of observations
    """
    percent_exp = exp / exp.sum()

    exponent_functions = [generate_normal_exponent(mean=(p*num_obs), std_dev=math.sqrt(p*num_obs*(1-p))) for p in percent_exp]
    denominator_expr = [math.sqrt(p*num_obs*(1-p)*2*math.pi) for p in percent_exp]

    def joint_pdf(*point: float) -> float:
        """takes in a point (distribution) and returns the probability of that distribution
        
        Args: 
            point (floats): distribution to evaluate at

        Returns: 
            float: the probability of achieving that distribution 
        """
        if len(point) < len(exp):
            point = list(point) + [(num_obs) - sum(point)]

        paired = zip(exponent_functions, point)
        exponent = sum([f(x) for f, x in paired])

        return math.exp(exponent) / math.prod(denominator_expr)

    return joint_pdf

# -----------------------------------------------------------


# CALCULUS --------------------------------------------------

def hyperplane_integration(f: Callable, hyperplane: list, max_val: float = None, chunk_size: int = "auto", num_samples: int = "auto", random_state: int = 42, pbar: Callable = None) -> float:
    """integrates the pdf over a hyperplane using quasi-Monte Carlo integration
    
    Args:
        pdf (function): the function to integrate
        hyperplane (object): the hyperplane over which to integrate
        max_val (float): the max_val at which to cap integration (defaulted to None) - 
            if specified, integrates without including any portions where 
            f(x) > max_val
        chunk_size (int): the amount of samples to handle at one time (defaulted to auto)
        random_state (int): random state to use to ensure the integration is deterministic

    Returns: 
        float: the result of integration
    """
    integration_dim = (len(hyperplane.normal) - 1)

    if chunk_size == "auto":
        chunk_size = calculate_optimal_chunk(dimension=integration_dim)
    if num_samples == 'auto':
        num_samples = calculate_num_samples(integration_dim=integration_dim, hyperplane=hyperplane)
    
    sobol_engine = qmc.Sobol(d=integration_dim, scramble=True, seed=random_state)

    total_samples = 0
    accumulated_sum = 0.0

    while total_samples < num_samples:

        current_chunk_size = min(chunk_size, num_samples - total_samples)
        samples = sobol_engine.random(n=current_chunk_size)

        hyperplane_points = np.zeros((current_chunk_size, integration_dim + 1))
        
        for i in range(current_chunk_size):
            remaining_sum = hyperplane.coef
            for j in range(integration_dim):

                max_val_for_dim = remaining_sum if j == 0 else remaining_sum - np.sum(hyperplane_points[i, :j])
                samples[i, j] = samples[i, j] * max_val_for_dim 
                hyperplane_points[i, j] = samples[i, j]

            x = hyperplane_points[i, :-1]
            hyperplane_points[i, -1] = (hyperplane.coef - np.dot(hyperplane.normal[:-1], x)) / hyperplane.normal[-1]
        
        f_values = np.apply_along_axis(lambda x: f(*x), 1, hyperplane_points)

        if max_val:
            f_values_threshold = np.where(f_values < max_val, f_values, 0)
        else:
            f_values_threshold = f_values

        accumulated_sum += np.sum(f_values_threshold)
        total_samples += current_chunk_size

        pbar.update(1)

    volume = (hyperplane.coef ** integration_dim) / math.factorial(integration_dim)

    return volume * (accumulated_sum / num_samples)

# -----------------------------------------------------------


# DISTRIBUTION ANALYSIS -------------------------------------

def E(exp: pd.Series, obs: pd.Series, approximate: bool, chunk_size: int = 'auto', num_samples: int = 'auto', random_state: int = None) -> float:
    """performs an E-test on an expected distribution and observed distribution
    
    Args: 
        exp (pd.Series): the expected (ground-truth) distribution
        obs (pd.Series): the observed distribution
        aproximate (pd.Series): if False, the exact discrete probability is calculated, if True, 
            an approximate is calculated based on continous probability
        chunk_size (int): the amount of samples to do simultaneously (defaulted to "auto")
        num_samples (int): the number of samples to calculate in total - lower is faster
            but less precise
        random_state (int): if specified, leads to deterministic results

    Returns: 
        float: the E-value
    """
    if not approximate:

        print(f"Running discrete E-Test...")

        try: 
            dlvns = 0
            threshold = discrete_distribution_prob(exp=exp, obs=obs)

            for combination in generate_combinations(len(obs), obs.sum()):
                prob = discrete_distribution_prob(exp=exp, obs=pd.Series(combination))
                if prob <= threshold:
                    dlvns += prob

        except OverflowError:
            raise OverflowError("Number of observations too large. Please use a continuous approximation")

    else:

        print(f"Running continuous E-Test...")

        obs = scale_binomial(exp=exp, obs=obs)

        joint_pdf = generate_joint_pdf(exp=exp, num_obs=obs.sum())
        threshold = joint_pdf(*obs)

        hyperplane = Hyperplane(normal=np.array([1] * len(exp)), coef=obs.sum())
 
        if chunk_size == "auto":
            chunk_size = calculate_optimal_chunk(dimension=(len(obs) - 1))
        if num_samples == "auto":
            num_samples = calculate_num_samples(integration_dim=(len(obs) - 1), hyperplane=hyperplane)
        print(f"Using {num_samples*2} total samples in size {chunk_size} chunks ({num_samples*2/chunk_size} total chunks)")
        
        if not random_state:
            random_state = random.randint(0, 2*32 - 1)

        pbar = tqdm(total=num_samples*2/chunk_size, desc='Integrating')
        thresheld_space = hyperplane_integration(f=joint_pdf, hyperplane=hyperplane, max_val=threshold, chunk_size=chunk_size, num_samples=num_samples, random_state=random_state, pbar=pbar)
        error_space = hyperplane_integration(f=joint_pdf, hyperplane=hyperplane, chunk_size=chunk_size, num_samples=num_samples, random_state=random_state, pbar=pbar)

        dlvns = thresheld_space / error_space

    return dlvns

# -----------------------------------------------------------