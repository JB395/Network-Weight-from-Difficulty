# Network-Weight-from-Difficulty
Calculate the Network Weight from Difficulty

A program to use qtum.info API calls to determine the Network Weight, which is a 72 period
moving average given by:

* each block difficulty * 4294967296
* get the 72 block average
* divide by 9216 (the average time in seconds for 72 blocks)
* multiply and divide by some scaling factors to get Network Weight

qtum.info API reference https://github.com/qtumproject/qtuminfo-api#qtuminfo-api-documentation

The format of the block API request is (mainnet):
https://qtum.info/api/block/nnnnnn 

## Program Summary

``` 
Loop on block number
    API call to get difficulty for the block
    Calculate the moving average of Network Weight
    Apply scaling multipliers and divisors
    Print the block, difficulty, and Network Weight
``` 

## Typical output

``` 
Network Weight from Difficulty 2020-12-30 

block,difficulty,network weight
679900,2481604.780,0
679901,2600704.998,0
<snip, first 72 blocks have Network Weight zeroed out until the moving average is valid>
679970,3445666.183,0
679971,3112908.511,0
679972,3186729.147,17297494
679973,2947249.089,17323334
679974,2947249.089,17338273
679975,3040806.600,17348675
679976,3088694.260,17366002
679977,3040815.010,17378088
``` 
