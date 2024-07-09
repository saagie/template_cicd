# Example of CI/CD with saagieapi (Python)

## Description
This project contains an __example__ to use github action to deploy jobs inside Saagie Platform using
[saagieapi](https://saagieapi.readthedocs.io/en/latest/).

You can use the following actions to interact with Saagie platform: `package_job`, `update_job`, `run_job`,
`update_pipeline` and `run_pipeline`.
Packaging only available for python package code.

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
- Create the following environment variables:
  * SAAGIE_URL
  * SAAGIE_USER
  * SAAGIE_PWD
  * SAAGIE_REALM
- If you have only one environment in Saagie, you can remove the `dev` directory inside `saagie/envs/`, and you create 
a json file with your environment name: `your_env_name.json`
- In your `saagie/envs/your_env_name.json`, you have to specify 3 key values:
  - `platform_id`
  - `project_id`
  - `project_name`


### Local prerequisite

- Install Python (at least 3.8) and all libraries in `requirements.txt`


## Configuration

If you want to use the CI for your own jobs, make sure that the respect of the following file organisation.
In this repository, we have 2 directories:
- `code`:
  - each directories inside `code` is a __job__ in Saagie
- `saagie`:
  - `envs`:
    - each json file is a configuration file for an environment
  - `jobs`:
    - each json file is a configuration file for a job, the name of the file should be the same
      as the name of job directory in `code`
  - `pipelines`:
    - each json file is a configuration file for a pipeline

You can also modify github workflows. For now, each push on a branch will trigger a check to see which configuration files have
been modified. Based on this, it will trigger actions such as updating a job, or updating a pipeline.








## How to use it in local

- To package a job, you can run the following command by replacing `your_job_name` by the job that you want to package: `python __main__.py --action package_job --job_name your_job_name`.
It suppose that your job code is in `code/your_job_name`
- To update a job,
  * For windows user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python cicd_saagie_tool/__main__.py --action update_job --job_name your_job_name --saagie_url "%SAAGIE_URL%" --saagie_user "%SAAGIE_USER%" --saagie_pwd "%SAAGIE_PWD%" --saagie_realm "%SAAGIE_REALM%" --saagie_env your_env_name`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python cicd_saagie_tool/__main__.py --action update_job --job_name your_job_name --saagie_url "$SAAGIE_URL" --saagie_user "$SAAGIE_USER" --saagie_pwd "$SAAGIE_PWD" --saagie_realm "$SAAGIE_REALM" --saagie_env your_env_name`

- To run a job, same thing as update, by using `--action run`,
  * For windows user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python cicd_saagie_tool/__main__.py --action run_job --job_name your_job_name --saagie_url "%SAAGIE_URL%" --saagie_user "%SAAGIE_USER%" --saagie_pwd "%SAAGIE_PWD%" --saagie_realm "%SAAGIE_REALM%" --saagie_env your_env_name`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python cicd_saagie_tool/__main__.py --action run_job --job_name your_job_name --saagie_url "$SAAGIE_URL" --saagie_user "$SAAGIE_USER" --saagie_pwd "$SAAGIE_PWD" --saagie_realm "$SAAGIE_REALM" --saagie_env your_env_name`

- To update a pipeline,
  * For windows user, use the following command line by replacing `your_pipeline_name` and `dev` if you want to use another environment:
    `python cicd_saagie_tool/__main__.py --action update_pipeline --pipeline_name your_pipeline_name --saagie_url "%SAAGIE_URL%" --saagie_user "%SAAGIE_USER%" --saagie_pwd "%SAAGIE_PWD%" --saagie_realm "%SAAGIE_REALM%" --saagie_env your_env_name`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python cicd_saagie_tool/__main__.py --action update_pipeline --pipeline_name your_pipeline_name --saagie_url "$SAAGIE_URL" --saagie_user "$SAAGIE_USER" --saagie_pwd "$SAAGIE_PWD" --saagie_realm "$SAAGIE_REALM" --saagie_env your_env_name`

- To run a pipeline,
  * For windows user, use the following command line by replacing `your_pipeline_name` and `dev` if you want to use another environment:
    `python cicd_saagie_tool/__main__.py --action run_pipeline --pipeline_name your_pipeline_name --saagie_url "%SAAGIE_URL%" --saagie_user "%SAAGIE_USER%" --saagie_pwd "%SAAGIE_PWD%" --saagie_realm "%SAAGIE_REALM%" --saagie_env your_env_name`

  * For Linux user, use the following command line by replacing `your_job_name` and `dev` if you want to use another environment:
    `python cicd_saagie_tool/__main__.py --action run_pipeline --pipeline_name your_pipeline_name --saagie_url "$SAAGIE_URL" --saagie_user "$SAAGIE_USER" --saagie_pwd "$SAAGIE_PWD" --saagie_realm "$SAAGIE_REALM" --saagie_env your_env_name`


### Environment configuration file

Each json file inside `/saagie/envs` has following schema:

#### Environment

_An environment inside Saagie_

Type: `object`

**_Properties_**

- **_platform_id_** `required`
  - _ID of Saagie platform_
  - Type: `string`
  - Example: `"1"`
- **_project_id_** `required`
  - _ID of the Saagie project_
  - Type: `UUID`
  - Example: `"5d714745-1fea-4b30-ab5c-a9965a028355"`
- **_project_name_** `required`
  - _Name of the Saagie project_
  - Type: `string`
  - Example: `"My project"`


### Job configuration file

Each json file inside `/saagie/jobs` has following schema:

#### Job

_A job inside Saagie_

Type: `object`

**_Properties_**

- **_job_name_** `required`
  - _Job name_
  - Type: `string`
  - Example: `Job extraction`
- **_file_path_** `required`
  - _File path of the code_
  - Type: `string`
  - Example: `./path/to/code/artefact.zip`
- **_description_** `optional`
  - _Description for your job. If not filled or not present, defaults to current value_
  - Type: `string`
  - Example: `This is my description`
- **_category_** `optional`
  - _Category of the job, If not filled or not present, defaults to current value_
  - Type: `string`
  - Must be `Extraction`, `Processing` or `Smart App`
- **_technology_** `optional`
  - _Technology label of the job. Only required for the creation, and it's not possible to change this value for a job_
  - Type: `string`
  - Example: `Python`
- **_technology_catalog_** `optional`
  - _Technology catalog containing the technology to use for this job. Only required for the creation, and it's not possible to change this value for a job_
  - Type: `string`
  - Example: `Saagie`
- **_runtime_version_** `optional`
  - _Technology version of the job, the ID of the context, If not filled or not present, defaults to current value_
  - Type: `string`
  - Example: `3.10`
- **_command_line_** `optional`
  - _Command line of the job, If not filled or not present, defaults to current value_
  - Type: `string`
  - Example: `python {file}`
- **_extra_technology_** `optional`
  - _Extra technology when needed (spark jobs). If not needed, leave to
    empty string or the request will not work_
  - Type: `string`
- **_extra_technology_version_** `optional`
  - _Version of the extra technology. Leave to empty string when not
    needed_
  - Type: `string`



#### Pipeline

Each file inside `/saagie/pipelines` has following schema:

_A pipeline inside Saagie_

Type: `object`

**_Properties_**
- **_file_path_** `required`
  - _The path of pipeline artefact_
  - Type: `string`

A pipeline artefact have the following schema, it's a yaml file.

_A pipeline inside Saagie_
Type: `object`

**_Properties_**
- **_schema_** `required`
  - _Version of schema_
  - Type: `string`
- **_pipeline_** `required`
  - _Dict that contains all information of the pipeline_
  - Type: `object`
  - **_Properties_**:
    - **_name_** `required`
      - _Name of the pipeline_
      - Type: `string`
    - **_alias_** `required`
      - _Alias of the pipeline, it cannot contain special character_
      - Type: `string`
    - **_executionVariables_** `required`
      - _Whether to activate the execution variables. If not filled or not present, defaults to current value_
        - Type: `bool`
        - Example:  `false`
    - **_node_** `required`
      - _Dict of pipeline's node_
      - Type: `object`
    - **_Properties_**:
      - **_job_**
        - _List of job nodes_
        - Type: `object`
        - **_Properties_**:
          - **_alias_** `required`
            - _Job alias_
            - Type: `string`
            - Example: `my_first_job`
          - **_node_** `required`
            - _An identifier in the yaml file to identify this node_
            - Type: `string`
            - Example: `node1`
          - **_next_nodes_** `optional`
            - _Next nodes of this job, each value in the list should be the identifier `node` of job or condition in the yaml file_
            - Type: `List[string]`
            - Example: `["node1"]`
      - **_conditionStatus_**
        - _List of condition on status nodes_
        - Type: `object`
        - **_Properties_**:
          - **_trigger_** `required`
            - _How to trigger this status. Can be `AllSuccessOrSkipped`, or `AllSuccess` or `AtLeastOneSuccess`_
            - Type: `string`
            - Example: `AllSuccessOrSkipped`
          - **_node_** `required`
            - _An identifier in the yaml file to identify this node_
            - Type: `string`
            - Example: `node_condition_status1`
          - **_nextNodesSuccess_**
            - _Next nodes of this job in case of success, each value in the list should be the identifier `node` of job or condition_
            - Type: `List[string]`
            - Example: `["node1"]`
          - **_next_nodes_failure_**
            - _Next nodes of this job in case of failure, each value in the list should be the identifier `node` of job or condition_
            - Type: `List[string]`
            - Example: `["node2"]`
      - **_conditionExpression_**
        - _List of condition on expression nodes_
        - Type: `object`
        - **_Properties_**:
          - **_expression_** `required`
            - _The expression to evaluate, the expession should use CEL specification_
            - Type: `string`
            - Example: `1 + 1 == 2`
          - **_node_** `required`
            - _An identifier in the yaml file to identify this node_
            - Type: `string`
            - Example: `node_condition_status1`
          - **_nextNodesSuccess_**
            - _Next nodes of this job in case of success, each value in the list should be the identifier `node` of job or condition_
            - Type: `List[string]`
            - Example: `["node1"]`
          - **_next_nodes_failure_**
            - _Next nodes of this job in case of failure, each value in the list should be the identifier `node` of job or condition_
            - Type: `List[string]`
            - Example: `["node2"]`