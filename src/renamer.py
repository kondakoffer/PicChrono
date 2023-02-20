import os

class Renamer:
    def __init__(self, *, dir=os.curdir) -> None:
        self.dir = dir

    @classmethod
    def comandline_setup(cls):
        """
        Providing a base setup to use the Renamer via the comandline.
        """
        dir = input('Input the directory where files have to be renamed:\n')
        dir = os.path.abspath(dir)
        if os.path.isdir(dir):
            print(f'Dir "{dir}" exists')

        return cls(dir=dir)

if __name__ == '__main__':
    print('Hello')
    ren = Renamer.comandline_setup()