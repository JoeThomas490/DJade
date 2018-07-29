class AudioItem:
    def __init__(self,master, source, fileName, artistTag, titleTag, genreTag):

        self.source = source
        self.fileName = fileName

        self.__artistTag = artistTag
        self.__titleTag = titleTag
        self.__genreTag = genreTag

    @property
    def artistTag(self):
        return self.__artistTag.text[0]

    @property
    def titleTag(self):
        return self.__titleTag.text[0]

    @property
    def genreTag(self):
        return self.__genreTag.text[0]