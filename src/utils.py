def streamf_to_tedges(fpath: str)-> tuple[list[tuple[int, int, int]], int]:
    pass

def patg_to_tedges(fpath: str) -> tuple[list[tuple[int, int, int]], int]:
    with open(fpath, 'r') as patg_file:
        n = int(patg_file.readline(1))
        lines = patg_file.readlines()[1:]
    f = lambda l: (int(l[0]), int(l[1]), int(l[2]))
    pre_tedges = [f(line.split(' ')) for line in lines]
    min_node = pre_tedges[0][0]
    for edge in pre_tedges:
        if edge[0] < min_node:
            min_node = edge[0]
        if edge[1] < min_node:
            min_node = edge[1] 
    tedges = [(e[0]-min_node, e[1]-min_node, e[2]) for e in pre_tedges]
    return n, tedges

def pagerank_ranking(r):
    return sorted(range(len(r)), key=lambda k: r[k], reverse=True)