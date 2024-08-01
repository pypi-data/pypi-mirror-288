"""To calculate sample size for binomial and continuous metrics"""
import pandas as pd
from scipy import stats
from typing import List

def _binomial_sample_size_calc(metric_mean:float, mde:float, 
                               alpha:float, beta:float, tail_type:int):
    """To calculate the sample size for the binomial metric
    Parameters: 
    metric_mean:mean of the metric,
    mde:minium detectable effect, 
    alpha,
    beta,
    tail_type: One tailed or Two Tailed, possible values are [1,2]
    
    Returns:
    sample_size, z_beta, z_alpha, pooled_proportions
    """
    
    # standard normal distribution to determine z values
    snd = stats.norm(0, 1)
    
    # beta
    z_beta = snd.ppf(1-beta)
    
    if tail_type == 1:
    
        # alpha
        z_alpha = snd.ppf(1 - alpha)
        
    elif tail_type == 2:
        
        # alpha
        z_alpha = snd.ppf(1 - (alpha/2) )
    
        
    else:
        raise TypeError('Unknown tail type')
             
    
    # pooled proportion
    p = (metric_mean + metric_mean + mde) / 2
    
    sample_size = (
                    2*p*
                   (1-p) *
                   (z_beta + z_alpha)**2 / mde**2
                              
                  )
    
    result = {'sample_size':round(sample_size, 0), 
             'z_beta':z_beta,
              'z_alpha':z_alpha,
              'pooled_proportions':p
             }
    
    return result

def _continuous_sample_size_calc(metric_mean, mde, alpha, beta, std_metric, tail_type):
    """To calculate the sample size for the continuous metric
    Parameters: 
    metric_mean:mean of the metric,
    std_metric: standard deviation of metric,
    mde:minium detectable effect, 
    alpha,
    beta,
    tail_type: One tailed or Two Tailed, possible values are [1,2]
    
    Returns:
    sample_size, z_beta, z_alpha
    """
    
    snd = stats.norm(0,1)
    
    # critical value for beta
    z_beta = snd.ppf(1-beta)
    
    # critical value for alpha
    if tail_type == 1:
        z_alpha = snd.ppf(1 - alpha)
        
    elif tail_type == 2:
        z_alpha = snd.ppf(1 - (alpha/2))
        
    else:
        raise TypeError('Unknown tail type')
        
    u1 = metric_mean
    u2 = round((metric_mean * (mde/100)) + metric_mean, 1)
    
    sample_size = (
                    2*(std_metric**2)*
                   (z_beta + z_alpha)**2 / (u1-u2)**2
                              
                  )
    
    result = {'sample_size':round(sample_size, 0),
             'z_beta':z_beta,
              'z_alpha':z_alpha,
             }
    
    return result

def sample_size_calc(metric_mean, mde, alpha, beta, tail_type = 1,
                     std_metric=None, metric_type = 'binomial'):
    
    if metric_type.lower().strip() == 'binomial':
        
        return _binomial_sample_size_calc(metric_mean, mde, alpha, beta,tail_type)
        
    if metric_type.lower().strip() == 'continuous':
        
        return _continuous_sample_size_calc(metric_mean, mde, alpha, beta, std_metric,tail_type)
    
    else:
        
        return "Unknown metric type" 
    
def pretest_bias(test_before:pd.DataFrame, control_before:pd.DataFrame, metrics:List):
    """
    Welch's T-Test: Used equal_var=False in ttest_ind to perform Welch's t-test, 
    which does not assume equal variances. This is more robust in cases where the 
    two samples might have different variances.
    Parameters:
    - test_before: a pandas dataframe of the test group
    - control_before: a pandas dataframe of the control group
    - metrics: a list of the metrics you want to test
    """
    
    for metric in metrics:

        # Perform t-test
        _, p_value = stats.ttest_ind(test_before[metric], control_before[metric], equal_var=False)  # Welch's t-test

        # Interpret results
        if p_value < 0.05:
            print(f'We reject the null hypothesis (H0). There is a significant difference in average {metric} between the test and control groups.')

        else:
            print(f'We fail to reject the null hypothesis (H0). There is no significant difference in average {metric} between the test and control groups.')
