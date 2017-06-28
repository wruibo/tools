"""
    data structure
"""
from ds.data import Data


def extract(data, *columns):
    """
        extract values from data object or data object list
    :param data: data object or data object list
    :param columns: column number want to extract, like: 1, 2
    :return: list of data extracted
    """

    def extract_data(data, *columns):
        extracted_values, values = [], data.values()
        for col in columns:
            extracted_values.append(values[col-1])
        if len(columns)>1:
            return extracted_values
        return extracted_values[0]

    # input data is @Data object, extract one record
    if issubclass(data.__class__, Data):
        return extract_data(data, *columns)

    #input data is @Data object list, extract record list
    if isinstance(data, list) or isinstance(data, tuple):
        extracted_values = []
        for item in data:
            extracted_values.append(extract_data(item, *columns))
        return extracted_values

    return None
