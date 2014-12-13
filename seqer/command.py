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
    @staticmethod
    def run(command_list, do, undo):
        completed_command_list = []
        for command in command_list:
            try:
                if hasattr(command, do):
                    getattr(command, do)()
                else:
                    #log
                    pass
            except RecoverableException as e:
                #log
                for completed_command in reversed(completed_command_list):
                    if hasattr(command, undo):
                        getattr(completed_command, undo)
                break
            completed_command_list.append(command)

    def execute(self):
        RollbackMacroCommand.run(
            command_list=self.command_list,
            do='execute',
            undo='unexecute')

    def unexecute(self):
        RollbackMacroCommand.run(
            command_list=reversed(self.command_list),
            do='unexecute',
            undo='execute')

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

    print '-' * 80

    class NonUndoableCommand(Command):
        def execute(self):
            print 'nonundoable command'

    class Raiser(Command):
        def execute(self):
            print 'exeception'
            raise RecoverableException('exception occured', None)

    rollback_macro_command = RollbackMacroCommand(
        command_list=[
            Printer(),
            NonUndoableCommand(),
            Printer(),
            Raiser()])

    rollback_macro_command.execute()
    rollback_macro_command.unexecute()
