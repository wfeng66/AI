import sys
import math as m

class Node:
    def __init__(self, state, level, move=None, nxt=None, pre=None, parent=None):
        self.state = state.replace(',', '')
        self.next = nxt
        self.prev = pre
        self.n = m.sqrt(len(self.state))
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
            root.next = None
            if self.tail is None:
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
            # print(len(self.hs_table[h]))
            for root in self.hs_table[h]:
                if root is not None:
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
            # print(type(node), node.state)
            h = self.hash_func(node.state)
            self.tail = self.tail.prev
            if self.tail is not None:
                self.tail.next = None
            # print('hs_table is: ', type(self.hs_table[h]))
            if self.hs_table[h] is not None:
                for i in range(len(self.hs_table[h])):
                    if self.hs_table[h][i].zstate == node.state:
                        # self.hs_table[h][i] = None
                        del self.hs_table[h][i]
                        if len(self.hs_table[h]) == 0:
                            self.hs_table[h] = None
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

def str_swap(str, pos1, pos2):
    return str[:pos1] + str[pos2] + str[pos1+1:pos2] + str[pos1] + str[pos2+1:]

def find_children(root):
    neighbors = []
    s = root.state
    pos = s.index('0')
    for op in root.av_move:
        if op == 'UP':
            # s[pos - 3], s[pos] = s[pos], s[pos - 3]
            # print(pos, 'U')
            s = str_swap(s, pos-3, pos)
            move = 'U'
        elif op == 'DOWN':
            # s[pos + 3], s[pos] = s[pos], s[pos + 3]
            # print(pos, 'D')
            s = str_swap(s, pos, pos+3)
            move = 'D'
        elif op == 'LEFT':
            # s[pos - 1], s[pos] = s[pos], s[pos - 1]
            # print(pos, 'L')
            s = str_swap(s, pos-1, pos)
            move = 'L'
        elif op == 'RIGHT':
            # s[pos + 1], s[pos] = s[pos], s[pos + 1]
            # print(pos, 'R')
            s = str_swap(s, pos, pos+1)
            move = 'R'
        neighbors.append(Node(s, root.level+1, move, parent=root))
    return neighbors


def BSF(frontier):
    pass





def DFS(init_node, goal_state, capFrontier, capVisited):
    num_visited, max_search_depth = 0, 0
    frontier = Stack(capFrontier)
    visited = Set(capVisited)
    frontier.push(init_node)

    while True:
        if frontier.is_empty():             # No solution
            return None, num_visited, max_search_depth
        node = frontier.pop()
        print(node)
        if node.state == goal_state:
            return node, num_visited, max_search_depth
        if not visited.is_in(node.state):
            visited.push(node)
            num_visited += 1
            print(num_visited)
            if node.level > max_search_depth:
                max_search_depth = node.level
            children = find_children(node)
            for child in children:
                if (not frontier.is_in(child.state)) and (not visited.is_in(child.state)):
                    frontier.push(child)




def main():
    goal_state = '012345678'
    capFrontier = 100
    capVisited = 1000
    args = sys.argv[1:]
    alg, init_state = args[0], args[1]
    init_node = Node(init_state, 0, nxt=None, pre=None, parent=None)
    if alg == 'dfs':
        goal_node, num_visited, max_search_depth = DFS(init_node, goal_state, capFrontier, capVisited)
    # if goal_node is None:
    #     print('No solution!!!', str(num_visited) + ' states were explored.', 'max_search_depth = ' + str(max_search_depth), sep='\n')



if __name__ == '__main__':
    main()
