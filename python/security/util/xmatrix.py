"""
    normal matrix process methods
"""


def rotate(matrix=[[]]):
    """
        rotate matrix with its ranks, rows to columns and columns to rows, example:
    before transform, there are N column list like:

         column1 column2 ... columnN
           v11    v21          vN1
           v12    v22          vN2
            .      .            .
            .      .            .
            .      .            .
           v1M     v2M          VNM

    after transform, the result is:

      row1 v11    v21          vN1
      row2 v12    v22          vN2
            .      .            .
            .      .            .
            .      .            .
      rowM v1M     v2M          VNM
    :param matrix: matrix
    :return: rotated matrix
    """

    rotated_matrix = []

    for i in range(0, len(matrix[0])):
        values = []
        for j in range(0, len(matrix)):
            values.append(matrix[j][i])
        rotated_matrix.append(values)

    return rotated_matrix

