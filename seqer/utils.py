from kivy.utils import QueryDict as KivyQueryDict


class QueryDict(KivyQueryDict):
    '''QueryDict is a dict() that can be queried with dot.

    .. versionadded:: 1.0.4

  ::

        d = QueryDict()
        # create a key named toto, with the value 1
        d.toto = 1
        # it's the same as
        d['toto'] = 1
    '''

    def __getattr__(self, attr):
        try:
            return self.__getitem__(attr)
        except KeyError:
            return super(QueryDict, self).__getattr__(attr)
