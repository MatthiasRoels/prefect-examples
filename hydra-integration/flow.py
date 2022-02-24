import hydra
from omegaconf import DictConfig, OmegaConf
from prefect import flow, task


@hydra.main(config_path="conf", config_name="config")
@flow
def test_flow(cfg: DictConfig) -> None:
    print("test")
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    test_flow()
