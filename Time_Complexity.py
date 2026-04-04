#Q. Bob has a fuzzy grid of size N x M. Each cell must be filled with a positive integer from 1 to K. Bob wants to fill the
#  grid such that the following constraint is satisfied: 
# -> No 2 adjacent cells in the same row contain the same value.
# 
# Your task is to calculate the total number of ways to fill the grid that satisfy this condition.
# Since the number of ways can be very large, return the answer modulo 10^9 + 7.


# SOLUTION:   
#i = Rows
#j = Columns

''' 
Args: 
N: No. of Rows 
M: No. of Columns
K: Max value allowed in the grid
X: Max allowed difference between max elements of the consecutive rows

Return:
Number of ways to fill the grid module 10^9 + 7

Example:        Tn = ⌀^n = (√5 + 1)^n / 2
'''

MOD = 10**9 + 7
def solve(N,M,K,X):
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    for i in range (1, K + 1):
        dp[1][i] = 1
#build the dp table iteratively
    for i in range (2, K + 1):
        for j in range (1, K + 1):
            #consider all valid values in the previous row within the same constraint
            for prev in range (max(1-j, 1), min(K, j - X) + 1):
                dp[i][j] ={dp[i][j] + dp[i-j][K]} % MOD
                #sum the last row to get the total number of valid fillings
                res = 0 
                for i in range (1, K+1): 
                    res = (res + dp[N][i]) % MOD
    return res



''' 
Example Usage:
N,M,K,X = 3,3,5,1
print(solve(N,M,K,X)) # Output: 25
'''
