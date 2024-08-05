import os
import re
import subprocess
import xml.etree.ElementTree as ET
import psutil
from wotclientdetection.constants import *

class Client:

    def __init__(self, path, launcher_flavour, is_preffered=False):
        self.branch = ClientBranch.UNKNOWN
        self.launcher_flavour = launcher_flavour
        self.l10n = None
        self.path = path
        self.path_mods = None
        self.path_resmods = None
        self.realm = None
        self.type = ClientType.UNKNOWN
        self.client_version = None
        self.exe_version = None
        self.is_preffered = is_preffered
        self.is_valid = self.__is_valid()
        self.__read_client_data()

    def update(self):
        self.__invalidate()
        self.__read_client_data()

    def is_version_match(self, pattern):
        regex = re.compile(pattern)
        match = regex.match(self.client_version)
        return bool(match)

    def is_started(self):
        for process in psutil.process_iter():
            if process is None:
                continue
            if process.name() != EXECUTABLE_NAME:
                continue
            if self.path in process.cwd():
                return True
        return False

    def run(self, replay_path=None):
        executable_path = os.path.normpath(os.path.join(self.path, EXECUTABLE_NAME))
        if not os.path.isfile(executable_path):
            return
        launch_args = [executable_path]
        if replay_path is not None:
            launch_args.append(replay_path)
        try:
            subprocess.run(executable_path, shell=True)
            return True
        except:
            pass
        return False

    def terminate(self):
        for process in psutil.process_iter():
            if process is None:
                continue
            if process.name() != EXECUTABLE_NAME:
                continue
            if self.path in process.cwd():
                process.terminate()
                return True
        return False

    def __read_client_data(self):
        if not self.is_valid:
            return
        self.__invalidate()
        self.__read_app_type()
        self.__read_exe_version()
        self.__read_version()
        self.__read_game_info()
        self.__read_paths()

    def __read_app_type(self):
        app_type_path = os.path.normpath(os.path.join(self.path, 'app_type.xml'))
        if not os.path.isfile(app_type_path):
            return
        app_type_xml = ET.parse(app_type_path)
        root = app_type_xml.getroot()
        element = root.find('app_type')
        if element is None:
            return
        app_type = element.text.strip().lower()
        if app_type == 'hd':
            self.type = ClientType.HD
        elif app_type == 'sd':
            self.type = ClientType.SD

    def __read_exe_version(self):
        pass

    def __read_version(self):
        version_path = os.path.normpath(os.path.join(self.path, 'version.xml'))
        if not os.path.isfile(version_path):
            return
        version_xml = ET.parse(version_path)
        root = version_xml.getroot()
        element = root.find('meta/realm')
        if element is not None:
            self.realm = element.text.strip()
        element = root.find('version')
        if element is None:
            return
        version = element.text.strip()
        version = version.replace('v.', '')
        version = version.split()[:-1]
        version = ' '.join(version)
        version = version.split(None, 1)
        self.client_version = version[0]
        if len(version) == 2:
            branch = version[1]
            if branch == 'Common Test':
                self.branch = ClientBranch.COMMON_TEST
            elif branch == 'ST':
                self.branch = ClientBranch.SUPERTEST
            elif branch == 'SB':
                self.branch = ClientBranch.SANDBOX
            return
        if self.branch == ClientBranch.UNKNOWN:
            self.branch = ClientBranch.RELEASE

    def __read_game_info(self):
        game_info_path = os.path.normpath(os.path.join(self.path, 'game_info.xml'))
        if not os.path.isfile(game_info_path):
            return
        game_info_xml = ET.parse(game_info_path)
        root = game_info_xml.getroot()
        element = root.find('game/id')
        if element is not None:
            id = element.text.strip()
            if '.RPT.' in id:
                self.branch = ClientBranch.COMMON_TEST
        element = root.find('game/localization')
        if element is None:
            return
        self.l10n = element.text.strip()

    def __read_paths(self):
        paths_path = os.path.normpath(os.path.join(self.path, 'paths.xml'))
        if not os.path.isfile(paths_path):
            return
        paths_xml = ET.parse(paths_path)
        root = paths_xml.getroot()
        elements = root.findall('Paths/Path')
        if elements is None:
            return
        for element in elements:
            path = element.text.strip()
            path = path.replace('./', '')
            path = path.replace('/', '\\')
            if path.startswith('res_mods'):
                self.path_resmods = path
            elif path.startswith('mods'):
                self.path_mods = path

    def __is_valid(self):
        if not os.path.isdir(self.path):
            return False
        for file in ('app_type.xml', 'game_info.xml', 'paths.xml', 'version.xml', EXECUTABLE_NAME):
            if not os.path.isfile(os.path.join(self.path, file)):
                return False
        return True

    def __invalidate(self):
        self.branch = ClientBranch.UNKNOWN
        self.l10n = None
        self.path_mods = None
        self.path_resmods = None
        self.realm = None
        self.type = ClientType.UNKNOWN
        self.client_version = None
        self.exe_version = None

    def __repr__(self):
        return (f'<Client branch={self.branch} launcherFlavour={self.launcher_flavour} l10n={self.l10n} path={self.path} pathMods={self.path_mods} pathResmods={self.path_resmods} realm={self.realm} type={self.type} clientVersion={self.client_version} exeVersion={self.exe_version} isPreffered={self.is_preffered}>')
