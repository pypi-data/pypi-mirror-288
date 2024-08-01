from webdrivermanager_cn.core import mirror_urls as urls
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.request import request_get
from webdrivermanager_cn.core.version_manager import GetClientVersion, ClientType


class EdgeDriver(DriverManager):
    def __init__(self, version=None, path=None):
        self.__download_version = version
        super().__init__(driver_name="edgedriver", version=self.version, root_dir=path)
        # self.driver_version = self.version

    @property
    def get_driver_name(self) -> str:
        return f"{self.driver_name}_{self.get_os_info}.zip"

    @property
    def get_os_info(self):
        _os_info = self.os_info.get_os_type
        if self.os_info.get_mac_framework in ["_m1", "_m2"]:
            _os_info += "_m1"
        return _os_info

    @property
    def download_url(self) -> str:
        return f"{urls.EdgeDriverUrl}/{self.driver_version}/{self.get_driver_name}"

    # @property
    # def version_bak(self):
    #     """
    #     根据传入版本，或者自动获取的Edge版本，获取匹配的webdriver版本
    #     弃用，仅保留逻辑
    #     :return:
    #     """
    #     if self.__download_version not in ['latest', None]:
    #         client_version = self.__download_version
    #     else:
    #         client_version = GetClientVersion().get_version(ClientType.Edge)
    #     client_version_parser = GetClientVersion(client_version)
    #     _os_name = self.os_info.get_os_name
    #     if _os_name == OSType.WIN:
    #         suffix = "windows"
    #     elif _os_name == OSType.MAC:
    #         suffix = "macos"
    #     else:
    #         suffix = OSType.LINUX
    #     latest_url = f"{urls.EdgeDriverUrl}/LATEST_RELEASE_{client_version_parser.version_obj.major}_{suffix.upper()}"
    #     return request_get(latest_url).text.strip()

    @property
    def version(self):
        if self.__download_version in ['latest', None]:
            try:
                self.__download_version = GetClientVersion().get_version(ClientType.Edge)
            except:
                pass
        if not self.__download_version:
            self.__download_version = self.__get_latest_version
        self.log.info(f'下载版本: {self.__download_version}')
        return self.__download_version

    @property
    def __get_latest_version(self):
        return request_get(f"{urls.EdgeDriverUrl}/LATEST_STABLE").text.strip()
