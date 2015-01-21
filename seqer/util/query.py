# Taken from: https://github.com/hansent/kivy/blob/kvquery/kivy/utils.py
from kivy.app import App


def breadth_first(root, children=iter):
    '''walk tree is a generator function for breadth first tree traversal.
    it will traverse the entire decendant tree of a widget/node.

    example:
        #can be used in standard list comnprehension
        specials = [w for w in walk_tree(root) if 'special' in w.cls]

        #but doesnt generate whole list, if used with e.g. next()
        #will only go until 1 item is found
        first = (w for w in walk_tree(root) if 'special in w.cls').next()

        :Parameters:
        `root`: root of teh tree to be walked
            this node be the first node visited.

        `children`: function, default: iter
            function used to get an iterator over the nodes child nodes
    '''
    yield root
    last = root
    for node in breadth_first(root, children):
        for child in children(node):
            yield child
            last = child
        if last == node:
            return


def walk_tree(root):
    '''returns an iterator that walks a tree of objects which have
    a attribute named 'children', which defines the tree structure
    using breadth first search.

    example:
        w = Widget()
        for i in range(10):
            layout = BoxLayout()
            layout.add_widget(Button())
            layout.add_widget(Button())
            w.add_widget(layout)

        tree = walk_tree(w) # this is a generator function
        tree.next() # returns the first Boxlayout
        tree.next() # returns the second Boxlayout (breadth first)
        for w in tree:  #iterate over teh whole collection
            print w

    :Parameters:
    `root`: root of the tree to be walked
        this node be the first node visited.
    '''
    return breadth_first(root, lambda w: w.children)


def filter_tree(root, predicate):
    '''filter a tree based on a predecate.
    the filter_tree function is very simmilar to walk_tree,
    with teh excpetion, that will will skip all those nodes
    for which predicate(node) returns False.

    :Parameters:
    `root`: root of the tree to be walked
        this node be the first node visited.
    '''
    return (c for c in walk_tree(root) if predicate(c))


def kvquery(root, **kwargs):
    '''kvquery provides a convinient way of finding widgets in an
    application that uses the kv style language.

    example:
        lets say you have a .kv file with the following Rule:
        <MovieWidget>:
            BoxLayout:
                Video:
                    kvid: 'video'
                Label:
                    text: root.movie_title
                Label:
                    text: root.movie_description

        in your python code, you may want to get the reference to
        Video widget nested inside the widget you have a handle to.

        # video will be the first node that jas a 'kvid' property == 'video'
        video = kvquery(movie, kvid='video').next()


        #lets get all teh labels in a list
        labels = list(kvquery(movie, __class__=Label))


    :Parameters:
    `root`: root of the tree to queried
        this node and all decendants will be iterated by the
        returned generator.

    `**kwargs`: **kwargs, key/value pairs
        The keys corrosponf to porperty names, and values to the
        property values of the widget nodes being queried.  If a node
        has at least one attr such that (gettattr(node, key) == value)
        is true; it will be included in the iteration.
    '''

    def _query(w):
        '''iternal query function / predicate for tree query
        '''
        for k, v in kwargs.iteritems():
            if (v == getattr(w, k, None)):
                return True
    return filter_tree(root, _query)


def select_by_type(root, object_type):
    return filter_tree(root, lambda c: isinstance(c, object_type))
