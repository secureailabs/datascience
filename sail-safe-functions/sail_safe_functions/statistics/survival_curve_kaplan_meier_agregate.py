from typing import Dict, List

import numpy
from lifelines.utils import inv_normal_cdf


class SurvivalCurveKaplanMeierAgregate:
    def run(list_survival_curve_dict: List) -> Dict:
        count_total = 0
        count_observed = 0
        domain = []
        for survival_curve_dict in list_survival_curve_dict:
            if survival_curve_dict["count_total"] == 0:
                continue
            count_total += survival_curve_dict["count_total"]
            count_observed += survival_curve_dict["count_observed"]
            # TODO these domain values need to get fudged for privacy reasons
            domain.extend(survival_curve_dict["domain"][1:])
        domain = sorted(domain)

        mean = 1 - (numpy.array(list(range(1, len(domain) + 1))) / count_total)
        mean = mean.tolist()
        domain.insert(0, 0.0)
        mean.insert(0, 1.0)
        lower, upper = SurvivalCurveKaplanMeierAgregate.bounds(mean, count_total)
        survival_curve_dict = {}
        survival_curve_dict["count_total"] = count_total
        survival_curve_dict["count_observed"] = count_observed
        survival_curve_dict["domain"] = domain
        survival_curve_dict["mean"] = mean
        survival_curve_dict["lower"] = lower
        survival_curve_dict["upper"] = upper

        return survival_curve_dict

    @staticmethod
    def bounds(mean, count_total, alpha=0.05):
        # This is a poor proxy for the bounds version used in kaplan me
        # the orginal from the lifelines library was buid on the exponential Greenwood formula.
        # See https://www.math.wustl.edu/%7Esawyer/handouts/greenwood.pdf

        # (deaths / (population * (population - deaths)))
        # population = count_total
        scale = numpy.ones(len(mean))
        for i in range(len(scale)):
            scale[i] = i / (count_total * (count_total - i))

        z = inv_normal_cdf(1 - alpha / 2)
        v = numpy.log(mean)
        lower = numpy.exp(-numpy.exp(numpy.log(-v) - z * numpy.sqrt(scale) / v))
        upper = numpy.exp(-numpy.exp(numpy.log(-v) + z * numpy.sqrt(scale) / v))
        # filty haxxor here as well, not sure this is correct but it matches
        lower[0] = 1.0
        upper[0] = 1.0
        lower[-1] = lower[-2]
        upper[-1] = upper[-2]
        return lower, upper
