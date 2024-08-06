import fire

from .cdn import CdnCmd

class Cmd:
    """
    A command line tool for hotfixing streamlit and streamlit compoents.
    """

    @property
    def cdn(self):
        return CdnCmd()


def main():
    fire.Fire(Cmd)


if __name__ == '__main__':
    main()
