import json


class ReadJSON:
    def __init__(self, directory='./', filename='file'):
        self.__FILENAME = filename
        self.__DIRECTORY = self.__init_directory(directory)

    def __init_directory(self, directory):
        if directory != './':
            return directory + '/'
        else:
            return directory

    def __open_file(self, directory, filename, mode='r'):
        return open(f'{self.__init_directory(directory)}{filename}.json', mode, encoding='utf8')

    def append_object(self, object={}):
        if object != {}:
            outfile = self.__open_file(self.__DIRECTORY, self.__FILENAME, 'a')
            json.dump(object, outfile)
            outfile.write('\n')
            outfile.close()

    def write_list(self, list=[]):
        if list != []:
            outfile = self.__open_file(self.__DIRECTORY, self.__FILENAME, 'w')
            json.dump(list, outfile)
            outfile.close()

    def read(self, directory='./', filename='file'):
        try:
            outfile = self.__open_file(directory, filename)
            json_data = json.load(outfile)

            if str(type(json_data)) != "<class 'dict'>":
                return json_data
            else:
                raise json.decoder.JSONDecodeError("Extra data", '1', 2)

        except json.decoder.JSONDecodeError:
            outfile = self.__open_file(directory, filename)
            return [json.loads(line) for line in outfile]

        except FileNotFoundError:
            return []