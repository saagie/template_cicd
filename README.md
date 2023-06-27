# Example of CI/CD with saagieapi (Python)

## Description 
This directory contains an example to use github action to deploy jobs inside Saagie Platform using
[saagieapi](https://saagieapi.readthedocs.io/en/latest/).

You can `package`, `update` or `run` your Saagie job with this project.
Packaging only available for python package code.

The `update` action depends on `package`, and the `run` action depends on `update` one.
If you want to package the artefact yourself, you have change the function `create_or_upgrade_job` in `utils.py`.

In this repository, we have 4 Python jobs and 1 Bash job.
For each python job, we have the source code inside `code`, and for the bash
job, we only have the job configuration file: `/saagie/job/model_deployment.json`.



## Prerequisite
### Global prerequisite

- You have an editor access to Saagie Platform
- You have to create at least one project in Saagie Platform (in the example, we have one in `dev`, 
another in `prod`)
- Change `project_id` value inside all json file at `/saagie/job/`
- Remove the value of `job_id` for all json file at `/saagie/job/`

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
  `python __main__.py --action update --job_name your_job_name --saagie_url %SAAGIE_URL% --saagie_user %SAAGIE_LOGIN% --saagie_pwd %SAAGIE_PWD% --saagie_realm %SAAGIE_REALM% --saagie_env dev`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python __main__.py --action update --job_name your_job_name --saagie_url $SAAGIE_URL --saagie_user $SAAGIE_LOGIN --saagie_pwd $SAAGIE_PWD --saagie_realm $SAAGIE_REALM --saagie_env dev`

- To run a job, same thing as update, by using `--action run`,
  * For windows user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
        `python __main__.py --action run --job_name your_job_name --saagie_url %SAAGIE_URL% --saagie_user %SAAGIE_LOGIN% --saagie_pwd %SAAGIE_PWD% --saagie_realm %SAAGIE_REALM% --saagie_env dev`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python __main__.py --action run --job_name your_job_name --saagie_url $SAAGIE_URL --saagie_user $SAAGIE_LOGIN --saagie_pwd $SAAGIE_PWD --saagie_realm $SAAGIE_REALM --saagie_env dev`


## Configuration

In this repository, we have 2 directories:
- `code`:
  - each directories inside `code` is a job in Saagie
- `saagie`: 
  - `job`:
    - each json file is a configuration file for a job, the name of the file should be the same 
  as the name of job directory in `code`
  - `pipeline`:
    - each json file is a configuration file for a pipeline


### Job configuration file

Each json file inside `/saagie/job` has following schema: 

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

