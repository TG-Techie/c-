from cmns_parse import parse

def test():
    with open('./examples/calltest.c-') as file:
        tree = parse(file.read())
        print(tree.pretty())
    return tree

if __name__ == '__main__':
    test()
