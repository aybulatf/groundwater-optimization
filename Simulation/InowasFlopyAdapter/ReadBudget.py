import os
from flopy.utils.mflistfile import MfListBudget


class ReadBudget:
    _filename = None

    def __init__(self, workspace):
        for file in os.listdir(workspace):
            if file.endswith(".list"):
                self._filename = os.path.join(workspace, file)
        pass

    def read_times(self):
        try:
            mf_list = MfListBudget(self._filename)
            if mf_list.get_times():
                return mf_list.get_times()
            else:
                return []
        except:
            return []

    def read_cumulative_budget(self, totim):
        try:
            mf_list = MfListBudget(self._filename)
            budget = mf_list.get_data(totim=totim, incremental=False)
            values = {}
            for x in budget:
                param = str(x[2].decode('UTF-8'))
                values[param] = str(x[1])
            return values
        except:
            return []

    def read_incremental_budget(self, totim):
        try:
            mf_list = MfListBudget(self._filename)
            budget = mf_list.get_data(totim=totim, incremental=True)
            values = {}
            for x in budget:
                param = str(x[2].decode('UTF-8'))
                values[param] = str(x[1])
            return values
        except:
            return []
