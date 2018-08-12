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

    @property
    def titleTag(self):
        return self.__titleTag

    @property
    def genreTag(self):
        return self.__genreTag
