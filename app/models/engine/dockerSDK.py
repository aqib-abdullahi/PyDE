#!/usr/bin/env python3
"""docker connection engine
"""
import docker
import docker
import os
from dotenv import load_dotenv
import tarfile
import time
from io import BytesIO


load_dotenv()
ip_address = os.getenv('IP_ADDRESS')
container_port = os.getenv('CONTAINER_PORT')

class dockerSDK():
    """docker container interaction engine
    """
    def __init__(self):
        """initializes with a connection"""
        self.remote_docker_client = docker.DockerClient(
            base_url =f"tcp://{ip_address}:{container_port}"
        )
    
    def get_container_by_id(self, container_id):
        """gets the docker container object using 
        container ID
        """
        return self.remote_docker_client.containers.get(container_id)
    
    def spawn_container(self, Container):
        """creates a docker container
        returns container ID
        """
        container_id = self.remote_docker_client.containers.run('python-container',
                                                command="/bin/bash",
                                                name=Container,
                                                stdin_open=True,
                                                tty=True,
                                                detach=True)
        # PATH CONFIG
        symlink = container_id.exec_run("ln -s /usr/bin/python3 /usr/bin/python")
        return container_id
    
    def upload_file(self, container_id, file_content, file_name):
        """Uploads file to container"""
        containerID = self.get_container_by_id(container_id)
        work_dir = "/PyDE"
        pw_tarstream = BytesIO()
        pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')
        if file_content is not None:
            file_content += "\n"
            file_data = file_content.encode('utf8')
            tarinfo = tarfile.TarInfo(name=file_name)
            tarinfo.size = len(file_data)
            tarinfo.mtime = time.time()
            pw_tar.addfile(tarinfo, BytesIO(file_data))
            pw_tar.close()
            pw_tarstream.seek(0)
            result = containerID.put_archive(path=work_dir, data=pw_tarstream)
            return result
        else:
            file_content = "\n"
            file_data = file_content.encode('utf8')
            tarinfo = tarfile.TarInfo(name=file_name)
            tarinfo.size = len(file_data)
            tarinfo.mtime = time.time()
            pw_tar.addfile(tarinfo, BytesIO(file_data))
            pw_tar.close()
            pw_tarstream.seek(0)
            result = containerID.put_archive(path=work_dir, data=pw_tarstream)
            return result

    
    def download_file(self, container_id, file_name):
        """downloads file from container
        """
        containerID = self.get_container_by_id(container_id)
        result = containerID.exec_run(f'cat {file_name}')
        return(result.output.decode('utf-8'))
    
    def execute_file(self, container_id, file_name):
        """executes the file within container
        """
        containerID = self.get_container_by_id(container_id)
        permission = containerID.exec_run(f'chmod 755 {file_name}')
        execute = containerID.exec_run(f'./{file_name}')
        return(execute.output.decode('utf-8'))