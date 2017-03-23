# encoding: utf-8
class Note():
    """ Represents a note
    """
    def __init__(self, note_text, category, dimension):
        """ :param note_text (str): The note content
            :param category (str): The category that the note describes
            :param dimension (Dimension): The dimension that the category belongs to
        """
        self.note = note_text
        self.dimension = dimension
        self.category = dimension.get(category)

        if self.category == None:
            msg = u"Error creating note. '{}' is not a valid category for {}.".format(category.decode("utf-8"), dimension)
            raise Exception(msg)