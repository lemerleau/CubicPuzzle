import numpy as np


class BTree(object):
    """docstring for BTree."""

    def __init__(self, label):
        super(BTree, self).__init__()
        self.label = label
        self.left = None
        self.right = None
    def __str__(self) :
        return "(left= "+self.left.label+", right= "+self.right.label+")"

def main():
    root = BTree('R')
    child1 = BTree('C1')
    child2 = BTree('C2')
    root.left = child1
    root.right = child2

    print(root)

if __name__ == '__main__':
    main()
