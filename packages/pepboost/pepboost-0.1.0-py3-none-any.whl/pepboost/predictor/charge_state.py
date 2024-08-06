import logging
from typing import Union, List, Optional
from xgboost import XGBRegressor

import numpy as np

from .base import _predict, _fine_tune, _train, _uniplot, _r_squared, BasePredictor, load_default_model
from .constants import DEFAULT_CHARGE_MODEL


class ChargePredictor(BasePredictor):

    def __init__(self, model: Optional[XGBRegressor] = None, verbose: bool = False):

        if model is None:
            self.model = load_default_model(DEFAULT_CHARGE_MODEL)
        else:
            self.model = model

        if not isinstance(self.model, XGBRegressor):
            raise ValueError("Model path must be a string or an instance of XGBRegressor.")

        self.verbose = verbose
        self.logger = logging.getLogger('ChargePredictor')
        self.logger.setLevel(logging.INFO if verbose else logging.WARNING)
        self.logger.info("ChargePredictor initialized.")

    def predict(self, sequences: List[str], charges: List[int]) -> np.ndarray:
        return _predict(model=self.model,
                        sequences=sequences,
                        charges=charges,
                        logger=self.logger)

    @classmethod
    def train(cls, sequences: List[str],
              charges: List[int],
              intensities: List[float],
              verbose: bool = False) -> XGBRegressor:

        logger = logging.getLogger('ChargePredictor')

        if verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        model = XGBRegressor()
        return _train(model=model,
                      sequences=sequences,
                      labels=intensities,
                      charges=charges,
                      logger=logger)

    def fine_tune(self, sequences: List[str],
                  charges: List[int],
                  intensities: List[float]) -> XGBRegressor:

        return _fine_tune(model=self.model,
                          sequences=sequences,
                          labels=intensities,
                          charges=charges,
                            logger=self.logger)

    def uniplot(self, sequences: List[str],
                charges: List[int],
                intensities: List[float], ) -> str:

        return _uniplot(model=self.model,
                        sequences=sequences,
                        labels=intensities,
                        plot_name='Intensity',
                        charges=charges,
                        logger=self.logger)

    def r_squared(self, sequences: List[str],
                  charges: List[int],
                  intensities: List[float], ) -> float:

        return _r_squared(model=self.model,
                          sequences=sequences,
                          labels=intensities,
                          charges=charges,
                          logger=self.logger)

