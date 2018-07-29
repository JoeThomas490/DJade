import json
import io

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

class SaveManager:
    def __init__(self, master):
        self.master = master

    def saveData(self,data):
        with io.open('../data.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))

    def loadData(self):
        with open('../data.json', 'r', encoding='utf8') as outfile:
            try:
                data = json.load(outfile)
                return data

            except IOError:
                print("Data file empty!")