import flopy.modflow as mf


class OcAdapter:
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

        if 'stress_period_data' in self._data:
            default['stress_period_data'] = self.get_stress_period_data(self._data['stress_period_data'])

        return default

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowOc(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "ihedfm": 0,
            "iddnfm": 0,
            "chedfm": None,
            "cddnfm": None,
            "cboufm": None,
            "compact": True,
            "stress_period_data": None,
            "extension": ['oc', 'hds', 'ddn', 'cbc'],
            "unitnumber": [14, 51, 52, 53]
        }

        return default

    @staticmethod
    def get_stress_period_data(stress_periods):
        if stress_periods is None:
            return stress_periods

        stress_period_data = {}
        for stress_period in stress_periods:
            stress_period_data[stress_period['stressPeriod'], stress_period['timeStep']] = stress_period['type']

        return stress_period_data

    @staticmethod
    def read_package(package):
        content = {
            "ihedfm": package.ihedfm,
            "iddnfm": package.iddnfm,
            "chedfm": package.chedfm,
            "cddnfm": package.cddnfm,  # None
            "cboufm": package.cboufm,  # None
            "compact": package.compact,
            # stress period data dict keys transformed from tuple to string to be json serializable
            "stress_period_data": {str(k): v for k, v in package.stress_period_data.items()},
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
