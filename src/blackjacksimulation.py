import multiprocessing
import time

from matplotlib import pyplot as plt
from betspread import BetSpread
from blackjack import BlackJackSimulator
from parsestrategy import parse_strategy_table
from defaultstrategy import strategy as strategy_table


def run_sim(runs, bank_values):
    spread = {0:1}
    # spread = BetSpread(spread)
    # spread = {0:0, 1:1, 2:3, 3:5, 4:7, 5:9}
    sim = BlackJackSimulator(8, 0.75, spread, strategy_table, 0)
    for _ in range(runs):
        value = sim.play_hand()
        bank_values.append(value)
    return sim._player_cash, sim._player_spending, bank_values

if __name__ == '__main__':
    start_time = time.time()

    # parse_strategy_table('basicstrategy.csv', strategy_table)

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    num_runs = 1_000_000
    runs = [int(num_runs / num_processes)] * num_processes
    process_args = [(run, []) for run in runs]
    results = pool.starmap(run_sim, process_args)
    # results = [run_sim(num_runs)]


    pool.close()
    pool.join()
    print('Sim completed in %s seconds.' % (time.time() - start_time))

    banks = [result[2] for result in results]
    l=[]
    # for i in range(int(num_runs/8)):
    #     l.append(sum([bank[i] for bank in banks]))

    l = []
    for bank in banks:
        l.extend(bank)
    l.insert(0, 0)
    for i in range(1, len(l)):
        l[i] += l[i-1]

    plt.plot(l, marker='o')
    # plt.plot(banks[1], marker='o')
    # plt.plot(banks[2], marker='o')
    # plt.plot(banks[3], marker='o')
    # plt.plot(banks[4], marker='o')
    # plt.plot(banks[5], marker='o')
    # plt.plot(banks[6], marker='o')
    # plt.plot(banks[7], marker='o')
    plt.xlabel('Number of Hands')
    plt.ylabel('Bank Value')
    plt.show()

    print('Total runs:', sum(runs))
    print('House edge:', (sum([result[0] for result in results])) / sum([result[1] for result in results]))
    print('Process finished in %s seconds.' % (time.time() - start_time))
