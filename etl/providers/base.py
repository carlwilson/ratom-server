import logging

from libratom.lib.pff import PffArchive

logger = logging.getLogger(__name__)


class ImportProviderError(Exception):
    def __init__(self, message, error):
        super().__init__(message)
        self.error = error


class ImportProvider:
    """Base class that provides an interface to the etl.importer.PstImporter"""

    def __init__(self) -> None:
        self._data = None
        self.pff_archive = None  # type: PffArchive

    def open(self) -> None:
        logger.info(f"Opening archive {self._data} with provider")
        self.pff_archive = PffArchive(self._data)

    @property
    def path(self):
        pass

    @property
    def exists(self):
        pass

    @property
    def file_size(self):
        pass

    @property
    def file_name(self):
        pass