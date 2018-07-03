import flopy.mt3d as mt


class GcgAdapter:
    _data = None

    def __init__(self, data):
        self._data = data

    def validate(self):
        # should be implemented
        # for key in content:
        #   do something
        #   return some hints
        pass

    def is_valid(self):
        # should be implemented
        # for key in content:
        #   do something
        #   return true or false
        return True

    def merge(self):
        default = self.default()
        for key in self._data:
            default[key] = self._data[key]
        return default

    def get_package(self, _mt):
        content = self.merge()
        return mt.Mt3dGcg(
            _mt,
            **content
        )

    @staticmethod
    def default():
        default = {
            "mxiter": 1,
            "iter1": 50,
            "isolve": 3,
            "ncrs": 0,
            "accl": 1,
            "cclose": 1e-05,
            "iprgcg": 0,
            "extension": 'gcg',
            "unitnumber": None
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "mxiter": package.mxiter,
            "iter1": package.iter1,
            "isolve": package.isolve,
            "ncrs": package.ncrs,
            "accl": package.accl,
            "cclose": package.cclose,
            "iprgcg": package.iprgcg,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
