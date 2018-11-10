class AudioItem:
    def __init__(self, master, source, fileName, audioFile, artistTag, titleTag, genreTag):

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
        print(value)
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
