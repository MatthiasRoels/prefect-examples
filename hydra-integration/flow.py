from hydra import initialize, compose
from omegaconf import DictConfig, OmegaConf
from prefect import Flow, task


def create_flow(flow_name: str) -> Flow:
    initialize(config_path="conf")
    cfg = compose("config.yaml", overrides=["db=postgres"])

    with Flow(flow_name) as flow:
        print(OmegaConf.to_yaml(cfg))

    return flow


flow = create_flow("test_flow")


if __name__ == "__main__":
    flow.run()
