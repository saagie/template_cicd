import argparse
import logging
import json
import utils


def main():
    # Retrieving arguments
    parser = argparse.ArgumentParser(description='Continous integration in Saagie Project')
    parser.add_argument("--action", type=str, choices=['package_job', 'update_job', 'run_job', 'update_pipeline',
                                                       'run_pipeline'],
                        help="Action to do with job: 'package_job', 'update_job', 'run_job', 'update_pipeline', "
                             "'run_pipeline'",
                        required=True)
    parser.add_argument("--job_name", type=str,
                        help="Name of the job", required=False)
    parser.add_argument("--pipeline_name", type=str,
                        help="Name of the pipeline", required=False)
    parser.add_argument("--saagie_url", type=str,
                        help="URL of Saagie Platform", required=False)
    parser.add_argument("--saagie_user", type=str,
                        help="Saagie user", required=False)
    parser.add_argument("--saagie_pwd", type=str,
                        help="Saagie user's password", required=False)
    parser.add_argument("--saagie_realm", type=str,
                        help="Saagie_realm", required=False)
    parser.add_argument("--saagie_env", type=str,
                        help="Saagie environment", required=False, default="dev")

    args = parser.parse_args()
    if "job" in args.action:
        with open(f"saagie/jobs/{args.job_name}.json", "r") as f:
            job_config = json.load(f)

    if args.action == "package_job":
        utils.package_code(f"./dist/{job_config['job_name']}", job_config["file_path"])
        logging.info(f"Successfully package job: [{args.job_name}]")

    if args.action == "update_job":
        client_saagie = utils.connect_to_saagie(args.saagie_url,
                                                job_config["env"][args.saagie_env]["platform_id"],
                                                args.saagie_user,
                                                args.saagie_pwd,
                                                args.saagie_realm)
        utils.create_or_upgrade_job(client_saagie, f"saagie/jobs/{args.job_name}.json", args.saagie_env)

    if args.action == "run_job":
        client_saagie = utils.connect_to_saagie(args.saagie_url,
                                                job_config["env"][args.saagie_env]["platform_id"],
                                                args.saagie_user,
                                                args.saagie_pwd,
                                                args.saagie_realm)
        utils.run_job(client_saagie, f"saagie/jobs/{args.job_name}.json", args.saagie_env)

    if args.action == "update_pipeline":
        with open(f"saagie/pipelines/{args.pipeline_name}.json", "r") as f:
            pipeline_config = json.load(f)
        client_saagie = utils.connect_to_saagie(args.saagie_url,
                                                pipeline_config["env"][args.saagie_env]["platform_id"],
                                                args.saagie_user,
                                                args.saagie_pwd,
                                                args.saagie_realm)
        utils.create_or_upgrade_graph_pipeline(client_saagie,
                                               f"saagie/pipelines/{args.pipeline_name}.json",
                                               args.saagie_env)
    if args.action == "run_pipeline":
        with open(f"saagie/pipelines/{args.pipeline_name}.json", "r") as f:
            pipeline_config = json.load(f)
        client_saagie = utils.connect_to_saagie(args.saagie_url,
                                                pipeline_config["env"][args.saagie_env]["platform_id"],
                                                args.saagie_user,
                                                args.saagie_pwd,
                                                args.saagie_realm)
        utils.run_pipeline(client_saagie,
                           f"saagie/pipelines/{args.pipeline_name}.json",
                           args.saagie_env)

    logging.info("DONE")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    main()
