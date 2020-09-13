from typing import Dict, Tuple


def value_to_ratio(xtalk_dict_dict: Dict[Tuple[str], Dict[Tuple[str], str]] = None, threshold: float = 0):
    result = {}
    for twoQcon, pairs in xtalk_dict_dict.items():
        for pair, value in pairs.items():
            ratio = value / xtalk_dict_dict[twoQcon][twoQcon]
            if ratio > threshold:
                try:
                    result[twoQcon][pair] = ratio
                except:
                    result[twoQcon] = {}
                    result[twoQcon][pair] = ratio
    return result


def extact_date_ratio(daily_dictdict, date):
    """
    data_dict = {
        (0, 1): {(0, 1): {"2020-07-17": 0.0051, "2020-07-18": 0.0055}}}
    """
    result = {}
    for twoQcon, pairs_dict in daily_dictdict.items():
        result[twoQcon] = {}
        for pair, daily_errors in pairs_dict.items():
            if twoQcon == pair:
                pass
            else:
                try:
                    base_err = pairs_dict[twoQcon][date]
                    pair_err = daily_errors[date]
                    ratio = pair_err / base_err
                    result[twoQcon][pair] = ratio
                except:
                    pass
    return result
