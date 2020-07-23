"""
engine:core
"""

from typing import Dict
from typing import Any
import asyncio

import ogr2pbf

import eventer
import effectors


class Engine(eventer.Engine,
             effectors.Gate,
             effectors.CityOsmId,
             effectors.OsmGraph,
             effectors.CityArea):
    """
    The Engine
    """
    
    _jobs: asyncio.Queue
    _results: asyncio.Queue
    _task: asyncio.Task

    def arise(self) -> None:
        """
        TODO: Add docstring
        """
        loop = asyncio.get_event_loop()

        try:
            self._intro()

            self._jobs = asyncio.Queue()
            self._results = asyncio.Queue()
            self._task = asyncio.ensure_future(self._consume())

            loop.run_until_complete(self._task)
        except KeyboardInterrupt:
            pass
        finally:
            self._outro()
            # Exit
            loop.close()

    def _intro(self) -> None:
        """
        TODO: Add docstring
        """
        core_id = self.__class__.__name__
        print(f'(i) The {core_id} core running...')

    def _outro(self) -> None:
        """
        TODO: Add docstring
        """
        core_id = self.__class__.__name__
        print(f'\n(i) The {core_id} core is stopped')

    async def _add_job(self, data: Dict[str, Any]) -> None:
        """
        TODO: Add docstring
        """
        await self._jobs.put(data)

    async def _add_result(self, is_isochrones_saved: bool) -> None:
        """
        TODO: Add docstring
        """
        await self._results.put(is_isochrones_saved)

    async def _consume(self) -> None:
        """
        TODO: Add docstring
        """
        while True:
            data = await self._jobs.get()
            if data is None:  # => producing is completed
                break
            # Causes the `started` event
            await self.started()
            # Waits result
            await self._wait_for_result()
            # Notifies the queue that data has been processed
            self._jobs.task_done()

    async def _wait_for_result(self) -> None:
        """
        TODO: Add docstring
        """
        is_isochrones_saved = await self._results.get()
        if is_isochrones_saved:
            # Saves the result in PBF format
            await self._save_file()
        # Notifies the queue that data has been processed
        self._results.task_done()

    async def _save_file(self):
        input_file = 'data/result.shp'
        output_file = 'data/result.pbf'

        translation_object = ogr2pbf.TranslationBase()
        datasource = ogr2pbf.OgrDatasource(translation_object)
        datasource.open_datasource(input_file)

        osmdata = ogr2pbf.OsmData(translation_object)
        osmdata.process(datasource)

        datawriter = ogr2pbf.PbfDataWriter(output_file)
        osmdata.output(datawriter)

        # Causes the `file_saved` event
        await self.file_saved(filepath=output_file)
