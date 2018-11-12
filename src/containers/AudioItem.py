class AudioItem:
    def __init__(self, master, rowNum, source, fileName, audioFile, artistTag, titleTag, genreTag):

        self.__rowNum = rowNum

        self.source = source
        self.fileName = fileName

        self.__audioFile = audioFile
        self.__artistTag = artistTag
        self.__titleTag = titleTag
        self.__genreTag = genreTag

    @property
    def audioFile(self):
        return self.__audioFile

    @property
    def artistTag(self):
        return self.__artistTag

    @artistTag.setter
    def artistTag(self, value):
        self.__artistTag = value

    @property
    def titleTag(self):
        return self.__titleTag

    @titleTag.setter
    def titleTag(self, value):
        self.__titleTag = value

    @property
    def genreTag(self):
        return self.__genreTag

    @genreTag.setter
    def genreTag(self, value):
        self.__genreTag = value

    @property
    def rowNum(self):
        return self.__rowNum
