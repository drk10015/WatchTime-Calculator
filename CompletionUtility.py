import readline, glob, os
class Completer:
    def __init__(self, list):
        self.volcab = list

    def complete(self, text, state):
        results = [x for x in self.volcab if x.startswith(text)] + [None]
        return results[state]

    def pathCompleter(text, state):
        """ 
        This is the tab completer for systems paths.
        Only tested on *nix systems
        """
        line = readline.get_line_buffer().split()

        # replace ~ with the user's home dir. See https://docs.python.org/2/library/os.path.html
        if '~' in text:
            text = os.path.expanduser('~')

        # autocomplete directories with having a trailing slash
        if os.path.isdir(text):
            text += '/'

        return [x for x in glob.glob(text + '*')][state]
