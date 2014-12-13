from abc import ABCMeta
from abc import abstractmethod
from collections import MutableSequence

class Command(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        """Execute the command"""


class UndoableCommand(Command):
    @abstractmethod
    def unexecute(self):
        """Reverses the effects of execute"""


class MacroCommand(Command, MutableSequence):
    def __init__(self, command_list=None):
        self.command_list = []
        if command_list:
            self.command_list.extend(command_list)

    def __len__(self):
        return len(self.command_list)

    def __getitem__(self, index):
        return self.command_list[index]

    def __setitem__(self, index, value):
        self.command_list[index] = value

    def __delitem__(self, index):
        del self.command_list[index]

    def insert(self, index, value):
        self.command_list.insert(index, value)

    def execute(self):
        for command in self.command_list:
            command.execute()


class UndoableMacroCommand(UndoableCommand, MacroCommand):
    def unexecute(self):
        for command in reversed(self.command_list):
            command.unexecute()


class RecoverableException(Exception):
    def __init__(self, msg, exception):
        self.msg = msg
        self.exception = exception


class RollbackMacroCommand(UndoableMacroCommand):
    def execute(self):
        completed_commands = []
        for command in self.command_list:
            try:
                command.execute()
            except RecoverableException as e:
                #log
                for completed_command in completed_commands:
                    completed_command.unexecute()

            completed_commands.append(command)

if __name__ == '__main__':
    class Printer(UndoableCommand):
        def execute(self):
            print 'execute'

        def unexecute(self):
            print 'unexecute'

    printer_macro = UndoableMacroCommand(
        command_list=[
            Printer(),
            Printer(),
            Printer()])

    printer_macro.execute()
    printer_macro.unexecute()
