import os

from prefect import context, task, Flow, Parameter
from prefect.triggers import all_finished
from prefect.tasks.dbt import DbtShellTask
from prefect.storage import Docker
from prefect.run_configs import DockerRun


def create_dbt_task() -> DbtShellTask:
    """Create DbtShellTask using the specified argument

    Returns
    -------
    DbtShellTask
        Description
    """

    return DbtShellTask(
        return_all=True,
        profiles_dir=os.environ.get("DBT_PROFILES_DIR", "."),
        helper_script="cd dbt",
        log_stdout=True,
        log_stderr=True,
    )


@task(trigger=all_finished)
def output_print(output):
    logger = context.get("logger")
    if isinstance(output, str) or isinstance(output, list):
        for line in output:
            logger.info(line)

    return None


@task
def build_dbt_command(
    dbt_build_select_args: str, dbt_build_exclude_args: str, full_refresh: bool
) -> str:

    dbt_cmd = "dbt build"

    if dbt_build_select_args:
        dbt_cmd += f"--select {dbt_build_select_args} "

    if dbt_build_exclude_args:
        dbt_cmd += f"--exclude {dbt_build_exclude_args} "

    if full_refresh:
        dbt_cmd += " --full-refresh"

    return dbt_cmd.strip()


def create_dbt_flow(flow_name: str) -> Flow:

    dbt = create_dbt_task()

    with Flow(name=flow_name) as flow:

        # argument of --select option
        dbt_build_select_args = Parameter(
            "dbt_build_select_args", default="", required=False
        )
        # argument of --exclude option
        dbt_build_exclude_args = Parameter(
            "dbt_build_exclude_args", default="", required=False
        )
        # flag for using --full-refresh option
        full_refresh = Parameter("full_refresh", default=False, required=False)

        # argument of --resource-type
        # resource_type_arg = Parameter(
        #     "resource_type_arg", default="", required=False
        # )

        dbt_cmd = build_dbt_command(
            dbt_build_select_args,
            dbt_build_exclude_args,
            full_refresh,
        )

        # execute dbt build
        dbt_build = dbt(
            command=dbt_cmd,
            task_args={"name": "dbt build"},
        )

        # log dbt output to Prefect
        output_print(dbt_build, task_args={"name": "log dbt output"})

    return flow


flow = create_dbt_flow("dbt test flow")


if __name__ == "__main__":

    docker_storage = Docker(
        image_name="prefect-dbt-demo",
        image_tag="latest",
        local_image=True,
        stored_as_script=True,
        path="/opt/prefect/flows/dbt_flow.py",
    )

    flow.storage = docker_storage
    docker_storage.add_flow(flow)

    flow.run_config = DockerRun(image="prefect-dbt-demo:latest")

    flow.register(project_name="tutorials", build=False)
