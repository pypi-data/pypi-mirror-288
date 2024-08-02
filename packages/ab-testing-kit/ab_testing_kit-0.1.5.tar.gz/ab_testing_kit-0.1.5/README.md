# A-B_testing_kit

ab-testing-kit is a Python package designed to facilitate A/B testing for data analysis. It provides utilities to perform statistical tests to compare two groups and determine if there are significant differences between them.

## Features
- Normality Test: Check if the data in both test and control groups follow a normal distribution using the Shapiro-Wilk test.
- Variance Equality Test: Assess if the variances between two groups are equal using Levene’s test.
- A/B Testing: Perform A/B testing using Student’s T-test, Welch’s T-test, or Mann-Whitney U test based on the data characteristics.

## Installation
You can install ab-testing-kit from PyPI using pip:

`pip install ab-testing-kit`

## Usage
Here's a quick guide on how to use ab-testing-kit for performing A/B testing.

### Importing the Package

`from ab_testing_kit import ab_test`


### Sample data
test_group = pd.DataFrame({
    'metric': [2.5, 3.6, 3.8, 2.9, 3.4]
})

control_group = pd.DataFrame({
    'metric': [3.2, 3.3, 2.8, 3.0, 3.1]
})

### Perform A/B testing
`result = ab_test(test_group, control_group, column='metric', alpha=0.05, center='mean')

print("Statistic:", result['statistic'])
print("P-value:", result['pvalue'])`

#### Functions
_normality_test(test, control, column, alpha)
Tests if the data in both test and control groups are normally distributed.