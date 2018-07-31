"""
This module is an intermediate layer between flopy version 3.2
and the inowas-modflow-configuration format.

Author: Ralf Junghanns
EMail: ralf.junghanns@gmail.com
"""

from .ReadBudget import ReadBudget
from .ReadDrawdown import ReadDrawdown
from .ReadHead import ReadHead
from .ReadFile import ReadFile


class InowasFlopyReadAdapter:
    """The Flopy Class"""

    _request = None
    _projectfolder = None
    _version = None

    def __init__(self, version, projectfolder, request):
        self._request = request
        self._projectfolder = projectfolder
        self._version = version
        pass

    def read_head(self, totim, layer):
        head_file = ReadHead(self._projectfolder)
        return head_file.read_layer(totim=totim, layer=layer)

    def read_head_ts(self, layer, row, column):
        head_file = ReadHead(self._projectfolder)
        return head_file.read_ts(layer=layer, row=row, column=column)

    def read_drawdown(self, totim, layer):
        drawdown_file = ReadDrawdown(self._projectfolder)
        return drawdown_file.read_layer(totim=totim, layer=layer)

    def read_drawdown_ts(self, layer, row, column):
        drawdown_file = ReadDrawdown(self._projectfolder)
        return drawdown_file.read_ts(layer=layer, row=row, column=column)

    def read_cumulative_budget(self, totim):
        budget_file = ReadBudget(self._projectfolder)
        return budget_file.read_cumulative_budget(totim=totim)

    def read_incremental_budget(self, totim):
        budget_file = ReadBudget(self._projectfolder)
        return budget_file.read_incremental_budget(totim=totim)

    def read_file(self, extension):
        namfile = ReadFile(self._projectfolder)
        return namfile.read_file(extension)

    def read_file_list(self):
        namfile = ReadFile(self._projectfolder)
        return namfile.read_file_list()

    def response(self):

        data = None
        request = self._request

        if 'budget' in request:
            if request['budget']['type'] == 'cumulative':
                totim = request['budget']['totim']
                data = self.read_cumulative_budget(totim=totim)

            if request['budget']['type'] == 'incremental':
                totim = self._request['totim']
                data = self.read_incremental_budget(totim=totim)

        if 'layerdata' in request:
            if request['layerdata']['type'] == 'head':
                totim = request['layerdata']['totim']
                layer = request['layerdata']['layer']
                data = self.read_head(totim=totim, layer=layer)

            if request['layerdata']['type'] == 'drawdown':
                totim = request['layerdata']['totim']
                layer = request['layerdata']['layer']
                data = self.read_drawdown(totim=totim, layer=layer)

        if 'file' in request:
            data = [self.read_file(request['file'])]

        if 'filelist' in request:
            data = self.read_file_list()

        if 'timeseries' in request:
            if request['timeseries']['type'] == 'head':
                layer = request['timeseries']['layer']
                row = request['timeseries']['row']
                column = request['timeseries']['column']
                data = self.read_head_ts(layer=layer, row=row, column=column)

            if request['timeseries']['type'] == 'drawdown':
                layer = request['timeseries']['layer']
                row = request['timeseries']['row']
                column = request['timeseries']['column']
                data = self.read_drawdown_ts(layer=layer, row=row, column=column)

        if data is not None:
            return dict(
                status_code=200,
                request=request,
                response=data
            )

        return dict(
            status_code=500,
            message="Internal Server Error. Request data does not fit."
        )
