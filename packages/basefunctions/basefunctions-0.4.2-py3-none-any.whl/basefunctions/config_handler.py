"""
=============================================================================

  Licensed Materials, Property of Ralph Vogl, Munich

  Project : backtraderfunctions

  Copyright (c) by Ralph Vogl

  All rights reserved.

  Description:

  a simple helper package for backtrader indicators and strategies

=============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
from typing import Dict
import basefunctions
import os
import toml

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------
DEFAULT_PATHNAME = ".config"

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# CLASS DEFINITIONS
# -------------------------------------------------------------
class ConfigHandler(metaclass=basefunctions.SingletonMeta):
    """
    The ConfigHandler class is a class to handle and abstract the configuration
    handling. The ConfigHandler class is a singleton class, means there is only
    one instance of this class.
    The ConfigHandler creates a .config directory in your home directory and
    stores configurations in this directory which then can be accessed by the
    individual users of the class. The configurations are stored in a toml file
    format and are stored by with the packagename as the filename.
    """

    configs = {}

    def load_configuration(self, package_name: str) -> None:
        """
        The load_configuration method loads the configuration from the .config
        directory in the home directory. The configuration is stored in a toml
        file format and is stored by with the packagename as the filename.
        """
        if not package_name:
            return
        # Load the configuration from the .config directory
        config_filename = self.get_config_filename(package_name)
        if basefunctions.check_if_file_exists(config_filename):
            self.configs.update({package_name: toml.load(config_filename)})
        else:
            raise FileNotFoundError(f"config file {config_filename} not found")

    def save_configuration(self, package_name: str) -> None:
        """
        The save_configuration method saves the configuration to the .config
        directory in the home directory. The configuration is stored in a toml
        file format and is stored by with the packagename as the filename.
        """
        if package_name not in self.configs:
            raise ValueError(f"package {package_name} not in configs")

        config_filename = self.get_config_filename(package_name)
        if not basefunctions.check_if_dir_exists(basefunctions.get_path_name(config_filename)):
            print("create directory", basefunctions.get_path_name(config_filename))
            basefunctions.create_directory(basefunctions.get_path_name(config_filename))
        with open(config_filename, "w") as config_file:
            toml.dump(self.configs.get(package_name), config_file)

    def get_configurations(self, package_name: str, auto_load: bool = True) -> Dict | None:
        """
        The get_configurations method returns the configurations as a dictionary
        """
        if package_name not in self.configs and auto_load:
            self.load_configuration(package_name)
        return self.configs.get(package_name, None)

    def get_configuration(
        self, package_name: str, config_name: str, auto_load: bool = True
    ) -> Dict | None:
        """
        The get_configuration method returns the configuration as a dictionary
        """
        if package_name not in self.configs and auto_load:
            self.load_configuration(package_name)
        return self.configs.get(package_name, {}).get(config_name, None)

    def get_config_filename(self, package_name: str) -> str:
        """
        The get_config_filename method returns the configuration filename
        """
        return os.path.sep.join(
            [
                basefunctions.get_home_path(),
                DEFAULT_PATHNAME,
                f"{package_name}",
                f"{package_name}.toml",
            ]
        )

    def add_configuration(
        self, package_name: str, config_name: str, config: Dict, permanent_flag: bool = True
    ) -> None:
        """
        The add_configuration method adds a configuration to the configuration
        dictionary
        """
        if package_name not in self.configs:
            self.configs.update({package_name: {}})
        self.configs[package_name].update({config_name: config})
        if permanent_flag:
            self.save_configuration(package_name)
