import numpy as np
import pickle
import time


def runTest(density='dense', numShardsRange=list(range(5, 51, 5)),
            numEpochsRange=list(range(100, 1001, 100)),
            redundancy=3, sizeShard=2000, sparsity=0.5,
            initBal=1000, numRuns=500):
    if density == 'dense':
        import mockTiming as mt
    else:
        import mockTimingSparse as mt
    numNodesRange = [k * redundancy for k in numShardsRange]

    schemes = ['full_replication', 'simple_sharding', 'poly_shard']
    metrices = ['tVerMax', 'tVerMedian', 'tVerMean']
    data = {}
    for s in schemes:
        data[s] = {}
        for m in metrices:
            data[s][m] = np.zeros((len(numShardsRange), len(numEpochsRange)))

    for i in range(len(numShardsRange)):
        numShards = numShardsRange[i]
        numNodes = numNodesRange[i]
        for j in range(len(numEpochsRange)):
            numEpochs = numEpochsRange[j]
            print('Now running K=' + str(numShards) + ' Epoch=' +
                  str(numEpochs))
            for n in range(numRuns):
                print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
                tVerMax, tVerMedian, tVerMean = \
                    mt.frEpoch(numShards, numNodes, sizeShard, sparsity,
                               numEpochs, initBal)
                data['full_replication']['tVerMax'][i, j] += tVerMax / numRuns
                data['full_replication']['tVerMedian'][i, j] += \
                    tVerMedian / numRuns
                data['full_replication']['tVerMean'][i, j] += \
                    tVerMean / numRuns

                print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
                tVerMax, tVerMedian, tVerMean =\
                    mt.ssEpoch(numShards, numNodes, sizeShard, sparsity,
                               numEpochs, initBal)
                data['simple_sharding']['tVerMax'][i, j] += tVerMax / numRuns
                data['simple_sharding']['tVerMedian'][i, j] += \
                    tVerMedian / numRuns
                data['simple_sharding']['tVerMean'][i, j] += \
                    tVerMean / numRuns

                print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')
                tVerMax, tVerMedian, tVerMean =\
                    mt.psEpoch(numShards, numNodes, sizeShard, sparsity,
                               numEpochs, initBal)
                data['poly_shard']['tVerMax'][i, j] += tVerMax / numRuns
                data['poly_shard']['tVerMedian'][i, j] += tVerMedian / numRuns
                data['poly_shard']['tVerMean'][i, j] += tVerMean / numRuns

        result = {}
        result['numShardsRange'] = numShardsRange
        result['numNodesRange'] = numNodesRange
        result['numEpochsRange'] = numEpochsRange
        result['data'] = data
        fileName = 'all_schemes_' + density + '_' + \
                   'K=' + str(numShards) + '_' \
                   'M=' + str(sizeShard) + '_' + \
                   'r=' + str(redundancy) + '_' + \
                   'epoch=' + str(numEpochsRange[0]) + ',' + \
                   str(numEpochsRange[-1]) + ']_' + \
                   's=' + str(sparsity) + '_' + \
                   str(int(time.time() / 1000)) + '.pickle'
        with open(fileName, 'wb') as handle:
            pickle.dump(result, handle)
    result = {}
    result['numShardsRange'] = numShardsRange
    result['numNodesRange'] = numNodesRange
    result['numEpochsRange'] = numEpochsRange
    result['data'] = data
    fileName = 'all_schemes_' + density + '_' + \
               'K=[' + str(numShardsRange[0]) + ',' + \
               str(numShardsRange[-1]) + ']_' + \
               'M=' + str(sizeShard) + '_' + \
               'r=' + str(redundancy) + '_' + \
               'epoch=' + str(numEpochsRange[0]) + ',' + \
               str(numEpochsRange[-1]) + ']_' + \
               's=' + str(sparsity) + '_' + \
               str(int(time.time() / 1000)) + '.pickle'
    with open(fileName, 'wb') as handle:
        pickle.dump(result, handle)
    print('Completed. Data saved at: ', fileName)
    return fileName


density = 'dense'
sparsity = 0.5
# numShardsRange = list(range(5, 51, 5))
numShardsRange = [5, 50]
# numEpochsRange = list(range(100, 501, 200))
numEpochsRange = [1000]
sizeShard = 2000
numRuns = 5
redundancy = 3
fileName = runTest(density=density, numShardsRange=numShardsRange,
                   numEpochsRange=numEpochsRange, sizeShard=sizeShard,
                   redundancy=redundancy,
                   sparsity=sparsity, numRuns=numRuns)
