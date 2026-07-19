"""
配置管理器

负责管理程序的配置信息，使用 TOML 格式存储配置文件。
目前主要管理 readelf 程序的路径配置。
"""

import os
import toml

# 配置文件名
CONFIG_FILE_NAME = "config.toml"


class ConfigManager:
    """
    配置管理类
    
    提供配置文件的读写功能，用于持久化存储程序的配置信息。
    """
    
    def __init__(self):
        """
        初始化配置管理器
        
        计算配置文件的绝对路径，并加载现有配置。
        """
        # 配置文件位于当前脚本所在目录
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE_NAME)
        # 加载配置文件内容
        self.config = self._load_config()

    def _load_config(self):
        """
        加载配置文件
        
        如果配置文件存在，读取并解析 TOML 内容；否则返回空字典。
        
        Returns:
            dict: 配置信息字典
        """
        if os.path.exists(self.config_path):
            try:
                # 使用 toml 库解析配置文件
                return toml.load(self.config_path)
            except Exception:
                # 解析失败时返回空字典
                return {}
        return {}

    def _save_config(self):
        """
        保存配置文件
        
        将当前配置字典写入 TOML 文件。
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                # 使用 toml 库将字典写入文件
                toml.dump(self.config, f)
        except Exception:
            # 保存失败时静默处理
            pass

    def get_readelf_path(self):
        """
        获取 readelf 程序路径
        
        Returns:
            str: readelf 程序的绝对路径，如果未配置则返回空字符串
        """
        return self.config.get("readelf", {}).get("path", "")

    def set_readelf_path(self, path):
        """
        设置 readelf 程序路径
        
        将路径保存到配置字典，并持久化到文件。
        
        Args:
            path: readelf 程序的绝对路径
        """
        if "readelf" not in self.config:
            # 如果 readelf 配置项不存在，创建新的字典
            self.config["readelf"] = {}
        # 更新路径配置
        self.config["readelf"]["path"] = path
        # 保存到文件
        self._save_config()