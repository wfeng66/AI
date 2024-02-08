import sys
import math as m

class Node:
    def __init__(self, state, level, nxt=None, pre=None, parent=None):
        self.state = state
        self.next = nxt
        self.prev = pre
        self.n = m.sqrt(len(self.state)+1)
        self.av_move = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.parent = parent
        self.level = level
        self.move
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
        elif op == 'DOWN':
            s[pos + 3], s[pos] = s[pos], s[pos + 3]
        elif op == 'LEFT':
            s[pos - 1], s[pos] = s[pos], s[pos - 1]
        elif op == 'RIGHT':
            s[pos + 1], s[pos] = s[pos], s[pos + 1]
        neighbors.append(Node(s))
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



def main():
    goal_state = '0,1,2,3,4,5,6,7,8'
    capFrontier = 100
    capExplored = 1000
    args = sys.argv[1:]
    alg, init_state = args[0], args[1]
    node = Node(init_state, 0, nxt=None, pre=None, parent=None)
    sFrontier, qFrontier = Stack(capFrontier), Queue(capFrontier)
    explored = Set(capExplored)
    sFrontier.push(node)
    qFrontier.push(node)

    dfs_goal_node = DFS(sFrontier, explored, goal_state)


if __name__ == '__main__':
    main()
