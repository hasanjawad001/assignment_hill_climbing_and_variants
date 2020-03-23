"""
    Implementation of hill climbing search and its variants.
    author: Jawad Chowdhury.
"""
import random, copy

class Board:
    """
    This class maintains properties related to the different state of the N-Queen Problem.
    """
    def __init__(self, n, state=None):
        self.n = n
        if state==None:
            self.state = [['_' for c in range(n)] for r in range(n)]
            for q in range(n):
                r, c = random.randint(0,n-1), random.randint(0,n-1)
                while self.state[r][c] != '_':
                    r, c = random.randint(0, n - 1), random.randint(0, n - 1)
                self.state[r][c] = 'Q'
        else:
            self.state=state
        self.hcost = self.get_hcost()
    def get_hvcost(self):
        hvcost = 0
        for r in range(self.n):
            for c in range(self.n):
                if self.state[r][c] == 'Q':
                    for t in range(self.n):
                        if self.state[r][t] == "Q":
                            hvcost += 1
                        if self.state[t][c] == "Q":
                            hvcost += 1
                    hvcost = hvcost -2
        hvcost = hvcost/2
        return hvcost
    def get_dcost(self):
        dcost = 0
        for r in range(self.n):
            for c in range(self.n):
                if self.state[r][c] == 'Q':
                    tr, tc = r - 1, c - 1
                    while tr >= 0 and tc >= 0:
                        if self.state[tr][tc] == "Q":
                            dcost += 1
                        tr -= 1
                        tc -= 1
                    tr, tc = r + 1, c - 1
                    while tr < self.n and tc >= 0:
                        if self.state[tr][tc] == "Q":
                            dcost += 1
                        tr += 1
                        tc -= 1
                    tr, tc = r + 1, c + 1
                    while tr < self.n and tc < self.n:
                        if self.state[tr][tc] == "Q":
                            dcost += 1
                        tr += 1
                        tc += 1
                    tr, tc = r - 1, c + 1
                    while tr >= 0 and tc < self.n:
                        if self.state[tr][tc] == "Q":
                            dcost += 1
                        tr -= 1
                        tc += 1
        dcost = dcost/2
        return dcost
    def get_hcost(self):
        """
        This method is being used to calculate the heuristic cost of the current board.
        :return:
        """
        hvcost = self.get_hvcost()
        dcost = self.get_dcost()
        hcost = hvcost + dcost
        return hcost
    def __str__(self):
        """
        String representation of the state.
        :return:
        """
        s=''
        for r in range(self.n):
            for c in range(self.n):
                s += str(self.state[r][c]) + ' '
            s += '\n'
        s += str('hcost') + ' : ' + str(self.hcost)
        s += '\n'
        return s

class NQueen:
    """
    This class is being used to maintain the overall flow of the N-Queen problem.
    """
    def __init__(self, no_runs, n, variant='random_restart_sideway'):
        self.no_runs = no_runs
        self.n = n
        self.variant = variant
        self.no_success = 0
        self.no_total_steps = 0
        self.no_random_restart = 0
        self.no_success_steps = 0
    def run(self, limit_random_restart_sideway=100):
        for i in range(0, self.no_runs):
            self.no_random_restart +=1
            print()
            print('==========     BOARD :%s    =========='%(i,) )
            b = Board(n=n)
            self.hill_climbing(variant=self.variant, board=b, limit_random_restart_sideway=limit_random_restart_sideway)
    def get_best_neighbor(self, board, allow_random_restart_sideway=False):
        """
        This method gives the best successor based on the strategy.
        :param board:
        :return:
        """
        u=False
        best_board = board
        best_cost = board.hcost
        if allow_random_restart_sideway:
            list_indexQ = []
            list_indexBlank = []
            for r in range(0,self.n):
                for c in range(0,self.n):
                    index = (r, c)
                    if board.state[r][c] == 'Q':
                        list_indexQ.append(index)
                    else:
                        list_indexBlank.append(index)
            random.shuffle(list_indexQ)
            random.shuffle(list_indexBlank)
            for (r,c) in list_indexQ:
                if board.state[r][c] == 'Q':
                    for (nr,nc) in list_indexBlank:
                        if board.state[nr][nc] == '_':
                            neighbor_state = copy.deepcopy(board.state)
                            neighbor_state[r][c] = '_'
                            neighbor_state[nr][nc] = 'Q'
                            neighbor = Board(n=self.n, state=neighbor_state)
                            if neighbor.hcost <= best_cost:
                                u=True
                                best_cost = neighbor.hcost
                                best_board = neighbor
        else:
            for r in range(0,self.n):
                for c in range(0,self.n):
                    if board.state[r][c] == 'Q':
                        for nr in range(0,self.n):
                            for nc in range(0,self.n):
                                if board.state[nr][nc] == '_':
                                    neighbor_state = copy.deepcopy(board.state)
                                    neighbor_state[r][c] = '_'
                                    neighbor_state[nr][nc] = 'Q'
                                    neighbor = Board(n=self.n, state=neighbor_state)
                                    if neighbor.hcost < best_cost:
                                        u=True
                                        best_cost = neighbor.hcost
                                        best_board = neighbor
        return best_board, u
    def hill_climbing(self, variant='random_restart_sideway', board=None, limit_random_restart_sideway=100):
        """
        This method runs the hill climbing algorithm based on the variant.
        :param variant:
        :param board:
        :return:
        """
        if board and variant == 'random_restart_sideway':
            current_board = board
            no_local_restart = 0
            no_local_steps = 0
            success = False
            while not success:
                while current_board.hcost != 0:
                    print(current_board)
                    best_neighbor, _ = self.get_best_neighbor(current_board, allow_random_restart_sideway=False)
                    if best_neighbor.hcost < current_board.hcost:
                        current_board = best_neighbor
                        no_local_steps += 1
                    else:
                        counter_random_restart_sideway = 0
                        updated = True
                        while (best_neighbor.hcost == current_board.hcost) and counter_random_restart_sideway <=limit_random_restart_sideway:
                            print(current_board)
                            current_board = best_neighbor
                            no_local_steps += 1
                            counter_random_restart_sideway +=1
                            best_neighbor, updated = self.get_best_neighbor(current_board, allow_random_restart_sideway=True)
                            if not updated:
                                break
                        if counter_random_restart_sideway > limit_random_restart_sideway or not updated:
                            break
                        current_board = best_neighbor
                if current_board.hcost == 0 :
                    success = True
                    print(current_board)
                    print ('SOLUTION FOUND!!!')
                else:
                    print ('RESTARTING!!!')
                    no_local_restart+=1
                    current_board = Board(n=self.n)
            self.no_success += 1
            self.no_total_steps += no_local_steps
            self.no_success_steps += no_local_steps
            self.no_random_restart += no_local_restart

if __name__ == "__main__":
    print('Hill Climbing Search (random_restart_sideway)!!!')
    input_file_name = 'input.txt'
    with open(input_file_name) as f:
        lines = f.readlines()
        values = [line.replace('\n', '').replace(' ', '') for line in lines]
        values = [int(v) for v in values]
    n = values[0] # value of n
    no_run = values[1] # value of number of runs.
    nq_random_restart_sideway = NQueen(no_runs=no_run, n=n, variant='random_restart_sideway')
    nq_random_restart_sideway.run(limit_random_restart_sideway=100)
    print()
    nr = nq_random_restart_sideway.no_runs
    ns = nq_random_restart_sideway.no_success
    rs = (ns/nr)*100
    nf = nr-ns
    rf = (nf/nr)*100
    n_total_steps = nq_random_restart_sideway.no_total_steps
    n_success_steps = nq_random_restart_sideway.no_success_steps
    n_failure_steps = n_total_steps - n_success_steps
    avg_steps_success = n_success_steps/ns if ns != 0 else 0
    avg_steps_failure = n_failure_steps/nf if nf != 0 else 0
    # print('No of Total Runs: {:.2f}'.format(nr) )
    # print('Success Rate: {:.2f} %'.format(rs) )
    # print('Failure Rate: {:.2f} %'.format(rf) )
    # print('Avg steps at Success: {:.2f} '.format(avg_steps_success) )
    # print('Avg steps at Failure: {:.2f} '.format(avg_steps_failure) )
    n_random_restart = nq_random_restart_sideway.no_random_restart
    avg_random_restart = n_random_restart/nr if nr != 0 else 0
    avg_steps = n_total_steps/nr if nr != 0 else 0
    print('Avg random restart: {:.2f} '.format(avg_random_restart) )
    print('Avg steps: {:.2f} '.format(avg_steps) )

