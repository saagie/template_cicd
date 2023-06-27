import logging
from saagieapi import SaagieApi, GraphPipeline, ConditionNode, JobNode, ConditionStatusNode, ConditionExpressionNode
import json
import shutil


def package_code(name_file, root_dir, archive_format="zip"):
    """
    Create a zip archive of a directory
    :param name_file: string, name of the file to create, including the path, minus any format-specific extension
    :param root_dir: string, a directory that will be the root directory of the archive
    :param archive_format: string, archive format, can be "zip", "tar", "gztar", "bztar" or "bztar"
    :return: string, name of the archive
    """
    if root_dir:
        return shutil.make_archive(name_file, archive_format, root_dir)
    else:
        return None


def connect_to_saagie(url, id_platform, user, password, realm):
    """
    Create an instance of SaagieAPI in order to interact with Saagie
    :param url: string, Saagie URL
    :param id_platform: string, Saagie ID platform
    :param user: string, Saagie's user
    :param password: string, Saagie user's password
    :param realm: string, Saagie realm
    :return: instance of SaagieAPI
    """
    saagie_client = SaagieApi(url_saagie=url,
                              id_platform=id_platform,
                              user=user,
                              password=password,
                              realm=realm)

    return saagie_client


def create_or_upgrade_job(client_saagie, job_config_file, env):
    """
    Package code and then create or upgrade a job on Saagie
    :param client_saagie: SaagieAPI, an instance of SaagieAPI
    :param job_config_file: str, job config file path
    :param env: str, environment of Saagie that you want to create or upgrade job
    :return: dict, dict of job informaiton
    """
    with open(job_config_file, "r") as f:
        job_config = json.load(f)

    output_zip = package_code(f"./dist/{job_config['job_name']}", job_config["file_path"])

    # var
    job_name = job_config["job_name"]
    project_id = job_config["env"][env]["project_id"]
    description = job_config["description"] if job_config["description"] else ""
    category = job_config["category"]
    technology = job_config["technology"]
    technology_catalog = job_config["technology_catalog"]
    runtime_version = job_config["runtime_version"]
    command_line = job_config["command_line"]
    release_note = job_config["release_note"] if job_config["release_note"] else ""
    extra_technology = job_config["extra_technology"] if job_config["extra_technology"] else ""
    extra_technology_version = job_config["extra_technology_version"] if job_config["extra_technology_version"] else ""
    is_scheduled = job_config["extra_technology_version"] if job_config["extra_technology_version"] else False
    cron_scheduling = job_config["cron_scheduling"] if job_config["cron_scheduling"] else None
    schedule_timezone = job_config["schedule_timezone"] if job_config["schedule_timezone"] else "UTC"
    resources = job_config["resources"] if job_config["resources"] else None
    emails = job_config["emails"] if job_config["emails"] else None
    status_list = job_config["status_list"] if job_config["status_list"] else None

    # check if job exists
    job_list = client_saagie.jobs.list_for_project_minimal(job_config["env"][env]["project_id"])["jobs"]
    job_names = [job["name"] for job in job_list]
    if job_name in job_names:
        job_id = [job["id"] for job in job_list if job["name"] == job_name][0]

        res = {"addJobVersion": client_saagie.jobs.upgrade(
            job_id=job_id,
            file=output_zip,
            runtime_version=runtime_version,
            command_line=command_line,
            release_note=release_note,
            extra_technology=extra_technology,
            extra_technology_version=extra_technology_version,
        )["data"]["addJobVersion"],
               "editJob": client_saagie.jobs.edit(
                   job_id=job_id,
                   job_name=job_name,
                   description=description,
                   is_scheduled=is_scheduled,
                   cron_scheduling=cron_scheduling,
                   schedule_timezone=schedule_timezone,
                   resources=resources,
                   emails=emails,
                   status_list=status_list,
               )["editJob"]}

    else:
        res = client_saagie.jobs.create(
            job_name=job_name,
            project_id=project_id,
            file=output_zip,
            description=description,
            category=category,
            technology=technology,
            technology_catalog=technology_catalog,
            runtime_version=runtime_version,
            command_line=command_line,
            release_note=release_note,
            extra_technology=extra_technology,
            extra_technology_version=extra_technology_version,
            cron_scheduling=cron_scheduling,
            schedule_timezone=schedule_timezone,
            resources=resources,
            emails=emails,
            status_list=status_list
        )
        print("Add job ID in the configuration file")
        job_config["env"][env]["job_id"] = res["data"]["createJob"]["id"]
        with open(job_config_file, "w") as f:
            json.dump(job_config, f, indent=4)
    return res


def run_job(client_saagie, job_config_file, env):
    """
    Package code, then create or upgrade a job on Saagie, and finally run it
    :param client_saagie: SaagieAPI, an instance of SaagieAP
    :param job_config_file: str, job config file path
    :param env: str, environment of Saagie that you want to create or upgrade job
    :return: dict, dict of job instance ID and status
    """
    create_or_upgrade_job(client_saagie, job_config_file, env)
    with open(job_config_file, "r") as f:
        job_config = json.load(f)
    return client_saagie.jobs.run(job_config["env"][env]["job_id"])


def create_graph_pipeline(pipeline_config_file, env):
    with open(pipeline_config_file, "r") as f:
        pipeline_config = json.load(f)
    pipeline_info = pipeline_config["env"][env]["graph_pipeline"]
    has_next_nodes = set()
    job_nodes = {}
    condition_nodes = {}
    graph_pipeline = GraphPipeline()

    # Find all job nodes
    for i in range(len(pipeline_info["job_nodes"])):
        job_node_info = pipeline_info["job_nodes"][i]
        job_id = job_node_info["job_id"]
        job_nodes[job_id]["node"] = JobNode(job_id)
        if job_node_info["is_root_node"]:
            graph_pipeline.add_root_node(job_nodes[job_id]["node"])
        if job_node_info["next_nodes"]:
            job_nodes[job_id]["next_nodes_ids"] = job_node_info["next_nodes"]
            has_next_nodes.add(job_id)

    # Find all condition nodes
    for i in range(len(pipeline_info["condition_nodes"])):
        condition_node_info = pipeline_info["condition_nodes"][i]
        condition_id = condition_node_info["condition_id"]
        condition_nodes[condition_id] = {}
        if condition_node_info["condition_type"] == "status":
            condition_nodes[condition_id]["node"] = ConditionStatusNode()
            if condition_node_info["value"].upper() == "ALLSUCCESS":
                condition_nodes[condition_id]["node"].put_all_success()
            if condition_node_info["value"].upper() == "ALLSUCCESSORSKIPPED":
                condition_nodes[condition_id]["node"].put_all_success_or_skipped()
            if condition_node_info["value"].upper() == "ATLEASTONESUCCESS":
                condition_nodes[condition_id]["node"].put_at_least_one_success()
        elif condition_node_info["condition_type"] == "expression":
            condition_nodes[condition_id]["node"] = ConditionExpressionNode()
            if condition_node_info["value"]:
                condition_nodes[condition_id]["node"].set_expression(condition_node_info["value"])
        else:
            condition_nodes[condition_id]["node"] = ConditionNode()
        if condition_node_info["next_nodes_success"]:
            condition_nodes[condition_id]["next_nodes_success_ids"] = condition_node_info["next_nodes_success"]
            has_next_nodes.add(condition_id)
        if condition_node_info["next_nodes_failure"]:
            condition_nodes[condition_id]["next_nodes_failure"] = condition_node_info["next_nodes_failure"]
            has_next_nodes.add(condition_id)

    # Add next nodes
    for node_id in has_next_nodes:
        if node_id in job_nodes.keys():
            job_node_tmp = job_nodes[node_id]["node"]
            for next_node in job_nodes[node_id]["next_nodes_ids"]:
                if next_node in job_nodes.keys():
                    job_node_tmp.add_next_node(job_nodes[next_node]["node"])
                if next_node in condition_nodes.keys():
                    job_node_tmp.add_next_node(condition_nodes[next_node]["node"])
        if node_id in condition_nodes.keys():
            condition_node_tmp = condition_nodes[node_id]["node"]
            if condition_nodes[node_id]["next_nodes_success_ids"]:
                for next_node in condition_nodes[node_id]["next_nodes_success_ids"]:
                    if next_node in job_nodes.keys():
                        condition_node_tmp.add_success_node(job_nodes[next_node]["node"])
                    if next_node in condition_nodes.keys():
                        condition_node_tmp.add_success_node(condition_nodes[next_node]["node"])
                for next_node in condition_nodes[node_id]["next_nodes_failure"]:
                    if next_node in job_nodes.keys():
                        condition_node_tmp.add_failure_node(job_nodes[next_node]["node"])
                    if next_node in condition_nodes.keys():
                        condition_node_tmp.add_failure_node(condition_nodes[next_node]["node"])

    return graph_pipeline


def get_pipeline_id(client_saagie, pipeline_config_file, env):
    """WIP"""
    with open(pipeline_config_file, "r") as f:
        pipeline_config = json.load(f)





    res = client_saagie.pipelines.create_or_upgrade(
        name=pipeline_config["pipeline_name"],
        project_id=pipeline_config["env"][env]["project_id"],
        description=job_config["description"] if job_config["description"] else "",
        category=job_config["category"],
        technology=job_config["technology"],
        technology_catalog=job_config["technology_catalog"],
        runtime_version=job_config["runtime_version"],
        command_line=job_config["command_line"],
        release_note=job_config["release_note"] if job_config["release_note"] else "",
        extra_technology=job_config["extra_technology"] if job_config["extra_technology"] else "",
        extra_technology_version=job_config["extra_technology_version"] if job_config[
            "extra_technology_version"] else "",
        is_scheduled=job_config["extra_technology_version"] if job_config["extra_technology_version"] else False,
        cron_scheduling=job_config["cron_scheduling"] if job_config["cron_scheduling"] else None,
        schedule_timezone=job_config["schedule_timezone"] if job_config["schedule_timezone"] else "UTC",
        resources=job_config["resources"] if job_config["resources"] else None,
        emails=job_config["emails"] if job_config["emails"] else None,
        status_list=job_config["status_list"] if job_config["status_list"] else None
    )
    if "data" in res.keys():
        job_config["env"][env]["job_id"] = res["data"]["createJob"]["id"]
        with open(job_config_file, "w") as f:
            json.dump(job_config, f, indent=4)
    return res
