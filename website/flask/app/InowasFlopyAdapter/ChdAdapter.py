import flopy.modflow as mf


class ChdAdapter:
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

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowChd(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "stress_period_data": None,
            "dtype": None,
            "extension": 'chd',
            "unitnumber": 24
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            # stress period data values translated to list of lists to be json serializable
            "stress_period_data": {k: [list(i) for i in v] for k, v in package.stress_period_data.data.items()},
            # "dtype": package.dtype,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
