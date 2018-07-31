import flopy.mt3d as mt


class TobAdapter:

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
        return mt.Mt3dTob(
                _mt,
                **content
            )

    @staticmethod
    def default():
        default = {
            "outnam": 'tob_output',
            "CScale": 1.0, 
            "FluxGroups": [],
            "FScale": 1.0,
            "iOutFlux": 0,
            "extension": 'tob',
            "unitnumber": None,
            "filenames": None
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "outnam": package.outnam,
            "CScale": package.CScale, 
            "FluxGroups": package.FluxGroups,
            "FScale": package.FScale,
            "iOutFlux": package.iOutFlux,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
            "filenames": package.filenames
        }
        return content
