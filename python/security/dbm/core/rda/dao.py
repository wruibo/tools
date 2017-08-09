"""
    data access object
"""


class dao:
    """
        data process object
    """
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    def decode(self, encoding='utf-8'):
        """
            decode bytes to string
        :param encoding:
        :return:
        """
        data = self._data.decode(encoding)
        self._data = data

        return self

    def decodes(self, encoding='utf-8'):
        """
            decode data to string
        :param encoding:
        :return:
        """
        datas = []
        for name, data in self._data:
            datas.append([name, data.decode(encoding)])
        self._data = datas

        return self

    def unzip(self):
        """
            unzip data to datas
        :return:
        """
        import io, zipfile

        datas = []
        zf = zipfile.ZipFile(io.BytesIO(self._data))
        for name in zf.namelist():
            datas.append([name, zf.read(name)])

        self._data = datas

        return self

    def json(self):
        """
            current data is text, decode to json object
        :return:
        """
        import json

        data = json.loads(self._data)
        self._data = data

        return self

    def jsons(self):
        """

        :return:
        """
        import json

        datas = []
        for name, data in self._data:
            datas.append([name, json.loads(data)])
        self._data = datas

        return self

    def xml(self):
        """
            current data is text, decode to xml object
        :return:
        """
        import xml.dom.minidom

        data = xml.dom.minidom.parseString(self._data)
        self._data = data

        return self

    def xmls(self):
        """

        :return:
        """
        import xml.dom.minidom

        datas = []
        for name, data in self._data:
            datas.append([name, xml.dom.minidom.parseString(self._data)])
        self._data = datas

        return self

    def csv(self):
        """

        :return:
        """
        import io, csv

        data = csv.reader(io.BytesIO(self._data))
        self._data = data

        return self

    def csvs(self):
        """

        :return:
        """
        import io, csv

        datas = []
        for name, data in self._data:
            datas.append([name, csv.reader(io.StringIO(data))])
        self._data = datas

        return self

    def xls(self):
        """
            extract data to excel
        :return:
        """
        import xlrd

        data = xlrd.open_workbook(file_contents=self.data)
        self._data = data

        return self

    def xlss(self):
        """

        :return:
        """
        import xlrd

        datas = []
        for name, data in self._data:
            datas.append([name, xlrd.open_workbook(file_contents=data)])
        self._data = datas

        return self

if __name__ == "__main__":
    path = "/Users/polly/Downloads/sz_fzb_000001_2015_2017.zip"
    dao = dao(open(path, 'rb').read())
    csvs = dao.unzip().decodes('gb2312').csvs()
    for name, data in csvs.data:
        print(name)
        for row in data:
            print(row)