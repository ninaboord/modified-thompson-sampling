from scipy import stats
import random
import statistics



def chooseA(prob_A, history):
    if stats.bernoulli.rvs(prob_A) == 1:
        history['A']['s'] += 1
    else:
        history['A']['f'] += 1


def chooseB(prob_B, history):
    if stats.bernoulli.rvs(prob_B) == 1:
        history['B']['s'] += 1
    else:
        history['B']['f'] += 1


def thompson(prob_A, prob_B, trials):
    history = {
        'A': {'s': 1, 'f': 1},
        'B': {'s': 1, 'f': 1}
    }
    for i in range(trials):
        A = stats.beta.rvs(history['A']['s'], history['A']['f'])
        B = stats.beta.rvs(history['B']['s'], history['B']['f'])
        if A > B:
            chooseA(prob_A, history)
        else:
            chooseB(prob_B, history)
    #print(history)
    return history['A']['s'] + history['B']['s']


def mean_beta(prob_A, prob_B, trials):
    history = {
        'A': {'s': 1, 'f': 1},
        'B': {'s': 1, 'f': 1}
    }
    for i in range(trials):
        mean_A = history['A']['s'] / (history['A']['s'] + history['A']['f'])
        mean_B = history['B']['s'] / (history['B']['s'] + history['B']['f'])
        if mean_A > mean_B:  # choose A
            chooseA(prob_A, history)
        else:
            chooseB(prob_B, history)
    #print(history)
    return history['A']['s'] + history['B']['s']


def modified_thompson(prob_A, prob_B, trials, epsilon):
    history = {
        'A': {'s': 1, 'f': 1},
        'B': {'s': 1, 'f': 1}
    }
    for i in range(int(epsilon * trials)):
        A = stats.beta.rvs(history['A']['s'], history['A']['f'])
        B = stats.beta.rvs(history['B']['s'], history['B']['f'])
        if A > B:  # choose A
            chooseA(prob_A, history)
        else:
            chooseB(prob_B, history)
    for i in range(int(trials - epsilon * trials)):
        mean_A = history['A']['s'] / (history['A']['s'] + history['A']['f'])
        mean_B = history['B']['s'] / (history['B']['s'] + history['B']['f'])
        if mean_A > mean_B:
            chooseA(prob_A, history)
        else:
            chooseB(prob_B, history)
    #print(history)
    return history['A']['s'] + history['B']['s']


def pull_random(prob_A, prob_B, history):
    choice = random.randint(0, 1)
    if choice == 0:
        chooseA(prob_A, history)
    else:
        chooseB(prob_B, history)


def epsilon_greedy(prob_A, prob_B, trials, epsilon):
    history = {
        'A': {'s': 1, 'f': 1},
        'B': {'s': 1, 'f': 1}
    }
    for i in range(trials):
        p = random.uniform(0, 1)
        mean_A = history['A']['s'] / (history['A']['s'] + history['A']['f'])
        mean_B = history['B']['s'] / (history['B']['s'] + history['B']['f'])
        if p < epsilon or mean_A == mean_B:
            pull_random(prob_A, prob_B, history)
        else:  # pull best
            if mean_A > mean_B:
                chooseA(prob_A, history)
            else:
                chooseB(prob_B, history)
    #print(history)
    return history['A']['s'] + history['B']['s']


def epsilon_greedy_dec(prob_A, prob_B, trials):
    history = {
        'A': {'s': 1, 'f': 1},
        'B': {'s': 1, 'f': 1}
    }
    for i in range(trials):
        actions = 1
        epsilon = 1/actions
        p = random.uniform(0, 1)
        mean_A = history['A']['s'] / (history['A']['s'] + history['A']['f'])
        mean_B = history['B']['s'] / (history['B']['s'] + history['B']['f'])
        if p < epsilon or mean_A == mean_B:
            pull_random(prob_A, prob_B, history)
        else:  # pull best
            if mean_A > mean_B:
                chooseA(prob_A, history)
            else:
                chooseB(prob_B, history)
        actions += 1
    #print(history)
    return history['A']['s'] + history['B']['s']


def main():
    t = set()
    mb = set()
    mt = set()
    eg = set()
    egd = set()

    for i in range(10000):
        prob_A = random.uniform(0, 1)
        prob_B = random.uniform(0, 1)
        t.add(thompson(prob_A, prob_B, 1000))
        mb.add(mean_beta(prob_A, prob_B, 1000))
        mt.add(modified_thompson(prob_A, prob_B, 1000, 0.1))
        eg.add(epsilon_greedy(prob_A, prob_B, 1000, 0.1))
        egd.add(epsilon_greedy_dec(prob_A, prob_B, 1000))

    print('thompson')
    print(statistics.mean(t))
    print(statistics.stdev(t))
    print('mean beta')
    print(statistics.mean(mb))
    print(statistics.stdev(mb))
    print('mod thompson')
    print(statistics.mean(mt))
    print(statistics.stdev(mt))
    print('eps greedy')
    print(statistics.mean(eg))
    print(statistics.stdev(eg))
    print('eps greedy dec')
    print(statistics.mean(egd))
    print(statistics.stdev(egd))


if __name__ == '__main__':
    main()