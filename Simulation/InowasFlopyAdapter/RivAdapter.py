import flopy.modflow as mf


class RivAdapter:
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
        return mf.ModflowRiv(
            _mf,
            ipakcb=content['ipakcb'],
            stress_period_data=content['stress_period_data'],
            dtype=content['dtype'],
            extension=content['extension'],
            unitnumber=content['unitnumber'],
            options=content['options']
        )

    @staticmethod
    def default():
        default = {
            "ipakcb": 0,
            "stress_period_data": None,
            "dtype": None,
            "extension": "riv",
            "unitnumber": 18,
            "options": None
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "ipakcb": package.ipakcb,
            "stress_period_data": package.stress_period_data,
            "dtype": package.dtype,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
            "options": package.options
        }
        return content
