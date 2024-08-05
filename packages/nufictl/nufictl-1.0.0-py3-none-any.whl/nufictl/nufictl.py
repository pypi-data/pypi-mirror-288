import fire
import requests
import json
import yaml
import random
import string
from tabulate import tabulate
from nufictl.model import NpuDeploy, DeployDetail
from nufictl.config_manager import ConfigManager

# https://gitlab.com/dudaji/ai-chip/aichip/-/merge_requests/229
CONFIG_FILE = "config.yaml"


class NufiCtl:
    """NufiCTL is a command-line tool for managing CRD Npu Deployments.

    Usage:
        nufictl ls
        nufictl create with sequential user input
        nufictl run --image=IMAGE [--cpu=CPU] [--memory=MEMORY] [--accelerator_type=TYPE] [--accelerator_count=COUNT]
        nufictl delete --name=NAME
        nufictl config set URL
        nufictl config ls
        nufictl config delete NAME_or_URL
        nufictl config set current-context NAME_or_URL
        nufictl config get current-context
    """

    def __init__(self):
        self.config_manager = ConfigManager()
        self.base_url = self.config_manager.config_data.get(
            self.config_manager.current_context,
            self.config_manager.config_data["default"],
        )

    def config(self, action=None, name=None, value=None):
        """
        Manage configuration for NufiCTL.

        Available actions:
            set: Set a new URL configuration.
            ls: List all configurations.
            delete: Delete a configuration by name or URL.
            set_current_context: Set the current context by name or URL.
            get_current_context: Get the current context.

        Usage:
            nufictl config set URL
            nufictl config ls
            nufictl config delete NAME_or_URL
            nufictl config set-current-context NAME_or_URL
            nufictl config get-current-context
        """
        if action is None:
            print(self.config.__doc__)
        elif action == "set":
            self.config_manager.set(name, value)
        elif action == "ls":
            self.config_manager.ls()
        elif action == "delete":
            self.config_manager.delete(value)
        elif action == "set-current-context":
            self.config_manager.set_current_context(value)
        elif action == "get-current-context":
            self.config_manager.get_current_context()
        else:
            print(
                "Unknown action. Available actions are: set, ls, delete, set_current_context, get_current_context."
            )

    @staticmethod
    def generate_random_name(length=8):
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def test(self, deployment_name):
        """Test the created NPU deployment.

        Usage:
            nufictl test DEPLOYMENT_NAME
        """
        test_url = f"https://{deployment_name}.dudaji.com:4443"
        try:
            response = requests.get(test_url)
            if response.status_code == 200:
                print(
                    f"Test successful for {test_url}. Response: {response.status_code}"
                )
            else:
                print(
                    f"Test failed for {test_url}. Status code: {response.status_code}"
                )
        except requests.RequestException as e:
            print(f"Test failed for {test_url}. Error: {str(e)}")

    def ls(self):
        """List all deployments"""
        response = requests.get(self.base_url)
        data = response.json()

        items = data.get("items", [])
        # print(items)  # 디버깅을 위해 추가

        deploys = []
        for item in items:
            name = item["metadata"]["name"]
            namespace = item["metadata"]["namespace"]
            creation_timestamp = item["metadata"]["creationTimestamp"]
            replicas = item["spec"]["replicas"]
            image = item["spec"]["image"]
            cpu = item["spec"]["resources"]["limits"]["cpu"]
            memory = item["spec"]["resources"]["limits"]["memory"]

            deploy = DeployDetail(
                name, namespace, image, cpu, memory, creation_timestamp, replicas
            )
            deploys.append(deploy)

        table = [
            [
                deploy.name,
                deploy.namespace,
                deploy.replicas,
                deploy.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                f"https://{deploy.name}.dudaji.com:4443",
            ]
            for deploy in deploys
        ]
        headers = ["Name", "Namespace", "Replicas", "Created", "Endpoint URL"]
        print(tabulate(table, headers, tablefmt="pretty"))

    # def get(self, name):
    #     """Get details of a deployment"""
    #     url = f"{self.base_url}/{name}"
    #     response = requests.get(url)
    #     data = response.json()

    #     name = data["metadata"]["name"]
    #     image = data["spec"]["image"]
    #     cpu = data["spec"]["resources"]["limits"]["cpu"]
    #     memory = data["spec"]["resources"]["limits"]["memory"]
    #     replicas = data["spec"]["replicas"]
    #     creation_timestamp = data["metadata"]["creationTimestamp"]

    #     deploy_detail = DeployDetail(
    #         name, image, cpu, memory, replicas, creation_timestamp
    #     )
    #     print(deploy_detail)
    #     return deploy_detail

    def create(
        self,
        name=None,
        image=None,
        cpu=None,
        memory=None,
        replicas=None,
        accelerator_type=None,
        accelerator_count=None,
    ):
        # Sequential user input with default values
        """Create a new deployment interactively."""
        name = input(f"Name [npu-deploy-example]: ") or "npu-deploy-example"
        image = input(f"Image [nginx]: ") or "nginx"
        cpu = input(f"CPU [1]: ") or "1"
        memory = input(f"Memory [1]: ") or "1"
        replicas = input(f"Replicas [1]: ") or 1
        accelerator_type = input(f"Accelerator Type [npu]: ") or "npu"
        accelerator_count = input(f"Accelerator Count [1]: ") or 1

        payload = {
            "name": name,
            "image": image,
            "cpu": cpu,
            "memory": memory,
            "replicas": replicas,
        }
        if accelerator_type:
            payload["acceleratorType"] = accelerator_type
        if accelerator_count:
            payload["acceleratorCount"] = accelerator_count

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.base_url, headers=headers, data=json.dumps(payload)
        )
        response_data = response.json()
        message = ""
        if response.status_code == 200:
            if (
                "response" in response_data
                and response_data["response"].get("statusCode") == 409
            ):
                message = (
                    f"Failed to create deployment. Deployment {name} already exists."
                )
            else:
                name = payload.get("name", "Unknown")
                image = payload.get("image", "Unknown")
                message = f"Successfully created {name} with image: {image}"
        else:
            message = (
                f"Failed to create deployment. Status code: {response.status_code}, "
                f"Error: {response_data.get('message', 'No error message')}"
            )
        # print(message)
        return message

    def run(
        self,
        image,
        cpu="1",
        memory="1",
        accelerator_type="npu",
        accelerator_count=1,
    ):
        """Run a new deployment with a random name"""
        name = f"npu-deploy-{image}-{self.generate_random_name()}"
        payload = {"name": name, "image": image, "cpu": cpu, "memory": memory}
        if accelerator_type:
            payload["acceleratorType"] = accelerator_type
        if accelerator_count:
            payload["acceleratorCount"] = accelerator_count

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.base_url, headers=headers, data=json.dumps(payload)
        )
        message = ""
        if response.status_code == 200:
            name = payload.get("name", "Unknown")
            image = payload.get("image", "Unknown")
            message = f"Successfully created {name} with image: {image}"
        return message

    def delete(self, name):
        """Delete a deployment.
        Args:
            --name: Name of the deployment to delete.
        """
        params = {"name": name}
        response = requests.delete(self.base_url, params=params)
        message = ""
        if response.status_code == 200:
            message = f"Successfully deleted {name}"
        return message


def main():
    fire.Fire(NufiCtl)


if __name__ == "__main__":
    main()
