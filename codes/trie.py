class Trie:

    root = None

    def __init__(self):
        self.root = None

    def insert(self, word, rank):
        self.root = insert(self.root, word, rank)

    def find(self, word):
        return find(self.root, word)

class Node:

    leftChild = None
    rightChild = None
    centerChild = None
    indicator = False
    character = None
    value = 99999

    def __init__(self, character):
        self.character = character

def insert(node, word, rank):
    if len(word) == 0:
        return node

    if node is None:
        node = Node(word[0])

    #print(word + repr(type(node)))
    if word[0] < node.character:
        node.leftChild = insert(node.leftChild, word, rank)
    elif word[0] > node.character:
        node.rightChild = insert(node.rightChild, word, rank)
    else:
        if len(word[1:]) == 0:
            node.indicator = True
            node.value = int(rank)
        else:
            node.centerChild = insert(node.centerChild, word[1:], rank)

    return node

def find(node, word):
    if node is None or len(word) == 0:
        return (False, 99999)

    #print(word + repr(type(node)))
    if word[0] < node.character:
        return find(node.leftChild, word)
    elif word[0] > node.character:
        return find(node.rightChild, word)
    else:
        if len(word) == 1 and node.indicator == True:
            return (True, node.value)
        return find(node.centerChild, word[1:])

if __name__ == '__main__':
    trie = Trie()
    trie.insert('ternary')
    trie.insert('search')
    trie.insert('tree')
    trie.insert('trie')
    print(trie.find('tree'))
    print(trie.find('trie'))
    print(trie.find('ternary'))
    print(trie.find('search'))
    print(trie.find('tre'))
