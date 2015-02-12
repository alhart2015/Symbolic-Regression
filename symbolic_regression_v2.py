'''
Client code for symbol tree revamp
'''

from symbol_tree_v2 import SymbolTree
from op_node_v2 import OpNode

def main():
    n = OpNode("^", 0)
    t = SymbolTree(n)
    t.root.left = OpNode("", -2)
    t.root.left.depth = 2
    t.root.right = OpNode("*", 0)
    t.root.right.depth = 2
    t.root.right.left = OpNode("*", 0)
    t.root.right.left.depth = 3
    t.root.right.right = OpNode("", -3)
    t.root.right.right.depth = 3
    t.root.right.left.left = OpNode("", -1)
    t.root.right.left.left.depth = 4
    t.root.right.left.right = OpNode("", -3)
    t.root.right.left.right.depth = 4
    print t
    print t.eval(2)

if __name__ == '__main__':
    main()