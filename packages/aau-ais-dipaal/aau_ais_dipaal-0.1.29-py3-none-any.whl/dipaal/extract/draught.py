from aau_ais_utilities.connections import PostgreSQLConnection
from dipaal.extract.sql.draught_mmsi import mmsi_draught_avg, mmsi_draught_min, mmsi_draught_max, \
    mmsi_draught_histogram, mmsi_draught_mean
from sqlalchemy import CursorResult, Engine


class DraughtExtractor:

    def __init__(self, engine: Engine):
        """Initialize the CellExtractor.

        The width of the grid is expected to be larger than the height.

        Args:
            engine: The engine to use for the connection.
        """
        self.connection = PostgreSQLConnection(engine)

    def extract_draught_avg(self, mmsi: int):
        """
        Extract the average draught for a given MMSI.

        Args:
            mmsi: The MMSI to extract the average draught for.
        """

        return self._extract_draught(mmsi_draught_avg, mmsi)

    def extract_draught_min(self, mmsi: int):
        """
        Extract the minimum draught for a given MMSI.

        Args:
            mmsi: The MMSI to extract the minimum draught for.
        """

        return self._extract_draught(mmsi_draught_min, mmsi)

    def extract_draught_max(self, mmsi: int):
        """
        Extract the maximum draught for a given MMSI.

        Args:
            mmsi: The MMSI to extract the maximum draught for.
        """

        return self._extract_draught(mmsi_draught_max, mmsi)

    def extract_draught_mean(self, mmsi: int):
        """
        Extract the mean draught for a given MMSI.

        Args:
            mmsi: The MMSI to extract the mean draught for.
        """

        return self._extract_draught(mmsi_draught_mean, mmsi)

    def extract_draught_histogram(self, mmsi: int):
        """
        Extract the draught histogram for a given MMSI.

        Args:
            mmsi: The MMSI to extract the draught histogram for.
        """

        return self._extract_draught(mmsi_draught_histogram, mmsi)

    def _extract_draught(self, query: str, mmsi: int) -> CursorResult:
        """
        Executes a query to extract draught information for a given MMSI.

        Args:
            query: The query to execute.
            mmsi: The MMSI to extract the draught information for.
        """

        params = {
            "mmsi": mmsi
        }

        return self.connection.execute_jinja(sql=query, params=params)
