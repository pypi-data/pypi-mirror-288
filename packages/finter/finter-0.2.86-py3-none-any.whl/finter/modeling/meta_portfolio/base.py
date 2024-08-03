import os
from pathlib import Path
import re
import inspect

from abc import ABCMeta
from typing import Optional
from pydantic import BaseModel

from finter import BasePortfolio
from finter.settings import logger
from finter.framework_model.submission.helper_submission import submit_model

from finter.framework_model.submission.config import (
    ModelTypeConfig,
    ModelUniverseConfig,
)


class PortfolioClassMeta(ABCMeta):
    def __new__(cls, name, bases, dct) -> type["BaseMetaPortfolio"]:
        return super().__new__(cls, name, bases, dct)


class BaseParameters(BaseModel):
    universe: ModelUniverseConfig
    alpha_set: set[str]


class BaseMetaPortfolio(BasePortfolio, metaclass=PortfolioClassMeta):
    _param: Optional[BaseParameters] = None
    _model_type = ModelTypeConfig.PORTFOLIO

    class Parameters(BaseParameters): ...

    universe: ModelUniverseConfig = ModelUniverseConfig.KR_STOCK
    alpha_set: set[str] = set()

    def alpha_loader(self, start, end):
        mi = self.get_model_info()
        return self.get_alpha_position_loader(
            start,
            end,
            mi["exchange"],
            mi["universe"],
            mi["instrument_type"],
            mi["freq"],
            mi["position_type"],
        )

    @classmethod
    def get_model_info(cls):
        return cls.universe.get_config(cls._model_type)

    @classmethod
    def submit(
        cls,
        model_name: str,
        staging: bool = False,
        **kwargs,
    ):
        outdir = Path(model_name)
        os.makedirs(outdir, exist_ok=True)

        source = cls.get_submit_code()

        with open(outdir / cls._model_type.file_name, "w", encoding="utf-8") as fd:
            fd.write(source)

        model_info = cls.get_model_info()

        if "insample" in kwargs:
            insample = kwargs.pop("insample")

            if not re.match(r"^\d+ days$", insample):
                raise ValueError("insample should be like '100 days'")

            model_info["insample"] = insample
            if kwargs:
                logger.warn(f"Unused parameters: {kwargs}")

        res = submit_model(model_info, model_name, docker_submit=False, staging=staging)

        return res

    @classmethod
    def get_source_code(cls):
        return inspect.getsource(cls.__bases__[0])

    @classmethod
    def create(cls, params: BaseParameters):
        dct = params.dict()
        dct["_param"] = params

        clz = PortfolioClassMeta("Portfolio", (cls,), dct)
        return clz

    @classmethod
    def get_submit_code(cls):
        meta_model = cls.__bases__[0]
        module_path = meta_model.__module__
        param = cls._param
        jsonstr = param.json()

        return f"""
from {module_path} import {meta_model.__name__}

param_json = r'{jsonstr}'
params = {meta_model.__name__}.Parameters.parse_raw(param_json)
Portfolio = {meta_model.__name__}.create(params)
"""
