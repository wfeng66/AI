import sys
import math as m

class Node:
    def __init__(self, state, level, move, nxt=None, pre=None, parent=None):
        self.state = state
        self.next = nxt
        self.prev = pre
        self.n = m.sqrt(len(self.state)+1)
        self.av_move = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.parent = parent
        self.level = level
        self.move = move
        self.av_move_update()
    def av_move_update(self):
        pos = self.state.index('0')
        if pos//self.n == 1:
            self.av_move.remove('UP')
        if pos//self.n == (self.n-1):
            self.av_move.remove('DOWN')
        if pos % self.n == 0:
            self.av_move.remove('LEFT')
        if (pos + 1) % self.n == 0:
            self.av_move.remove('RIGHT')


class Set:
    def __init__(self, cap):                 # cap refer to the capacity of the hash table
        self.hs_table = [None] * cap
        self.capacity = cap
        self.level = 0
        self.head = None
        self.tail = None
    def hash_func(self, key):
        return int(key) % self.capacity
    def push(self, root):
        h = self.hash_func(root.state)
        if self.hs_table[h] is None:        # the spot is empty
            self.hs_table[h] = [root]
        else:
            if self.is_in(root.state):      # the state exist
                return False
            else:                           # the state doesn't exist
                self.hs_table[h].append(root)
        if self.is_empty():                 # creat link list
            self.head = root
            self.tail = root
        else:
            root.prev = self.tail
            self.tail.next = root
            self.tail = root
    def is_empty(self):
        if self.head is None and self.tail is None:
            return True
        else: return False
    def is_in(self, state):
        h = self.hash_func(state)
        if self.hs_table[h] is not None:
            for root in self.hs_table[h]:
                if root.state == state:
                    return True
        return False
"""
    def pop(self, state):
        h = self.hash_func(state)
        if self.hs_table[h] is not None:
            for i in range(len(self.hs_table[h])):
                if self.hs_table[h][i].state == state:
                    del self.hs_table[h][i]
                    return state
        return None
"""


class Stack(Set):
    def __init__(self, cap):
        super().__init__(cap)

    def pop(self):
        if not self.is_empty():
            node = self.tail
            h = self.hash_func(node.state)
            self.tail = self.tail.prev
            if self.hs_table[h] is not None:
                for i in range(len(self.hs_table[h])):
                    if self.hs_table[h][i].state == node.state:
                        del self.hs_table[h][i]
        return node


class Queue(Set):
    def __init__(self, cap):
        super().__init__(cap)

    def pop(self):
        if not self.is_empty():
            node = self.head
            h = self.hash_func(node.state)
            self.head = self.head.next
            if self.hs_table[h] is not None:
                for i in range(len(self.hs_table[h])):
                    if self.hs_table[h][i].state == node.state:
                        del self.hs_table[h][i]
        return node



def find_children(root):
    neighbors = []
    s = root.state
    pos = root.index(0)
    for op in root.av_move:
        if op == 'UP':
            s[pos - 3], s[pos] = s[pos], s[pos - 3]
            move = 'U'
        elif op == 'DOWN':
            s[pos + 3], s[pos] = s[pos], s[pos + 3]
            move = 'D'
        elif op == 'LEFT':
            s[pos - 1], s[pos] = s[pos], s[pos - 1]
            move = 'L'
        elif op == 'RIGHT':
            s[pos + 1], s[pos] = s[pos], s[pos + 1]
            move = 'R'
        neighbors.append(Node(s, root.level+1, move, parent=root))
    return neighbors


def BSF(frontier):
    pass



def DFS(frontier, explored, goal_state):
    node = frontier.pop()
    explored.push(node)
    if node.state == goal_state:
        return node
    children = find_children(node)
    for child in children:
        if frontier.is_in(child.state) or explored.is_in(child.state):
            continue
        else:
            frontier.push(child)
    DFS(frontier, explored, goal_state)


def DFS(init_node, goal_state, capFrontier, capVisited):
    num_visited, max_search_depth = 0, 0
    frontier = Stack(capFrontier)
    visited = Set(capVisited)
    frontier.push(init_node)
    while True:
        if frontier.is_empty():             # No solution
            return None, num_visited, max_search_depth
        node = frontier.pop()
        if node.state == goal_state:
            return node, num_visited, max_search_depth
        if visited.is_in(node.state):
            visited.push(node)
            num_visited += 1
            if node.level > max_search_depth:
                max_search_depth = node.level
            children = find_children(node)
            for child in children:
                if (not frontier.is_in(child.state)) and (not visited.is_in(child.state)):
                    frontier.push(child)




def main():
    goal_state = '0,1,2,3,4,5,6,7,8'
    capFrontier = 100
    capVisited = 1000
    args = sys.argv[1:]
    alg, init_state = args[0], args[1]
    init_node = Node(init_state, 0, nxt=None, pre=None, parent=None)
    if alg == 'dfs':
        DFS(init_node, goal_state, capFrontier, capVisited)
    sFrontier, qFrontier = Stack(capFrontier), Queue(capFrontier)
    explored = Set(capExplored)
    sFrontier.push(node)
    qFrontier.push(node)

    dfs_goal_node = DFS(sFrontier, explored, goal_state)


if __name__ == '__main__':
    main()
