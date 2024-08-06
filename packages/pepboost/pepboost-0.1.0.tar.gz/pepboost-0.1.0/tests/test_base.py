from pepboost.base import NAME
from pepboost.predictor.charge_state import ChargePredictor
from pepboost.predictor.ion_mobility import ImPredictor
from pepboost.predictor.retention_time import RtPredictor

PEPTIDES = ['VGFYDIERTLGK', 'MVIMSEFSADPAGQGQGQQKPLR', 'VGFYDIERMV']
CHARGES = [2, 3, 4]
VALUES = [1.0, 2.0, 3.0]


def test_base():
    assert NAME == "pepboost"


def test_predictors():
    model = RtPredictor.train(PEPTIDES, VALUES)
    rt_predictor = RtPredictor(model)
    preds = rt_predictor.predict(PEPTIDES)
    print(preds)
    assert len(preds) == len(PEPTIDES)
    rt_predictor.fine_tune(PEPTIDES, VALUES)
    p = rt_predictor.uniplot(PEPTIDES, VALUES)
    r = rt_predictor.r_squared(PEPTIDES, VALUES)

    model = ImPredictor.train(PEPTIDES, CHARGES, VALUES)
    im_predictor = ImPredictor(model)
    preds = im_predictor.predict(PEPTIDES, CHARGES)
    assert len(preds) == len(PEPTIDES)
    im_predictor.fine_tune(PEPTIDES, CHARGES, VALUES)
    p = im_predictor.uniplot(PEPTIDES, CHARGES, VALUES)
    r = im_predictor.r_squared(PEPTIDES, CHARGES, VALUES)

    model = ChargePredictor.train(PEPTIDES, CHARGES, VALUES)
    charge_predictor = ChargePredictor(model)
    preds = charge_predictor.predict(PEPTIDES, CHARGES)
    assert len(preds) == len(PEPTIDES)
    charge_predictor.fine_tune(PEPTIDES, CHARGES, VALUES)
    p = charge_predictor.uniplot(PEPTIDES, CHARGES, VALUES)
    r = charge_predictor.r_squared(PEPTIDES, CHARGES, VALUES)


def test_load_defaults():
    rt_predictor = RtPredictor()
    im_predictor = ImPredictor()
    charge_predictor = ChargePredictor()

    assert rt_predictor.model is not None
    assert im_predictor.model is not None
    assert charge_predictor.model is not None

    preds = rt_predictor.predict(PEPTIDES)
    assert len(preds) == len(PEPTIDES)
    preds = im_predictor.predict(PEPTIDES, CHARGES)
    assert len(preds) == len(PEPTIDES)
    preds = charge_predictor.predict(PEPTIDES, CHARGES)
    assert len(preds) == len(PEPTIDES)
