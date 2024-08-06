import logging
from typing import Union, List, Optional
from xgboost import XGBRegressor

import numpy as np

from .base import _predict, _fine_tune, _train, _uniplot, _r_squared, BasePredictor, load_default_model
from .constants import DEFAULT_IM_MODEL


class ImPredictor(BasePredictor):

    def __init__(self, model: Optional[XGBRegressor] = None, verbose: bool = False):

        if model is None:
            self.model = load_default_model(DEFAULT_IM_MODEL)
        else:
            self.model = model

        if not isinstance(self.model, XGBRegressor):
            raise ValueError("Model path must be a string or an instance of XGBRegressor.")

        self.verbose = verbose
        self.logger = logging.getLogger('ImPredictor')
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
              ion_mobilities: List[float],
              verbose: bool = False) -> XGBRegressor:

        logger = logging.getLogger('ImPredictor')

        if verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        model = XGBRegressor()
        return _train(model=model,
                      sequences=sequences,
                      labels=ion_mobilities,
                      charges=charges,
                      logger=logger)

    def fine_tune(self, sequences: List[str],
                  charges: List[int],
                  ion_mobilities: List[float]) -> XGBRegressor:

        return _fine_tune(model=self.model,
                          sequences=sequences,
                          labels=ion_mobilities,
                          charges=charges,
                          logger=self.logger)

    def uniplot(self, sequences: List[str],
                charges: List[int],
                ion_mobilities: List[float], ) -> str:

        return _uniplot(model=self.model,
                        sequences=sequences,
                        labels=ion_mobilities,
                        plot_name='Ion Mobility',
                        charges=charges,
                        logger=self.logger)

    def r_squared(self, sequences: List[str],
                  charges: List[int],
                  ion_mobilities: List[float], ) -> float:

        return _r_squared(model=self.model,
                          sequences=sequences,
                          labels=ion_mobilities,
                          charges=charges,
                          logger=self.logger)
