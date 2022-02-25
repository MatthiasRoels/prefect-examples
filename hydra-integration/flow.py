from hydra import initialize, compose
from omegaconf import DictConfig, OmegaConf
from prefect import Flow, task

from prefect.engine.results import LocalResult
from prefect.engine.serializers import JSONSerializer

@task
def main_task() -> list:
    return [1, 2, 3]


def configure_result(result_conf) -> dict:

    extra_args = OmegaConf.to_container(result_conf.extra_args, resolve=True)

    if result_conf.get("serializer", None):
        serializer = eval(result_conf.serializer)()

    if result_conf.result_class == "LocalResult":
        return LocalResult(
            location=result_conf.location,
            **extra_args,
            serializer=serializer,
        )


def create_flow(flow_name: str) -> Flow:
    initialize(config_path="conf")
    cfg = compose("config.yaml", overrides=["db=postgres"])

    with Flow(flow_name) as flow:
        print(OmegaConf.to_yaml(cfg, resolve=True))

        output = main_task(
            task_args={"result": configure_result(cfg.catalog.data_source)}
        )

    return flow


flow = create_flow("test_flow")


if __name__ == "__main__":
    flow.run()
