import os
import sys
from argparse import ArgumentParser
from typing import List, Tuple, Optional

from .console import clear, black, blue, yellow, green, red, cyan, purple


class FileManager:

    def __init__(self, root_dir: str):
        self._root_dir = root_dir
        self._last_error = None
        self._list_entries: Optional[List[str]] = None
        self._menu_items = [
            (('MENU',), 'Menu', self.menu,
             ['MENU']),
            (('LIST',), 'List Entries', self.list_entries,
             ['LIST',
              'LIST LIKE <pattern>...',
              'LIST LINKS',
              'LIST LINKS LIKE <pattern>...',
              'LIST AGAIN',
              'LIST LINKS AGAIN']),
            (('VIEW',), 'View Entry', self.view_entry,
             ['VIEW <index>']),
            (('OPEN',), 'Open Entry', self.open_entry,
             ['OPEN <index>']),
            (('RENAME',), 'Rename Entry', self.rename_entry,
             ['RENAME <index> TO <new-name>']),
            (('GO', 'GOTO'), 'Go to an Entry', self.go_to_entry,
             ['GO TO <index>',
              'GOTO <index>',
              'GO BACK',
              'GO HOME']),
            (('RETURN',), 'Return to prior Entry', self.go_back,
             ['RETURN']),
            (('DELETE',), 'Delete an Entry', self.delete_entry,
             ['DELETE <index>']),
            (('HELP',), 'Help', self.help,
             ['HELP <command>']),
            (('QUIT', 'EXIT'), 'Quit App', self.quit_app,
             ['QUIT',
              'EXIT']),
        ]
        self._database_dir = os.path.join(self._root_dir, 'Database')
        if not os.path.lexists(self._database_dir):
            print(f'{red}Missing folder {self._database_dir}')
            yesno = input(f'{yellow}Would you like to create the missing folder [N] ? {black}')
            if yesno.upper().startswith('Y'):
                os.makedirs(self._database_dir)
            if not os.path.lexists(self._database_dir):
                raise RuntimeError(f'Missing folder {self._database_dir}')
        self._dir_history = [self._database_dir]

    def _cur_dir(self):
        return self._dir_history[-1]

    def _push_dir_path(self, path: str):
        self._dir_history.append(path)
        self._list_entries = None

    def _pop_dir_path(self):
        while len(self._dir_history) > 1:
            self._dir_history.pop()
            self._list_entries = None
            if os.path.lexists(self._cur_dir()):
                return
        return

    def _pop_to_home(self):
        self._dir_history = [self._dir_history[0]]
        return

    def list_entries(self, request: List[str]):
        like = None
        show_links = False
        if len(request) > 0:
            if request[0].upper() == 'LINKS':
                show_links = True
                request.pop(0)
        if len(request) > 0:
            if request[0].upper() == 'AGAIN':
                self._list_current_entries(show_links)
                return
        if len(request) > 1:
            if request[0].upper() == 'LIKE':
                like = ' '.join(request[1:]).upper()
        self._list_entries = sorted([entry for entry in os.listdir(self._cur_dir()) if like is None or like in entry.upper()])
        self._list_current_entries(show_links)

    def _list_current_entries(self, show_links=False):
        for index, entry in enumerate(self._list_entries):
            entry_path = os.path.join(self._cur_dir(), entry)
            if os.path.islink(entry_path):
                link_target = self.rel_path(os.path.realpath(entry_path))
                if os.path.isdir(entry_path):
                    if show_links:
                        print(f'{blue}{index+1:3} - {entry} {cyan}({link_target}){black}')
                    else:
                        print(f'{blue}{index+1:3} - {entry}{black}')
                elif os.path.isfile(entry_path):
                    if show_links:
                        print(f'{purple}{index+1:3} - {entry} {cyan}({link_target}){black}')
                    else:
                        print(f'{purple}{index+1:3} - {entry}{black}')
                else:
                    if show_links:
                        print(f'{red}{index+1:3} - {entry} {cyan}({link_target}){black}')
                    else:
                        print(f'{red}{index+1:3} - {entry}{black}')
            elif os.path.isdir(entry_path):
                print(f'{blue}{index+1:3} - {entry}{black}')
            elif os.path.isfile(entry_path):
                print(f'{purple}{index+1:3} - {entry}{black}')
            else:
                print(f'{red}{index+1:3} - {entry}{black}')

    def view_entry(self, request: List[str]):
        print(f'{red}Not implemented yet{black}')

    def open_entry(self, request: List[str]):
        for item in request:
            entry, index = self._lookup_index_entry(item)
            entry_path = os.path.join(self._cur_dir(), entry)
            if os.path.lexists(entry_path):
                if os.path.isfile(entry_path):
                    print(f'{green}Open {self.rel_path(entry_path)}{black}')
                    os.system(f'xdg-open \'{entry_path}\'')

    def delete_entry(self, request: List[str]):
        if len(request) == 1:
            entry, index = self._lookup_index_entry(request[0])
            entry_path = os.path.join(self._cur_dir(), entry)
            if not os.path.lexists(entry_path):
                raise ValueError(f'"{entry}" does not exist')
            if os.path.islink(entry_path):
                print(f'Deleting {self.rel_path(entry_path)}')
                yesno = input('Are you sure [N] ? ')
                if yesno.upper().startswith('Y'):
                    os.remove(entry_path)
                    del self._list_entries[index-1]
                    self._list_current_entries()
                return
            raise ValueError(f'Do not currently support deleting folders or files')
        self.help(['DELETE'])

    def rename_entry(self, request:List[str]):
        if len(request) >= 3:
            if request[1].upper() != 'TO':
                self.help(['RENAME'])
                return
            entry, index = self._lookup_index_entry(request[0])
            new_name = ' '.join(request[2:])
            new_path = os.path.join(self._cur_dir(), new_name)
            if os.path.lexists(new_path):
                raise ValueError(f'"{new_name}" already exists')
            entry_path = os.path.join(self._cur_dir(), entry)
            if not os.path.lexists(entry_path):
                raise ValueError(f'"{entry}" does not exist')
            if os.path.islink(entry_path):
                link_target = os.readlink(entry_path)
                if os.path.isdir(entry_path) or os.path.isfile(entry_path):
                    os.symlink(link_target, new_path)
                    if not os.path.lexists(new_path):
                        raise ValueError(f'Failed to create "{new_name}"')
                    self._list_entries[index-1] = new_name
                    self._list_entries.sort()
                    os.remove(entry_path)
                    if os.path.lexists(entry_path):
                        raise ValueError(f'Failed to remove old entry "{entry}"')
                    self._list_current_entries()
                    return
                else:
                    raise ValueError(f'Not allowed to change the entry')
            else:
                if os.path.isdir(entry_path):
                    references = self._find_references(entry_path)
                    print(f'{red}Not implemented yet for directories{black}')
                    return
                elif os.path.isfile(entry_path):
                    os.rename(entry_path, new_path)
                    if not os.path.lexists(new_path) or os.path.lexists(entry_path):
                        raise ValueError(f'Failed to rename to "{new_name}"')
                    self._list_entries[index-1] = new_name
                    self._list_entries.sort()
                    self._list_current_entries()
                    return
                else:
                    raise ValueError(f'Not allowed to change the entry')
        self.help(['RENAME'])

    def _find_references(self, entry_path: str) -> List[str]:
        pass

    def go_back(self, request: List[str]):
        self._pop_dir_path()
        return

    def go_to_entry(self, request: List[str]):
        if len(request) == 2:
            if request[0].upper() == 'TO':
                request.pop(0)
        if len(request) == 1:
            if request[0].upper() == 'HOME':
                self._pop_to_home()
                return
            if request[0].upper() == 'BACK':
                self._pop_dir_path()
                return
            entry, index = self._lookup_index_entry(request[0])
            new_path = os.path.realpath(os.path.join(self._cur_dir(), entry))
            if not os.path.isdir(new_path):
                raise ValueError(f'Not a directory: {self.rel_path(new_path)}')
            if not new_path.startswith(self._database_dir):
                raise ValueError(f'Not in the database: {self.rel_path(new_path)}')
            self._push_dir_path(new_path)
            return
        self.help(['GO'])

    def _lookup_index_entry(self, index: str) -> Tuple[str, int]:
        if not index.isdigit():
            raise ValueError(f'Index "{index}" is not a number')
        index = int(index)
        if index < 1 or index > len(self._list_entries):
            raise ValueError(f'Index "{index}" out of range')
        return self._list_entries[index-1], index

    def help(self, request: List[str]):
        if len(request) > 0:
            for command in request:
                for entry in self._menu_items:
                    if command.upper() in entry[0]:
                        for line in entry[3]:
                            print(f'{red}{line}{black}')
            return
        for entry in self._menu_items:
            for line in entry[3]:
                print(f'{red}{line}{black}')

    def quit_app(self, request: List[str]):
        print(f'{blue}Goodbye!{black}')
        print()
        sys.exit(0)

    def rel_path(self, path: str = None) -> str:
        if path is None:
            path = self._cur_dir()
        return os.path.relpath(path, self._root_dir)

    def menu(self, request: List[str]):
        clear()
        print(f'{blue}File Manager{black}')
        print(f'{blue}============{black}')
        print()
        for entry in self._menu_items:
            print(f'{blue}{entry[0][0]} = {entry[1]}{black}')

    def run(self):
        self.menu([])
        while True:
            if self._last_error is not None:
                print(f'{red}Error> {self._last_error}{black}')
                self._last_error = None
            print()
            print(f'{green}Folder> [{len(self._dir_history)}] {self.rel_path()}{black}')
            print()
            request = input(f'{yellow}Action ? {black}')
            print()
            self._perform_request(request)

    def _perform_request(self, request: str):
        if len(request) > 0:
            request = request.split(' ')
            action = request[0].upper()
            for entry in self._menu_items:
                if action in entry[0]:
                    print(f'{green}Action> {entry[1]}{black}')
                    print()
                    try:
                        entry[2](request[1:])
                    except Exception as e:
                        self._last_error = e
                    return
            self._last_error = ValueError(f'Action "{action}" is not recognised')


def main():
    default_folder = os.path.join(os.getenv('HOME'), '.local', 'docman')
    parser = ArgumentParser(description='Document Manager')
    parser.add_argument('-f', '--folder', help='Main Folder', default=default_folder)
    args = parser.parse_args()
    try:
        file_manager = FileManager(root_dir=args.folder)
        file_manager.run()
    except Exception as ex:
        print(f'{red}Error> {ex}{black}')


if __name__ == '__main__':
    main()
