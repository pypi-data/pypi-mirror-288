"""Statistical tests for ab test"""
import pandas as pd
from scipy import stats

def _normality_test(test:pd.DataFrame, control:pd.DataFrame, column:str, alpha:float):
    
    """Shapiro-Wilk test is a test of normality, it determines whether the given sample comes 
    from the normal distribution or not. Shapiro-Wilk’s test or Shapiro test is a normality test 
    in frequentist statistics. The null hypothesis of Shapiro’s test is that the population is
    distributed normally.
    Parameters:
    - test: pandas dataframe of the test/experimental group
    - control:pandas dataframe of the control group 
    - column: metric to test
    - alpha: significance level
    
    Returns:
    True, if normal, else False
    
    """
    
    test_pval = stats.shapiro(test[column]).pvalue

    control_pval = stats.shapiro(control[column]).pvalue
    

    if test_pval<alpha and control_pval<alpha:

        return False

    return True

def _equal_variance_test(test:pd.DataFrame, control:pd.DataFrame, column:str, alpha:float, center:str):
    """
    Levene’s test is used to assess the equality of variance between two different samples. 
    The null hypothesis for Levene’s test is that the variance among groups is equal.
    The alternative hypothesis is that the variance among different groups is not equal (for at least one pair the variance is not equal to others).
    Parameters:
     - test: pandas dataframe of the test/experimental group
     - control:pandas dataframe of the control group 
     - column: metric to test
     - alpha: significance level
     - center: {'mean', 'median', 'trimmed'}, optional
    Which function of the data to use in the test. 
    
     Returns:
     True, if normal, else False
    """
    pval = stats.levene(test[column], control[column], center=center).pvalue
    
    if pval < alpha:
        
        return False
    
    return True

def ab_test(test:pd.DataFrame, control:pd.DataFrame, column:str, alpha:float, center:str):
    
    """
    A/B test. It compares the means of two groups and checks if there is a difference.
    It uses a Student's T-test if both samples are normal and have equal variance
    It uses a Welch's T-test if both samples are normal and have no equal variance
    It uses a Mann-Whiteny's test if none of the samples are normal
    
    Parameters:
     - test: pandas dataframe of the test/experimental group
     - control:pandas dataframe of the control group 
     - column: metric to test
     - alpha: significance level
     - center: {'mean', 'median', 'trimmed'}, optional
    Which function of the data to use in the test. 
    
    Returns:
    statistic
    pvalue
    """
    
    is_equal_var = _equal_variance_test(test, control, column, alpha, center)
    
    is_normal =  _normality_test(test, control, column, alpha)
    
    test = test[column]
    control = control[column]
    
    print(f"Samples have equal variance: {is_equal_var}\nSamples are normal: {is_normal}")
    
    if is_equal_var and is_normal:
        
        # ttest
        # Ho: no effect or no difference,
        # H1: suggests a specific relationship or effect.
        print("Performing Student T-test...")
        stat, pvalue = stats.ttest_ind(test,control)
        
    elif is_normal and is_equal_var is False:
        
        # welch's test
        print("Performing Welch\'s...")
        stat, pvalue = stats.ttest_ind(test,control, equal_var = False)
       
    else:
        
        # mann-whitney
        print("Performing Mann-whitney test...")
        stat, pvalue = stats.mannwhitneyu(test,control)
        
    if pvalue < alpha:
        
        print('There is a difference between the two groups')
    
    else:
        
        print('There is no difference between the two groups')
        
    return {'statistic':stat,
           'pvalue':pvalue}