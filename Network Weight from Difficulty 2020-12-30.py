version = "2020-12-30"

startingBlock = 679900         
numBlocks = 200

'''
Network Weight from Difficulty.py 

Copyright (c) 2020 Jackson Belove
Beta software, use at your own risk
MIT License, free, open software for the Qtum Community

= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

A program to use qtum.info API calls to determine the Network Weight, which is a 72 period
moving average given by:

each block difficulty * 4294967296
get the 72 block average
divide by 9216 (the average time in seconds for 72 blocks)
multiply and divide by some scaling factors to get Network Weight

qtum.info API reference https://github.com/qtumproject/qtuminfo-api#qtuminfo-api-documentation

The format of the block API request is (mainnet):

https://qtum.info/api/block/nnnnnn 

Revisions

2020-12-28 Repurposed from SuperStakerCheckup

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Program Summary

Loop on block number
    API call to get difficulty for the block
    Calculate the moving average of Network Weight
    Apply scaling multipliers and divisors
    Print the block, difficulty, and Network Weight

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

'''

from timeit import default_timer as timer               # for timer()
import sys                                              # for system exit
import urllib.request                                   # for reading Web sites, Python 3
from urllib.request import Request, urlopen
import urllib.request as urlRequest
from urllib.error import URLError, HTTPError            # for URL errors
from array import *                                     # for arrays

# MAIN PROGRAM = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

def main():

    isMainnet = True                                        # set True for Mainnet, False for Testnet
    APIEndpointTestnet = "https://testnet.qtum.info/api/"   # for testnet
    APIEndpointMainnet = "https://qtum.info/api/"           # for mainnet
    APIEndpointThisChain = ''                               # for the chain we are on

    # for API calls pretend to be a chrome 87 browser on a windows 10 machine
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

    data = ""                                               # data read from API calls
         
    nPoSInterval = 72                                       # moving average period for network weight
    networkWeightList = array('f',(0.0,) * nPoSInterval)    # an array for storing old difficulty values

    networkWeightListIndex = 0                  # the index into the moving average arrays
    STAKE_TIMESTAMP_MASK = 15                   # pos.h line 21: static const uint32_t STAKE_TIMESTAMP_MASK = 15;
    networkWeightListIndex = 0                  # the index into the moving average arrays
    averageNetworkWeight = 0.0                  # used to calculate average new network weight
    COIN = 100000000                            # from amount.h line 14:
                                                # static const CAmount COIN = 100000000;
                          
    print("Network Weight from Difficulty", version, "\n")
    print("block,difficulty,network weight")

    start = timer()

    if isMainnet:
        APIEndpointThisChain = APIEndpointMainnet
    else:
        APIEndpointThisChain = APIEndpointTestnet

    block = startingBlock
    endBlock = startingBlock + numBlocks

    # loop through blocks to get the difficulties and calculate the Network Weight
    # Network Weight is valid after the first 72 blocks

    while block < endBlock:

        url = APIEndpointThisChain + "block/" + str(block)

        # print(url)
           
        try:                
            req = Request(url, headers = headers)
            # open the url
            x = urlRequest.urlopen(req)
            result = x.read()

        except URLError as e:
            print("We failed to reach a server for ", url)
            print("ULR Reason: ", e.reason)
            break

        # print(result)

        data = str(result)

        '''
        <snip>
        "miner":"qZGa1suMNRksgu1geoKMcNUsViHE8nCzXc",
        "difficulty":1332331.8285931018,
        "reward":"400090000",
        "confirmations":247944}
        '''
        
        strDifficulty = ''          # a string      
        lenData = len(data)

        dataIndex = data.find("difficulty", 0, lenData)

        if dataIndex > 0:           # found "difficulty"

            dataIndex += 12         # point at the first digit

            while data[dataIndex] != ',':
                
                strDifficulty += data[dataIndex]
                dataIndex += 1

        dDiff = float(strDifficulty)

        # print("difficulty =", dDiff)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
         
        # calculate the network weight as a moving average of difficulty
        # following GetPoSKernelPS()

        # this overwrites the value 72 blocks ago:
        networkWeightList[networkWeightListIndex] = dDiff * 4294967296  # scaling factor

        sum = 0.0
                                  
        for i in range(72):                 # get the 72 period sum
            sum += networkWeightList[i]

        sum /= 9216                         # divisor for 72 * 128 seconds

        millions = sum / COIN               # convert to millions

        averageNetworkWeight = millions * (STAKE_TIMESTAMP_MASK + 1)  # scaling factor

        networkWeightListIndex += 1
        
        if networkWeightListIndex >= nPoSInterval: # wrap
            networkWeightListIndex = 0

        # print("Index =", networkWeightListIndex)
                 
        formattedDiff = '{0:.3f}'.format(round(dDiff, 3))
        formattedDiffWithComma = formattedDiff + ","

        if block > nPoSInterval + startingBlock - 1:
            temp = str(block) + "," + formattedDiffWithComma + str(round(averageNetworkWeight))
                                           
        else:     # starting up, no good average yet
            temp = str(block) + "," + formattedDiffWithComma + "0"
            
        print(temp)
            
        block += 1

    sys.exit()

if __name__ == '__main__':
    main()
     
    

