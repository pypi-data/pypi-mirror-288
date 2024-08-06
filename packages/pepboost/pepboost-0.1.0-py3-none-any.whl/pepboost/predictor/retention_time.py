import logging
from typing import Union, List, Optional
from xgboost import XGBRegressor

import numpy as np

from .base import _predict, _fine_tune, _train, _uniplot, _r_squared, BasePredictor, load_default_model
from .constants import DEFAULT_RT_MODEL


class RtPredictor(BasePredictor):

    def __init__(self, model: Optional[XGBRegressor] = None, verbose: bool = False):

        if model is None:
            self.model = load_default_model(DEFAULT_RT_MODEL)
        else:
            self.model = model

        if not isinstance(self.model, XGBRegressor):
            raise ValueError("Model path must be a string or an instance of XGBRegressor.")

        self.verbose = verbose
        self.logger = logging.getLogger('RtPredictor')
        self.logger.setLevel(logging.INFO if verbose else logging.WARNING)
        self.logger.info("ChargePredictor initialized.")

    def predict(self, sequences: List[str], gradient: Optional[float] = None) -> np.ndarray:
        preds = _predict(model=self.model,
                         sequences=sequences,
                         charges=None,
                         logger=self.logger)

        if gradient is not None:
            preds *= gradient

        return preds

    @classmethod
    def train(cls, sequences: List[str],
              retention_times: List[float],
              verbose: bool = False) -> XGBRegressor:

        logger = logging.getLogger('RtPredictor')

        if verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        model = XGBRegressor()
        return _train(model=model,
                      sequences=sequences,
                      labels=retention_times,
                      charges=None,
                      logger=logger)

    def fine_tune(self, sequences: List[str],
                  retention_times: List[float]) -> XGBRegressor:

        return _fine_tune(model=self.model,
                          sequences=sequences,
                          labels=retention_times,
                          charges=None,
                            logger=self.logger)

    def uniplot(self, sequences: List[str],
                retention_times: List[float]) -> str:

        return _uniplot(model=self.model,
                        sequences=sequences,
                        labels=retention_times,
                        plot_name='Retention Time',
                        charges=None,
                        logger=self.logger)

    def r_squared(self, sequences: List[str],
                  retention_times: List[float]) -> float:

        return _r_squared(model=self.model,
                          sequences=sequences,
                          labels=retention_times,
                          charges=None,
                          logger=self.logger)
