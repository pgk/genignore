from .helpers import print_notice


class SourcesController(object):

    def __init__(self):
        pass

    def list(self, args):
        print_notice("listing")

    def __call__(self, args):
        action = args.sub_action
        if hasattr(self, action):
            return getattr(self, action)(args)
        else:
            raise NotImplementedError()
