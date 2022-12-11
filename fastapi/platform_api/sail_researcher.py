import uuid

import requests

from sail_session import ResearcherSession

PORT = 8000


def login(user_name: str, password: str, ip: str) -> ResearcherSession:

    login_endpoint = f"https://{ip}:{PORT}/login"
    login_body = {"username": user_name, "password": password}
    login_request = requests.post(login_endpoint, login_body, verify=False)

    new_session = ResearcherSession()

    if login_request.status_code == 200:
        new_session.jwt = login_request.json()["access_token"]
        new_session.username = user_name
        new_session.ip = ip
        new_session.provision_clusters = dict()
    else:
        raise Exception("Failed to login")

    return new_session


def get_federations(session: ResearcherSession):

    assert session.jwt is not None

    federation_endpoint = f"https://{session.ip}:{PORT}/data-federations"
    request_headers = {"Authorization": f"Bearer {session.jwt}"}
    federation_request = requests.get(federation_endpoint, verify=False, headers=request_headers)

    if federation_request.status_code != 200:
        raise Exception("Failed to retrieve federations")

    return federation_request.json()["data_federations"]


def provision_federation_by_name(session: ResearcherSession, federation_name: str):

    federations = get_federations(session)

    federation_id = [federation["id"] for federation in federations if federation["name"] == federation_name]

    if len(federation_id) != 1:
        raise Exception("Failed to find federation {federation_name}")

    print(f"Id for federation is {federation_id[0]}")

    # Now that we have the ID call the API to start our provision operation
    # For now we just store a temporary identifier until we can really connect to Azure

    endpoint = f"https://{session.ip}:{PORT}/data-federations-provisions"
    request_body = {"data_federation_id": federation_id[0], "secure_computation_nodes_size": "Standard_D4s_v4"}
    request_headers = {"Authorization": f"Bearer {session.jwt}"}
    print(f"{request_body}")
    response = requests.post(endpoint, json=request_body, verify=False, headers=request_headers)

    if response.status_code != 201:
        raise Exception(f"Provision call failed: {response.status_code}")

    provision_id = response.json()["id"]
    session.provision_clusters[federation_name] = {}
    session.provision_clusters[federation_name]["provision_id"] = provision_id
    session.provision_clusters[federation_name]["broker_id"] = response.json()["smart_broker_id"]

    print(f"Provision id {provision_id}")
    print(f"Smart broker id: {response.json()['smart_broker_id']}")
    return provision_id


def connect_to_federation(session: ResearcherSession, federation_name: str):
    # Reach out to the API to get information about a provision
    broker_id = session.provision_clusters[federation_name]["broker_id"]

    endpoint = f"https://{session.ip}:{PORT}/secure-computation-node/{broker_id}"
    request_headers = {"Authorization": f"Bearer {session.jwt}"}
    response = requests.get(endpoint, verify=False, headers=request_headers)

    if response.status_code != 200:
        raise Exception(f"Failed to get status for federation {federation_name}")

    state = response.json()["state"]

    print(f"State is {state}")
    return_dict = None
    if state == "WAITING_FOR_DATA":
        # For now we assume we got a valid IP to a smart broker
        return_dict["ip"] = response.json()["ipaddress"]
        return_dict["port"] = 8000

    return return_dict


def connect_to_federation_by_id(session: ResearcherSession, broker_id: str):

    endpoint = f"https://{session.ip}:{PORT}/secure-computation-node/{broker_id}"
    request_headers = {"Authorization": f"Bearer {session.jwt}"}
    response = requests.get(endpoint, verify=False, headers=request_headers)

    if response.status_code != 200:
        raise Exception(f"Failed to get status for federation {broker_id}")

    state = response.json()["state"]

    print(f"State is {state}")
    return_dict = {}
    if state == "WAITING_FOR_DATA":
        # For now we assume we got a valid IP to a smart broker
        return_dict["ip"] = response.json()["ipaddress"]
        return_dict["port"] = 8000
    else:
        return_dict = None

    return return_dict


def deprovision_federation_by_name(session: ResearcherSession, federation_name: str):

    provision_id = session.provision_clusters[federation_name]["provision_id"]

    print(f"Deprovision ID is {provision_id}")

    # We no longer want access to this, the provision_id can still be used
    del session.provision_clusters[federation_name]

    # Now that we have the ID call the API to start the de-provision operation
    deprovision_federation_by_id(session, provision_id)


def deprovision_federation_by_id(session: ResearcherSession, federation_id: uuid):
    endpoint = f"https://{session.ip}:{PORT}/data-federations-provisions/{federation_id}"
    request_headers = {"Authorization": f"Bearer {session.jwt}"}

    print(f"Endpoint is {endpoint}")
    response = requests.delete(endpoint, verify=False, headers=request_headers)

    if response.status_code != 204:
        raise Exception(f"Failed to de-provision, status: {response.status_code}")


def federation_mean(session: ResearcherSession, federation_name: str):

    payload = {"series_uuid": "some identifier"}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/mean", params=payload)
    return result.json()["mean_sail"]


def federation_chi_square(session: ResearcherSession, federation_name: str, series_uuid_1: str, series_uuid_2: str):
    payload = {"series_uuid_1": series_uuid_1, "series_uuid_2": series_uuid_2}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/chisquare", params=payload)
    return result.json()["chisquare_sail"]


def federation_kolmogorov_smirnov_test(
    session: ResearcherSession, federation_name: str, series_uuid, type_distribution, type_ranking
):
    payload = {"series_uuid": series_uuid, "type_distribution": type_distribution, "type_ranking": type_ranking}
    result = requests.get(
        f"{session.get_federation_connect_string(federation_name)}/kolmogorovSmirnovTest", params=payload
    )
    return result.json()["k_statistic_sail"], result.json()["p_value_sail"]


def federation_kurtosis(session: ResearcherSession, federation_name: str, series_uuid):
    payload = {"series_uuid": series_uuid}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/kurtosis", params=payload)
    return result.json()["kurtosis_sail"]


def federation_levene_test(session: ResearcherSession, federation_name: str, series_uuid_1, series_uuid_2):
    payload = {"series_uuid_1": series_uuid_1, "series_uuid_2": series_uuid_2}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/leveneTest", params=payload)
    return result.json()["f_statistic_sail"], result.json()["p_value_sail"]


def federation_mann_whitney_utest(
    session: ResearcherSession, federation_name: str, series_uuid_1, series_uuid_2, alternative, type_ranking
):
    payload = {
        "series_uuid_1": series_uuid_1,
        "series_uuid_2": series_uuid_2,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/mannWhitneyUTest", params=payload)
    return result.json()["w_statistic_sail"], result.json()["p_value_sail"]


def federation_min_max(session: ResearcherSession, federation_name: str, series_uuid):
    payload = {"series_uuid": series_uuid}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/minMax", params=payload)
    return result.json()["min_sail"], result.json()["max_sail"]


def federation_paired_t_test(
    session: ResearcherSession, federation_name: str, series_uuid_1, series_uuid_2, alternative
):
    payload = {"series_uuid_1": series_uuid_1, "series_uuid_2": series_uuid_2, "alternative": alternative}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/pairedTTest", params=payload)
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def federation_pearson(session: ResearcherSession, federation_name: str, series_uuid_1, series_uuid_2, alternative):
    payload = {"series_uuid_1": series_uuid_1, "series_uuid_2": series_uuid_2, "alternative": alternative}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/pearson", params=payload)
    return result.json()["pearson_sail"], result.json()["p_value_sail"]


def federation_skewness(session: ResearcherSession, federation_name: str, series_uuid):
    payload = {"series_uuid": series_uuid}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/skewness", params=payload)
    return result.json()["skewness_sail"]


def federation_spearman(
    session: ResearcherSession, federation_name: str, series_uuid_1, series_uuid_2, alternative, type_ranking
):
    payload = {
        "series_uuid_1": series_uuid_1,
        "series_uuid_2": series_uuid_2,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/spearman", params=payload)
    return result.json()["spearman_sail"], result.json()["p_value_sail"]


def federation_student_ttest(
    session: ResearcherSession, federation_name: str, series_uuid_1, series_uuid_2, alternative
):
    payload = {"series_uuid_1": series_uuid_1, "series_uuid_2": series_uuid_2, "alternative": alternative}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/studentTTest", params=payload)
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def federation_variance(session: ResearcherSession, federation_name: str, series_uuid):
    payload = {"series_uuid": series_uuid}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/variance", params=payload)
    return result.json()["variance_sail"]


def federation_welch_t_test(
    session: ResearcherSession, federation_name: str, series_uuid_1, series_uuid_2, alternative
):
    payload = {"series_uuid_1": series_uuid_1, "series_uuid_2": series_uuid_2, "alternative": alternative}
    result = requests.get(f"{session.get_federation_connect_string(federation_name)}/welchTTest", params=payload)
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def federation_wilcoxon_signed_rank_test(
    session: ResearcherSession, federation_name: str, series_uuid_1, series_uuid_2, alternative, type_ranking
):
    payload = {
        "series_uuid_1": series_uuid_1,
        "series_uuid_2": series_uuid_2,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.get(
        f"{session.get_federation_connect_string(federation_name)}/wilcoxonSignedRankTest", params=payload
    )
    return result.json()["w_statistic_sail"], result.json()["p_value_sail"]
