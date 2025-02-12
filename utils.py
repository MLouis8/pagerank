def streamf_to_tedges(fpath: str)-> tuple[list[tuple[int, int, int]], int]:
    pass

def patg_to_tedges(fpath: str) -> tuple[list[tuple[int, int, int]], int]:
    with open(fpath, 'r') as patg_file:
        n = int(patg_file.readline(0))
        lines = patg_file[1:].readlines()
    f = lambda l: (int(l[0]), int(l[1]), int(l[2])) 
    tedges = [f(line.split(' ')) for line in lines]
    return n, tedges