import pandas as pd
from .predictor import RtPredictor, ImPredictor, ChargePredictor


def train_rt_model(df: pd.DataFrame,
                   peptide_col: str = 'peptide',
                   retention_time_col: str = 'rt') -> RtPredictor:
    sequences = df[peptide_col].values
    rts = df[retention_time_col].values
    model = RtPredictor.train(sequences, rts)
    return RtPredictor(model=model)


def train_im_model(df: pd.DataFrame,
                   peptide_col: str = 'peptide',
                   charge_col: str = 'charge',
                   ion_mobility_col: str = 'im') -> ImPredictor:
    sequences = df[peptide_col].values
    charges = df[charge_col].values
    ims = df[ion_mobility_col].values
    model = ImPredictor.train(sequences, charges, ims)
    return ImPredictor(model=model)


def train_charge_model(df: pd.DataFrame,
                       peptide_col: str = 'peptide',
                       charge_col: str = 'charge',
                       intensity_col: str = 'intensity') -> ChargePredictor:
    sequences = df[peptide_col].values
    charges = df[charge_col].values
    intensities = df[intensity_col].values
    model = ChargePredictor.train(sequences, charges, intensities)
    return ChargePredictor(model=model)


