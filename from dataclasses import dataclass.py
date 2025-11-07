from dataclasses import dataclass
import math, random, time

@dataclass
class Client:
    idx: int; demand: int; a: float; b: float; service: float; x: float; y: float

@dataclass
class Data:
    clients: list  # [0] = depot
    Q: int
    dist: list     # dist[i][j]
    time_mat: list # if same as dist, reuse
    n: int

def feasible_insert(route, pos, client, data, load_prefix, time_prefix):
    # recalcul local autour de pos: renvoie (delta_cost, feasible)
    return delta, feasible

def construct_initial(data):
    # Solomon-like greedy insertion with TW checks (placeholder)
    solution = [[0, 0]]  # one empty route
    unrouted = set(range(1, data.n+1))
    # ... remplir avec best/regret insertion
    return solution

def neighbors_moves(solution, data):
    # yield (move, delta_cost, check_fun)
    yield from ()

def tabu_local(solution, data, it_max=200, tenure=15):
    tabu = {}
    best = solution
    cur = solution
    for it in range(it_max):
        best_move, best_delta = None, float('inf')
        for move, delta, admissible in neighbors_moves(cur, data):
            key = move.attribute_key()
            if key in tabu and not move.aspiration(best):
                continue
            if delta < best_delta:
                best_move, best_delta = move, delta
        if best_move is None:
            break
        cur = best_move.apply(cur)
        tabu[best_move.attribute_key()] = it + tenure
        # purge tabu
        for k, exp in list(tabu.items()):
            if exp <= it: del tabu[k]
        if cost(cur, data) < cost(best, data):
            best = cur
    return best

def alns(data, time_limit=60.0):
    start = time.time()
    x = construct_initial(data)
    x = tabu_local(x, data, it_max=150)
    best = x
    # init operators, weights, temperature
    while time.time() - start < time_limit:
        D = select_destroy()
        R = select_repair()
        x2 = R.insert(D.remove(best))
        if accept(cost(x2,data) - cost(best,data)):
            x = x2
            if cost(x,data) < cost(best,data):
                best = tabu_local(x, data, it_max=80)  # polish court
        update_adaptation()
    return best