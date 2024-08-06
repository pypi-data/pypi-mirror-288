import pickle
import time
from typing import List, Union, Optional
import numpy as np
from uniplot import plot_to_string
from xgboost import XGBRegressor, XGBClassifier
import logging
import importlib.resources

from .encoder import bin_encode_sequences

BASE_LOGGER = logging.getLogger('pepboost')


def load_default_model(filename):
    # Access the resource within the package
    with importlib.resources.open_binary('pepboost.predictor.models', filename) as file:
        model = pickle.load(file)
    return model


def _predict(model: Union[XGBRegressor, XGBClassifier],
             sequences: List[str],
             charges: Optional[List[int]] = None,
             logger: logging.Logger = BASE_LOGGER) -> np.ndarray:
    start_time = time.time()
    logger.info(f"Predicting for {len(sequences)} sequences.")
    X = bin_encode_sequences(sequences, charges, ignore_index_error=True)
    invalid_indices = np.where(X.sum(axis=1) == 0)[0]
    if len(invalid_indices) > 0:
        logger.warning(f"Found {len(invalid_indices)} invalid sequences.")
    preds = model.predict(X)
    preds[invalid_indices] = -1
    logger.info("Prediction completed in: %.2f seconds." % (time.time() - start_time))
    return preds


def _train(model: Union[XGBRegressor, XGBClassifier],
           sequences: List[str],
           labels: Union[List[float], List[bool]],
           charges: Optional[List[int]] = None,
           logger: logging.Logger = BASE_LOGGER) -> Union[XGBRegressor, XGBClassifier]:
    start_time = time.time()
    logger.info(f"Training model with {len(sequences)} sequences.")

    X = bin_encode_sequences(sequences, charges, ignore_index_error=False)

    if isinstance(model, XGBRegressor):
        y = np.array(labels, dtype=float)
    elif isinstance(model, XGBClassifier):
        y = np.array(labels, dtype=bool)
    else:
        raise ValueError("Model must be an instance of XGBRegressor or XGBClassifier.")

    model.fit(X, y)

    logger.info("Model training completed in: %.2f seconds." % (time.time() - start_time))
    return model


def _fine_tune(model: Union[XGBRegressor, XGBClassifier],
               sequences: List[str],
               labels: Union[List[float], List[bool]],
               charges: Optional[List[int]] = None,
               logger: logging.Logger = BASE_LOGGER) -> Union[XGBRegressor, XGBClassifier]:
    logger.info(f"Fine-tuning model with {len(sequences)} sequences.")
    model = _train(model=model,
                   sequences=sequences,
                   labels=labels,
                   charges=charges,
                   logger=logger)
    logger.info("Fine-tuning completed.")
    return model


def _uniplot(model: Union[XGBRegressor, XGBClassifier],
             sequences: List[str],
             labels: Union[List[float], List[bool]],
             plot_name: str,
             charges: Optional[List[int]] = None,
             logger: logging.Logger = BASE_LOGGER) -> str:
    logger.info(f"Generating plot for {len(sequences)} sequences.")
    preds = _predict(model=model, sequences=sequences, charges=charges, logger=logger)
    plot = '\n'.join(
        plot_to_string(labels, preds, lines=False, title=f"{plot_name}: Predicted vs Experimental"))
    logger.info("Plot generation completed.")
    return plot


def _r_squared(model: Union[XGBRegressor, XGBClassifier],
               sequences: List[str],
               labels: Union[List[float], List[bool]],
               charges: Optional[List[int]] = None,
               logger: logging.Logger = BASE_LOGGER) -> float:
    logger.info(f"Calculating R-squared for {len(sequences)} sequences.")
    preds = _predict(model=model, sequences=sequences, charges=charges, logger=logger)
    r2 = np.corrcoef(labels, preds)[0, 1] ** 2
    logger.info(f"R-squared calculation completed: {r2}")
    return r2


def save_model(model: Union[XGBRegressor, XGBClassifier], path: str) -> None:
    with open(path, "wb") as f:
        f.write(pickle.dumps(model))


def load_model(path: str) -> Union[XGBRegressor, XGBClassifier]:
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model


class BasePredictor:

    def save_model(self, path: str) -> None:
        save_model(self.model, path)
        self.logger.info(f"Model saved to {path}.")

    def load_model(self, path: str) -> None:
        self.model = load_model(path)
        self.logger.info(f"Model loaded from {path}.")
