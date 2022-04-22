import yaml


class Config(object):
    def __init__(self, filename):
        with open(filename, "r") as fd:
            config = yaml.load(fd, Loader=yaml.FullLoader)

        self._java = config.get("java")
        self._doc_root = config.get("doc_root")
        self._index_path = config.get("index_path", "docs-index")
        self._listen_port = config.get("listen_port", 8080)
        self._path_token = config.get("path_token", "DEVNET")
        self._workdir = config.get("workdir", ".")

        if not all([self._java, self._doc_root]):
            raise ValueError("ERROR: You must set both java and doc_root in your config file.")

        try:
            self._listen_port = int(self._listen_port)
        except TypeError:
            raise Exception("ERROR: listen_port must be an integer")

    @property
    def java(self) -> str:
        """Path to the Java Runtime Environment command"""
        return self._java

    @property
    def doc_root(self) -> str:
        """URL base where docs can be found.

        The next element in this path MUST be path_token defined below.
        """
        return self._doc_root

    @property
    def index_path(self) -> str:
        """Name of the directory containing the document index.

        This MUST be present in the root directory of this project.
        """
        return self._index_path

    @property
    def listen_port(self) -> int:
        """The TCP port on which the search service listens"""
        return self._listen_port

    @property
    def path_token(self) -> str:
        """
        The name of the directory where both the local documents and
        the remote web-hosted documents live.

        Everything in the directory tree prior to this directory are ignored.
        """
        return self._path_token

    @property
    def workdir(self) -> str:
        """
        The working directory from which the script will be run.
        """
        return self._workdir
