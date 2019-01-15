from stocks import *
from exp3_stocks import Exp3_runExperiment
from ucb1_stocks import Ucb1_runExperiment
import matplotlib.pyplot as plt


if __name__ == '__main__':
    table = readInStockTable('A_Stock_Data/A_Stock2.csv')
    Ucb1_Regret, Ucb1_Reward, Ucb1_numRounds = Ucb1_runExperiment(table)

    gamma = .33
    Exp3_Regret, Exp3_Reward, Exp3_numRounds = Exp3_runExperiment(table, gamma)

    fig = plt.figure()
    fig.set_size_inches(20,20)
    ax1 = fig.add_subplot(111)
    # 产生测试数据
    ax1.set_title('Regret For A_stock')  # 设置标题
    plt.xlabel('NumRounds')  # 设置X轴标签
    plt.ylabel('Cumulative_Regret')  # 设置Y轴标签

    ax1.scatter([i for i in range(Exp3_numRounds)], Exp3_Regret, c='r', marker='>', label='Exp3_Regret', edgecolors='none')  # 画散点图
    # plt.legend(['Exp3_Regret'])  # 设置图标
    ax1.scatter([i for i in range(Exp3_numRounds)], Exp3_Reward, c='b', marker='>', label='Exp3_Reward', edgecolors='none')  # 画散点图
    # plt.legend(['Exp3_Reward'])  # 设置图标

    ax1.scatter([i for i in range(Ucb1_numRounds)], Ucb1_Regret, c='g', marker='>', label='Ucb1_Regret', edgecolors='none')  # 画散点图
    # plt.legend(['Ucb1_Regret'])  # 设置图标
    ax1.scatter([i for i in range(Ucb1_numRounds)], Ucb1_Reward, c='y', marker='>', label='Ucb1_Reward', edgecolors='none')  # 画散点图
    # plt.legend(['Ucb1_Reward'])  # 设置图标

    ax1.legend(loc='upper left')
    plt.savefig("RegretAndReward.png")

    plt.show()  # 显示所画的图

    payoffGraph(table, list(sorted(table.keys())), cumulative=True)



# import matplotlib.pyplot as plt
# from numpy.random import rand
#
#
# fig, ax = plt.subplots()
# for color in ['red', 'green', 'blue']:
#     n = 750
#     x, y = rand(2, n)
#     scale = 200.0 * rand(n)
#     ax.scatter(x, y, c=color, s=scale, label=color,
#                alpha=0.3, edgecolors='none')
#
# ax.legend(loc = 'upper left')
# ax.grid(True)