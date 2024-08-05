import re
from .shell import run


def list_local_docker_images():
    """Get the mirror list of the local mirror registry."""
    out = run("docker images")
    images = []
    lines = out.split("\n")
    for line in lines[1:]:
        m = re.match(r"^(\S+)\s+(\S+)\s+(\S+)\s+(.+?)\s+(\S+)$", line)
        repo = m.group(1)
        tag = m.group(2)
        image = f"{repo}:{tag}"
        images.append({"image": image})
    return images
