##########################################################################
#
#   A wrapper class for the pypubsub extension providng any required extras
#   for the pubsub schema
#
#   NOTE:
#       This is a Singleton class, the whole application must use the
#       same instance.
#
##########################################################################

from pubsub import pub

##########
#
#   ctxLink subscription topics
#
##########

###
#
#   Load the requested ELF file:
#       The Main Window of the UI sends this request.
#
#       The Variable Manager listens to this topic, it loads the file and
#       creates the database of variables defined in the file.
TOPIC_ELF_FILE_LOAD = 'root.load_elf_file'

###
#
#   Close the current ELF file:
#       The Main Window of the UI sends this request.
#
#       The Variable Manager listens to this topic, it flushes the
#       symbols and publishes an empty database
TOPIC_ELF_FILE_CLOSE = 'root.close_elf_file'

###
#
#   Subscribe to the database of variables:
#       The main window of the UI sends this request.
#
#       The VariableManager sends the database to this topic when
#       it changes
TOPIC_VARIABLE_DB = 'root.variable_database'


class Ctx_PubSub():
    __instance = None

    @staticmethod
    def getInstance():
        '''
            Static access method
        '''
        if Ctx_PubSub.__instance == None:
            Ctx_PubSub()
        return Ctx_PubSub.__instance

    def __init__(self):
        '''
            Virtually private constructor
        '''
        if Ctx_PubSub.__instance != None:
            raise Exception('This class is a singleton')
        else:
            Ctx_PubSub.__instance = self

    ###
    #
    #   Send message to request loading the given elf file. Filename
    #   must be fully-qualified path/name
    #
    def send_load_elf_file(self, elf_filename):
        pub.sendMessage(TOPIC_ELF_FILE_LOAD, elf_file=elf_filename)

    ###
    #
    #   Send message to request closing the current elf file
    #
    def send_close_elf_file(self):
        pub.sendMessage(TOPIC_ELF_FILE_CLOSE)

    ###
    #
    #   Subscribe to the load elf topic
    #
    def subscribe_load_elf_file(self, listener):
        pub.subscribe(listener, TOPIC_ELF_FILE_LOAD)

    ###
    #
    #   Subscribe to the close elf topic
    #
    def subscribe_close_elf_file(self, listener):
        pub.subscribe(listener, TOPIC_ELF_FILE_CLOSE)

    ###
    #
    #   Send the given database topic to listeners
    #
    def send_variable_database(self, database):
        pub.sendMessage(TOPIC_VARIABLE_DB, symbols=database)

    ###
    #
    #   Subscribe to the variable database topic
    #
    def subscribe_variable_database(self, listener):
        pub.subscribe(listener, TOPIC_VARIABLE_DB)


def myElf_Listener(elf_file):
    print(elf_file)


def myDatabase_Listener(data):
    print(data)


if __name__ == '__main__':
    # s = Ctx_PubSub()
    # print(s)
    s = Ctx_PubSub.getInstance()
    print(s)
    s = Ctx_PubSub.getInstance()
    print(s)
    # pubsub_manager = Ctx_PubSub()
    # pubsub_manager.subscribe_load_elf_file(myElf_Listener)
    # pubsub_manager.subscribe_variable_database(myDatabase_Listener)
    # pubsub_manager.send_load_elf_file('this file')
    # somedata = {"one": "value_one", "two": "value_two"}
    # pubsub_manager.send_variable_database(somedata)
