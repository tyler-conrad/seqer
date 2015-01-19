from kivy.metrics import dp


class QueryDict(dict):
    def __getattr__(self, attr):
        try:
            return self.__getitem__(attr)
        except KeyError:
            return super(QueryDict, self).__getitem__(attr)

    def __setattr__(self, attr, value):
        self.__setitem__(attr, value)


def map_dp(iterable):
    return [dp(i) for i in iterable]


def print_pipe(value):
    print value
    return value
