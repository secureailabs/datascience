from typing import Dict
from uuid import uuid4


class ResearcherSession:
    username: str
    jwt: str
    ip: str
    # Dict of federation name to information about the cluster (id, ip)
    provision_clusters: Dict

    def get_federation_connect_string(self, federation_name: str):
        if federation_name in self.provision_clusters:
            return f'http://{self.provision_clusters[federation_name]["cluster_ip"]}:{self.provision_clusters[federation_name]["cluster_port"]}'
        raise Exception(f"Federation {federation_name} not found")
