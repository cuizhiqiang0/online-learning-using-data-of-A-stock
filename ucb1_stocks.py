from ucb1.ucb1 import ucb1
from stats import stats
from stocks import *
from random import shuffle
import matplotlib.pyplot as plt


def ucb1Stocks(stockTable):
   tickers = list(stockTable.keys())
   shuffle(tickers) # note that this makes the algorithm SO unstable
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

   ucb1Generator = ucb1(numActions, reward)
   for (chosenAction, reward, ucbs) in ucb1Generator:
      cumulativeReward += reward
      Reward_graph.append(cumulativeReward)

      weakRegret = (bestActionCumulativeReward - cumulativeReward)
      Regret_graph.append(weakRegret)

      t += 1
      if t == numRounds:
         break

   return cumulativeReward, bestActionCumulativeReward, ucbs, tickers[bestAction],tickers, Regret_graph,Reward_graph,numRounds


prettyList = lambda L: ', '.join(['%.3f' % x for x in L])
payoffStats = lambda data: stats(ucb1Stocks(data)[0] for _ in range(1000))


def Ucb1_runExperiment(table):
   # print("(Expected payoff, variance) over 1000 trials is %r" % (payoffStats(table),))
   reward, bestActionReward, ucbs, bestStock,tickers,Regret, Reward, numRounds = ucb1Stocks(table)
   print("For a single run: ")
   print("Payoff was %.2f" % reward)
   print("Regret was %.2f" % (bestActionReward - reward))
   print("Best stock was %s at %.2f" % (bestStock, bestActionReward))
   print("ucbs: %r" % prettyList(ucbs))

   return Regret, Reward, numRounds

if __name__ == "__main__":
   table = readInStockTable('A_Stock_Data/A_Stock2.csv')
   Regret, Reward, numRounds = Ucb1_runExperiment(table)
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


   # print()

   # table2 = readInStockTable('stocks/random-stocks.csv')
   # runExperiment(table2)
   # payoffGraph(table2, list(sorted(table2.keys())), cumulative=True)

