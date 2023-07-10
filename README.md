# Example of CI/CD with saagieapi (Python)

## Description
This directory contains an example to use github action to deploy jobs inside Saagie Platform using
[saagieapi](https://saagieapi.readthedocs.io/en/latest/).

You can use the following actions to interact with Saagie platform: `package_job`, `update_job`, `run_job`, `update_pipeline`.
Packaging only available for python package code.

The `update_job` action depends on `package_job`, and the `run_job` action depends on `update_job` one.
If you want to package the artefact yourself, you have change the function `create_or_upgrade_job` in `utils.py`.

In this repository, we have 4 Python jobs and 2 Bash job.
For each python job, we have the source code inside `code`, and for the bash
job, we only have the job configuration file, for example: `/saagie/job/model_deployment.json`. In fact,
we don't need to create a zip for bash job.



## Prerequisite
### Global prerequisite

- You have an editor access to Saagie Platform
- You have to create at least one project in Saagie Platform (in the example, we have one in `dev`,
  another in `prod`)
- git clone this repo
- Change `project_id` value inside all json file at `/saagie/jobs/`
- Remove the value of `job_id` for all json file at `/saagie/jobs/`

### Local prerequisite

- Install Python and all libraries in `requirements.txt`
- To make it easier when launching command line, you can create the following environment variables:
  * SAAGIE_URL
  * SAAGIE_LOGIN
  * SAAGIE_PWD
  * SAAGIE_REALM

## How to use it in local

- To package a job, you can run the following command by replacing `your_job_name` by the  job that you want to package: `python __main__.py --action package --job_name your_job_name`
- To update a job,
  * For windows user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python __main__.py --action update_job --job_name your_job_name --saagie_url %SAAGIE_URL% --saagie_user %SAAGIE_LOGIN% --saagie_pwd %SAAGIE_PWD% --saagie_realm %SAAGIE_REALM% --saagie_env dev`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python __main__.py --action update_job --job_name your_job_name --saagie_url $SAAGIE_URL --saagie_user $SAAGIE_LOGIN --saagie_pwd $SAAGIE_PWD --saagie_realm $SAAGIE_REALM --saagie_env dev`

- To run a job, same thing as update, by using `--action run`,
  * For windows user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python __main__.py --action run_job --job_name your_job_name --saagie_url %SAAGIE_URL% --saagie_user %SAAGIE_LOGIN% --saagie_pwd %SAAGIE_PWD% --saagie_realm %SAAGIE_REALM% --saagie_env dev`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python __main__.py --action run_job --job_name your_job_name --saagie_url $SAAGIE_URL --saagie_user $SAAGIE_LOGIN --saagie_pwd $SAAGIE_PWD --saagie_realm $SAAGIE_REALM --saagie_env dev`

- To update a pipeline,
  * For windows user, use the following command line by replacing `your_pipeline_name` and `dev` if you want to use another environment:
    `python __main__.py --action update_pipeline --pipeline_name your_pipeline_name --saagie_url %SAAGIE_URL% --saagie_user %SAAGIE_LOGIN% --saagie_pwd %SAAGIE_PWD% --saagie_realm %SAAGIE_REALM% --saagie_env dev`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python __main__.py --action update_pipeline --pipeline_name your_pipeline_name --saagie_url $SAAGIE_URL --saagie_user $SAAGIE_LOGIN --saagie_pwd $SAAGIE_PWD --saagie_realm $SAAGIE_REALM --saagie_env dev`

- To run a pipeline,
  * For windows user, use the following command line by replacing `your_pipeline_name` and `dev` if you want to use another environment:
    `python __main__.py --action run_pipeline --pipeline_name your_pipeline_name --saagie_url %SAAGIE_URL% --saagie_user %SAAGIE_LOGIN% --saagie_pwd %SAAGIE_PWD% --saagie_realm %SAAGIE_REALM% --saagie_env dev`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python __main__.py --action run_pipeline --pipeline_name your_pipeline_name --saagie_url $SAAGIE_URL --saagie_user $SAAGIE_LOGIN --saagie_pwd $SAAGIE_PWD --saagie_realm $SAAGIE_REALM --saagie_env dev`


## Configuration

If you want to use the CI for your own jobs, make sure that the respect of the following file organisation.
In this repository, we have 2 directories:
- `code`:
  - each directories inside `code` is a job in Saagie
- `saagie`:
  - `jobs`:
    - each json file is a configuration file for a job, the name of the file should be the same
      as the name of job directory in `code`
  - `pipelines`:
    - each json file is a configuration file for a pipeline


### Job configuration file

Each json file inside `/saagie/jobs` has following schema:

#### Job

_A job inside Saagie_

Type: `object`

**_Properties_**

- **_env_** `required`
  - _Dict that contains all environment where you want to deploy job_
  - Type: `object`
- **_environment_name_** `required`
  - _Group all variables needed by each environment inside one dict_
  - Type: `object`
  - Example: ```"dev": {"platform_id": "your_platform_id", "project_id": "your_project_id", "job_id": ""}```
  - **_Properties_**:
    - **_platform_id_** `required`
      - _ID of Saagie platform_
      - Type: `string`
      - Example: `"1"`
    - **_project_id_** `required`
      - _ID of the Saagie project_
      - Type: `string`
      - Example: `"a0295a5b-40db-410e-994f-3096ff7c7398"`
    - **_job_id_**
      - _ID of the Saagie job_
      - Type: `string`
      - Example: `"a1f04f47-b317-43b4-b55d-ee6544b0a8ec"`
    - **_is_scheduled_**
      - _True if the job is scheduled, else False_
      - Type: `bool`
    - **_cron_scheduling_**
      - _Scheduling CRON format_
      - Type: `string`
    - **_schedule_timezone_**
      - _Timezone of the scheduling_
      - Type: `string`
    - **_resources_**
      - _CPU, memory limit and requests_
      - Type: `object`
      - **_Properties_**:
        - **_cpu_**
          - _CPU limit and request_
          - Type: `object`
          - **_Properties_**:
            - **_request_**
              - _CPU request_
              - Type: `double`
              - Example: `1`
            - **_limit_**
              - _CPU limit_
              - Type: `double`
              - Example: `1`
        - **_memory_**
          - _Memory limit and request_
          - Type: `object`
          - **_Properties_**:
            - **_request_**
              - _Memory request_
              - Type: `double`
              - Example: `1`
            - **_limit_**
              - _Memory limit_
              - Type: `double`
              - Example: `1`
    - **_emails_**
      - _Emails to receive alerts for the job, each item should be a valid email_
      - Type: `List[String]`
      - Example: `["test_user1@gmail.com", "test_user2@gmail.com"]`
    - **_status_list_**
      - _Receive an email when the job status change to a specific status. Each item of the list should be one of these following values: `REQUESTED`, `QUEUED`,
        `RUNNING`, `FAILED`, `KILLED`, `KILLING`, `SUCCEEDED`, `UNKNOWN`, `AWAITING`, `SKIPPED`_
      - Type: `List[String]`
      - Example:  `["FAILED", "KILLED", "UNKNOWN"]`


- **_job_name_** `required`
  - _Job name_
  - Type: `string`
  - Example: `Job extraction`
- **_file_path_** `required`
  - _File path of the code_
  - Type: `string`
  - Example: `./code/data_preparation`
- **_description_**
  - _Description for your job_
  - Type: `string`
  - Example: `This is my description`
- **_category_** `required`
  - _Category of the job_
  - Type: `string`
  - Must be `Extraction`, `Processing` or `Smart App`
- **_technology_** `required`
  - _Technology label of the job_
  - Type: `string`
  - Example: `Python`
- **_technology_catalog_** `required`
  - _Technology catalog containing the technology to use for this job_
  - Type: `string`
  - Example: `Saagie`
- **_runtime_version_** `required`
  - _Technology version of the job, the ID of the context_
  - Type: `string`
  - Example: `3.10`
- **_command_line_** `required`
  - _Command line of the job_
  - Type: `string`
  - Example: `python {file}`
- **_release_note_**
  - _Release note of the job_
  - Type: `string`
  - Example: `This is my release note`
- **_extra_technology_**
  - _Extra technology when needed (spark jobs). If not needed, leave to
    empty string or the request will not work_
  - Type: `string`
- **_extra_technology_version_**
  - _Version of the extra technology. Leave to empty string when not
    needed_
  - Type: `string`



#### Pipeline

_A pipeline inside Saagie_

Type: `object`

**_Properties_**

- **_env_** `required`
  - _Dict that contains all environment where you want to deploy job_
  - Type: `object`
- **_environment_name_** `required`
  - _Group all variables needed by each environment inside one dict_
  - Type: `object`
  - Example: ```"dev": {"platform_id": "your_platform_id", "project_id": "your_project_id", "graph_pipeline": {"job_nodes": [], "condition_nodes": []}}```
  - **_Properties_**:
    - **_platform_id_** `required`
      - _ID of Saagie platform_
      - Type: `string`
      - Example: `"1"`
    - **_project_id_** `required`
      - _ID of the Saagie project_
      - Type: `string`
      - Example: `"a0295a5b-40db-410e-994f-3096ff7c7398"`
    - **_is_scheduled_**
      - _True if the job is scheduled, else False_
      - Type: `bool`
    - **_cron_scheduling_**
      - _Scheduling CRON format_
      - Type: `string`
    - **_schedule_timezone_**
      - _Timezone of the scheduling_
      - Type: `string`
    - **_graph_pipeline_**
      - _Graph pipeline_
      - Type: `object`
      - **_Properties_**:
        - **_job_nodes_**
          - _List of job nodes_
          - Type: `object`
          - **_job_**:
            - **_Properties_**:
              - **_id_**
                - _An unique string to identify this job_
                - Type: `string`
                - Example: `my unique job 1`
              - **_job_name_**
                - _Name of the job_
                - Type: `string`
                - Example: `my awesome job 1`
              - **_job_id_**
                - _Job ID on Saagie's platform_
                - Type: `string`
                - Example: `6bb1b3b2-dd21-4d63-9661-ef2ad7308728`
              - **_next_nodes_**
                - _Next nodes of this job, each value in the list should be an ID of job or condition_
                - Type: `List[string]`
                - Example: `["my unique condition 1"]`
              - **_is_root_node_**
                - _Indicates whether the pipeline will start with this job_
                - Type: `bool`
                - Example: `True`
        - **_condition_nodes_**
          - _List of condition nodes_
          - Type: `object`
          - **_condition_**:
            - **_Properties_**:
              - **_id_**
                - _An unique string to identify this condition_
                - Type: `string`
                - Example: `my unique condition 1`
              - **_condition_type_**
                - _Type of the condition, should be `status` or `expression`_
                - Type: `string`
                - Example: `status`
              - **_value_**
                - _The value of the condition.If it's a condition on status, the value should be `AllSuccess` or `AllSuccessOrSkipped` or `AtLeastOneSuccess` .
                  If it's a condition on expression, make sure the value is a Common Expression Language (CEL) expression_
                - Type: `string`
                - Example: `AllSuccessOrSkipped`
              - **_next_nodes_success_**
                - _Next nodes of this job, each value in the list should be an ID of job or condition_
                - Type: `List[string]`
                - Example: `["my awesome job 2"]`
              - **_next_nodes_failure_**
                - _Indicates whether the pipeline will start with this job_
                - Type: `List[string]`
                - Example: `["My error handler job"]`
    - **_emails_**
      - _Emails to receive alerts for the job, each item should be a valid email_
      - Type: `List[String]`
      - Example: `["test_user1@gmail.com", "test_user2@gmail.com"]`
    - **_status_list_**
      - _Receive an email when the job status change to a specific status. Each item of the list should be one of these following values: `REQUESTED`, `QUEUED`,
        `RUNNING`, `FAILED`, `KILLED`, `KILLING`, `SUCCEEDED`, `UNKNOWN`, `AWAITING`, `SKIPPED`_
      - Type: `List[String]`
      - Example:  `["FAILED", "KILLED", "UNKNOWN"]`
    - **_has_execution_variables_enabled_**
      - _Whether to activate the execution variables
      - Type: `bool`
      - Example:  `True`

- **_description_**
  - _Description for your job_
  - Type: `string`
  - Example: `This is my description`
- **_release_note_**
  - _Release note of the job_
  - Type: `string`
  - Example: `This is my release note`
