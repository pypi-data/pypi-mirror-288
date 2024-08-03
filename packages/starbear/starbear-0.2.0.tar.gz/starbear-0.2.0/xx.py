import gifnoc
from starbear import config

# from dataclasses import dataclass
# from pathlib import Path
# import gifnoc

# @dataclass
# class StarbearConfig:
#     debug: bool = False

# config = gifnoc.define(
#     field="starbear",
#     model=StarbearConfig,
# )

with gifnoc.use("testconfig.yaml"):
    breakpoint()
    print(config.debug)


# from dataclasses import dataclass
# from pathlib import Path
# import gifnoc

# @dataclass
# class StarbearConfig:
#     debug: bool = False

# config = gifnoc.define(
#     field="starbear",
#     model=StarbearConfig,
# )

# with gifnoc.use(Path("testconfig.yaml")):
#     print(config.debug)
