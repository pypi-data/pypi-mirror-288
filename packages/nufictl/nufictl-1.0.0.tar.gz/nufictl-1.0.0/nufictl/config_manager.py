import yaml
import random
import string
import os
from tabulate import tabulate


CONFIG_FILE = "config.yaml"


class ConfigManager:
    def __init__(self):
        self.config_data = self.load_config()
        self.default_url = self.config_data.get("default")
        if self.default_url is None:
            raise ValueError("default_url is not set in config.yaml")
        self.current_context = self.config_data.get("current_context", "default")
        if "default" not in self.config_data:
            self.config_data["default"] = self.default_url
        self.save_config()

    @staticmethod
    def generate_random_name(length=8):
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def save_config(self):
        self.config_data["current_context"] = self.current_context
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(self.config_data, f, default_flow_style=False)

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            print(f"{CONFIG_FILE} not found. Creating a new one with default settings.")
            default_config = {"default": "", "current_context": "default"}
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
        else:
            with open(CONFIG_FILE, "r") as f:
                return yaml.safe_load(f)

    def set(self, name: None, url: None):
        # both name and url -> update
        if name and url:
            self.config_data[name] = url
            self.save_config()
            print(f"URL {url} has been set with name {name}.")
        # setup url with random name
        elif url:
            name = self.generate_random_name()
            self.config_data[name] = url
            self.save_config()
            print(f"URL {url} has been set with name {name}.")
        else:
            print("URL is required for setting configuration.")

    def ls(self):
        headers = ["Context", "Config Name", "URL"]
        table = [
            [
                "*" if self.current_context == "default" else "",
                "default",
                self.default_url,
            ]
        ]
        for name, url in self.config_data.items():
            if name in ["current_context", "default", "default"]:
                continue
            table.append(["*" if name == self.current_context else "", name, url])
        print(tabulate(table, headers, tablefmt="pretty"))

    def delete(self, name_or_url):
        if name_or_url:
            if name_or_url in ["default", "current_context"]:
                print(f"Cannot delete reserved context: {name_or_url}")
                return
            # Check if it's a URL
            if name_or_url in self.config_data.values():
                for name in list(self.config_data.keys()):
                    if self.config_data[name] == name_or_url:
                        del self.config_data[name]
                        self.save_config()
                        print(f"Configuration with URL {name_or_url} has been deleted.")
                        return
            # Check if it's a name
            elif name_or_url in self.config_data:
                del self.config_data[name_or_url]
                self.save_config()
                print(f"Configuration {name_or_url} has been deleted.")
            else:
                print("Configuration name or URL must exist.")
        else:
            print("Configuration name or URL is required for deletion.")

    def set_current_context(self, name_or_url):
        if (
            name_or_url == "default"
            or name_or_url in self.config_data.keys()
            or name_or_url in self.config_data.values()
        ):
            if name_or_url == "default":
                self.current_context = "default"
            else:
                for name, url in self.config_data.items():
                    if name_or_url == name or name_or_url == url:
                        self.current_context = name
                        break
            self.save_config()
            print(f"Current context set to {name_or_url}")
        else:
            print("Configuration name or URL must exist.")

    def get_current_context(self):
        context_url = self.config_data.get(self.current_context, self.default_url)
        print(f"Current context: {self.current_context} ({context_url})")
