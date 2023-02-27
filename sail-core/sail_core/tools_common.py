import json
from typing import Dict

import numpy


def check_instance(instance, class_check) -> None:
    if not isinstance(instance, class_check):
        raise Exception(f"{instance} is not instance of class: {class_check} instead type is {type(instance)}")


def sanitize_dict_for_json(dict_in: Dict) -> Dict:
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, numpy.integer):
                return int(obj)
            if isinstance(obj, numpy.floating):
                return float(obj)
            if isinstance(obj, numpy.ndarray):
                return obj.tolist()
            return super(NpEncoder, self).default(obj)

    return json.loads(json.dumps(dict_in, cls=NpEncoder))
