import argparse

class connect_act(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            values = 0
        setattr(namespace, self.dest, values)

class delete_act(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            values = 0
        setattr(namespace, self.dest, values)
