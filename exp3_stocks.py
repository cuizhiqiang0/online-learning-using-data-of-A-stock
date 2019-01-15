from exp3.exp3 import exp3, distr
from stats import stats

from stocks import *
from random import shuffle
import matplotlib.pyplot as plt

def exp3Stocks(stockTable, gamma):
   tickers = list(stockTable.keys())
   # print(tickers)
   shuffle(tickers)
   #print(tickers)
   numRounds = len(stockTable[tickers[0]])
   numActions = len(tickers)

   reward = lambda choice, t: payoff(stockTable, t, tickers[choice])
   singleActionReward = lambda j: sum([reward(j,t) for t in range(numRounds)])

   bestAction = max(range(numActions), key=singleActionReward)
   bestActionCumulativeReward = singleActionReward(bestAction)

   cumulativeReward = 0
   t = 0

   weakRegret = 0
   Reward_graph = []
   Regret_graph = []
   expGenerator = exp3(numActions, reward, gamma, rewardMin = -1, rewardMax = 1.0)
   for (choice, reward, estReward, weights) in expGenerator:
      # print(choice)
      cumulativeReward += reward
      Reward_graph.append(cumulativeReward)

      weakRegret = (bestActionCumulativeReward - cumulativeReward)
      Regret_graph.append(weakRegret)

      t += 1
      if t >= numRounds:
         break
   # print(bestAction)
   # print(cumulativeReward, bestActionCumulativeReward, weights, tickers[bestAction], tickers)
   return cumulativeReward, bestActionCumulativeReward, weights, tickers[bestAction], tickers, Regret_graph,Reward_graph, numRounds


prettyList = lambda L: ', '.join(['%.2f' % x for x in L])
payoffStats = lambda data, gamma: stats(exp3Stocks(data, gamma)[0] for _ in range(1000))


def Exp3_runExperiment(table, gamma):
   #均值和方差
   # print("(Expected payoff, variance) over 1000 trials is %r" % (payoffStats(table, gamma),))
   reward, Gmax, weights, bestStock, tickers,Regret, Reward, numRounds = exp3Stocks(table, gamma)
   print("For a single run: ")
   print("Payoff was %.2f" % reward)
   print("Regret was %.2f" % (Gmax - reward))
   print("Best stock was %s at %.2f" % (bestStock, Gmax))
   print("weights: %r" % (prettyList(distr(weights)),))

   return Regret,Reward,numRounds

def weightsStats(table, gamma):
   weightDs = [] # dictionaries of final weights across all rounds

   for i in range(1000):
      reward, Gmax, weights, bestStock, tickers = exp3Stocks(table, gamma)
      weightDs.append(dict(zip(tickers, distr(weights))))

   weightMatrix = []
   for key in tickers:
      print("weight stats for %s: %r" % (key, prettyList(stats(d[key] for d in weightDs))))


def bestGamma(table):
   return max(range(1, 100, 5), key=lambda g: payoffStats(table, g / 100.0)[0]) / 100.0


if __name__ == "__main__":
   # table = readInStockTable('stocks/fortune-500.csv')
   table = readInStockTable('A_Stock_Data/A_Stock2.csv')
   print(table)
   gamma = .33
   # print("Gamma used: %.2f, best gamma is %.2f" % (gamma, bestGamma(table)))
   Regret, Reward, numRounds =Exp3_runExperiment(table, gamma)

   fig = plt.figure()
   ax1 = fig.add_subplot(111)
   # 产生测试数据
   ax1.set_title('Regret of Exp3 For A_stock')  # 设置标题
   plt.xlabel('NumRounds')  # 设置X轴标签
   plt.ylabel('Cumulative_Regret')  # 设置Y轴标签
   ax1.scatter([i for i in range(numRounds)], Regret, c='r', marker='>')  # 画散点图
   plt.legend('Regret')  # 设置图标

   ax1.scatter([i for i in range(numRounds)], Reward, c='b', marker='>')  # 画散点图
   plt.legend('Reward')  # 设置图标
   plt.show()  # 显示所画的图

   payoffGraph(table, list(sorted(table.keys())), cumulative=True)
   #
   # print()

   # table2 = readInStockTable('stocks/random-stocks.csv')
   # gamma = .33
   # print("Gamma used: %.2f, best gamma is %.2f" % (gamma, bestGamma(table2)))
   # runExperiment(table2, gamma)
   # payoffGraph(table2, list(sorted(table2.keys())), cumulative=True)

   #print(weightsStats(table2, 0.33))
