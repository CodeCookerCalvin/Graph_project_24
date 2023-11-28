from collections import deque

def inlist(small:list, big:list):
    '''Returns whether a list is inside another list'''

    for x in small:
        if small.count(x) > big.count(x):
            return False
    return True

def bfs(G, s1, s2, r:list, e, n=100):
    '''BFS but stopping only after all of the required integers are used and keeping track of operations'''

    reql = r.copy()
    reql.remove(s1)

    dist = {s1: 0}
    Q = deque([[s1]])

    biglist = []
    c = 0
    stopcounter = 0

    while len(Q) > 0:

        path = Q.popleft()
        node = path[-1]
        adjs = G[node]

        for v in adjs:
            dist[v] = dist[node] + 1
            path2 = path + [v]
            Q.append(path2)

            if stopcounter == 1000000:
                return biglist
            stopcounter += 1

            if v == s2:
                lsmall = [e[str(path2[i-1]) + ',' + str(path2[i])][0] for i in range(1, len(path2))]
                if inlist(reql, lsmall):
                    if c == 0:
                        length = len(path2)
                    if len(path2) == length:
                        lop = [e[str(path2[i-1]) + ',' + str(path2[i])][1] + str(e[str(path2[i-1]) + ',' + str(path2[i])][0]) for i in range(1, len(path2))]
                        if (path2, lop) not in biglist:
                            biglist.append([len(path2), path2, lop])
                    if c == n:
                        return biglist
                    c += 1
                    
    return []

def graph(l:list):
    '''Makes a dictionary graph and a dictionary of edges'''

    g = {i: [] for i in range(-100, 101)}
    e = {}

    for num, adjs in g.items():
        for x in l:

            xsum = num + x
            if xsum >= -100 and xsum <= 100:
                adjs += [xsum]
                key = str(num) + ',' + str(xsum)
                e[key] = [x, '+']

            xprod = num * x
            if xprod >= -100 and xprod <= 100:
                adjs += [xprod]
                key = str(num) + ',' + str(xprod)
                e[key] = [x, '*']
            
            xdif = num - x
            if xdif >= -100 and xdif <= 100:
                adjs += [xdif]
                key = str(num) + ',' + str(xdif)
                e[key] = [x, '-']

            if num/x % 1 == 0:
                xquo = int(num/x)
                if xquo >= -100 and xquo <= 100:
                    adjs += [xquo]
                    key = str(num) + ',' + str(xquo)
                    e[key] = [x, '/']

    return [g, e]

def find_eq(reql:list, solution:int, n=100):
    '''Returns the solutions in the form: [number of solutions, length of solutions, [list of solution nodes, list of operations used in order]]'''

    g = graph(reql)[0]
    e = graph(reql)[1]
    bigbiglist = []

    for i in range(len(reql)):
        bigbiglist += bfs(g, reql[i], solution, reql, e, n)

    if len(bigbiglist) == 0:
        return "Function timed out, too many operations necessary"
    
    lowest = bigbiglist[0][0]
    for i in range(len(bigbiglist)):
        if bigbiglist[i][0] < lowest:
            lowest = bigbiglist[i][0]

    l = []
    for i in range(len(bigbiglist)):
        if bigbiglist[i][0] == lowest and bigbiglist[i] not in l:
            l.append(bigbiglist[i])
    
    length = l[0][0]
    for i in range(len(l)):
        l[i] = l[i][1:]
    
    return [len(l), length, l]

##### python

import numpy as np
import pygame
pygame.font.init()

background_colour = (255, 255, 255)
 
# width, height
screen = pygame.display.set_mode((1000, 800))
 
# caption
pygame.display.set_caption('Graph')
 
screen.fill(background_colour)

running = True

#g = [4, [6, 4, 12, 17], ['-2', '*3', '+5']]
#g = [4, [5, 15, 22, 24], ['*3', '+7', '+2']]
g = [5, [1, 2, 8, 5, 10], ['*2', '*4', '-3', '+5']]

num = 24
num_s = len(g[1])
nodes = [str(i) for i in range(1, 25)]
posgraph = {}

font = pygame.font.SysFont("Verdana", 20)

for i in range(1, num+1):
    sf = 320
    co = (np.cos(np.pi * 2 / num*i) * sf + 500, np.sin(np.pi * 2 / num*i) * sf + 400)
    posgraph[nodes[i-1]] = co
    pygame.draw.circle(screen, (0, 255, 162), co, 34)
    text = font.render(nodes[i-1], True, (0, 0, 0))
    screen.blit(text, co)

#graph = ['6', '4', '12', '17']
graph = [str(x) for x in g[1]]
pygame.draw.circle(screen, (255, 0, 0), posgraph[graph[0]], 12)

for i in range(1, num+1):
    pygame.draw.circle(screen, (0, 0, 0), (np.cos(np.pi * 2 / num*i) * sf + 500, np.sin(np.pi * 2 / num*i) * sf + 400), 8)

for i in range(num_s-1):
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    purple = (128, 0, 128)
    
    if g[2][i][0] == '-':
        color = blue
    elif g[2][i][0] == '*':
        color = purple
    elif g[2][i][0] == '+':
        color = red
    elif g[2][i][0] == '/':
        color = black
    pygame.draw.line(screen, color, posgraph[graph[i]], posgraph[graph[i+1]], 7)

while running:
    pygame.display.update()
