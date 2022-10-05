from concurrent.futures.process import _threads_wakeups
import random

class game_state():
    """
    Balls in bins trading game

    With k bins, 
    n_1 + ... + n_k = n balls, 
    can trade ball j -> i 
    if c_i*n_i < c_j*(n_j - 1).
    
    Can we find upper bound on number of trades?    
    """
    def __init__(self, state, trades=0, coeffs=[]):
        self.k = len(state)
        self.n = sum(state)
        self.state = state
        self.trades = trades
        if not coeffs:
            self.coeffs = self.k*[1]
    
    def __repr__(self):
        repr_str = 'Game state with {} balls in {} bins: {}'
        return repr_str.format(self.n, self.k, self.state)

    def trade_possible(self, i, j):
        """
        Returns boolean whether there is legal trade j -> i.
        """
        i -= 1
        j -= 1
        c_i = self.coeffs[i]
        c_j = self.coeffs[j]
        n_i = self.state[i]
        n_j = self.state[j]
        return c_i*n_i < c_j*(n_j - 1)
    
    def any_trades_possible(self, pair=False):
        """
        Returns boolean whether any legal trades j -> 1.
        """
        inds = list(range(self.k))
        for i in inds:
            other_inds = inds
            other_inds.remove(i)
            for j in other_inds:
                if self.trade_possible(i+1, j+1):
                    if pair:
                        return (i, j)
                    else:
                        return True
        return False

    def any_trades(self):
        """
        Returns list of pairs (i, j) of legal trades.
        """
        inds = list(range(self.k))
        trade_pairs = []
        for i in inds:
            other_inds = inds
            other_inds.remove(i)
            for j in other_inds:
                i += 1
                j += 1
                if self.trade_possible(i, j):
                    trade_pairs.append((i, j))
        return trade_pairs

    def make_trade(self, i, j):
        """
        Make trade j -> i if possible, 
        else raise IllegalTradeError.
        """
        if self.trade_possible(i, j):
            i -= 1
            j -= 1
            self.state[i], self.state[j] = self.state[j], self.state[i]
        else:
            print('Illegal trade.')

def randperm(k):
    """
    Return random permutation of [1, ..., k] 
    or list [i_1, ..., i_k].
    """
    if type(k) == int:
        inds = list(range(1, k+1))
    else:
        inds = list(k)
    k = len(inds)
    perm = []
    while inds:
        j = random.randint(1, k)
        i = inds.pop(j-1)
        perm.append(i)
        k -= 1
    return perm[]
