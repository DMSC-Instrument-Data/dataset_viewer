class FileReader(object):

    def file_to_dictionary(file_path):

        try:
            file = open(file_path, "r")
        except FileNotFoundError:
            pass

        if empty_file(file):
            raise Error
