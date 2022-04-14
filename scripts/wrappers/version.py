#!/usr/bin/env python3

import click
from typing import List, Union, Dict


ALL_COMPONENTS = [
    "kubernetes",
    "etcd",
    "dqlite",
    "microk8s",
]


VersionData = Union[str, Dict[str, str]]


def get_versions(components: List[str]) -> Dict[str, VersionData]:
    versions = {}
    for component in components:
        version_data = get_component_version(component)
        versions[component] = version_data
    return versions


def get_component_version(component: str) -> VersionData:
    version_handlers = {
        "kubernetes": get_kubernetes_version,
        "etcd": get_etcd_version,
        "dqlite": get_dqlite_version,
        "microk8s": get_microk8s_version,
    }
    handler = version_handlers[component]
    return handler()


def get_kubernetes_version():
    # try:
    #     result = run("kubectl", "version", "-o", "json", die=False)
    # except Exception:
    # import pdb; pdb.set_trace()
    # pass
    return "1.24"


def get_etcd_version():
    # TODO
    return {"version": "3.3.4", "hash": "fewgepw"}


def get_dqlite_version():
    # TODO
    return {"version": "0.0.1", "revision": "foobar"}


def get_microk8s_version():
    # TODO
    return {"version": "1.24", "channel": "stable"}


def print_versions(versions: Dict[str, VersionData]) -> None:
    print("MicroK8s components versions:")
    for component, version_data in versions.items():
        if isinstance(version_data, str):
            print(f"  - {component.capitalize()}: {version_data}")
        else:
            print(f"  - {component.capitalize()}:")
            for key, value in version_data.items():
                print(f"      {key.capitalize()}: {value}")


class UnknownComponentError(Exception):
    def __init__(self, component: str):
        self.component = component


def check_components_are_known(components: List[str]) -> None:
    for component in components:
        if component not in ALL_COMPONENTS:
            raise UnknownComponentError(component)


@click.command(
    context_settings={
        "ignore_unknown_options": True,
        "help_option_names": ["-h", "--help"],
    }
)
@click.argument("components", nargs=-1, required=False)
def versions_command(components: List[str]):
    """
    Shows version information for MicroK8s and its main components.
    """
    if len(components) == 0:
        # Default to print versions for all components
        components = ALL_COMPONENTS

    try:
        check_components_are_known(components)
    except UnknownComponentError as err:
        print(f"Unknown component {err.component}")
        exit(1)

    versions = get_versions(components)
    print_versions(versions)


if __name__ == "__main__":
    versions_command(prog_name="microk8s version")
