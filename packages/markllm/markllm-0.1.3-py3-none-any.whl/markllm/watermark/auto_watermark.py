# =========================================================================
# AutoWatermark.py
# Description: This is a generic watermark class that will be instantiated 
#              as one of the watermark classes of the library when created 
#              with the [`AutoWatermark.load`] class method.
# =========================================================================

import importlib

WATERMARK_MAPPING_NAMES={
    'KGW': 'markllm.watermark.kgw.KGW',
    'Unigram': 'markllm.watermark.unigram.Unigram',
    'SWEET': 'markllm.watermark.sweet.SWEET',
    'UPV': 'markllm.watermark.upv.UPV',
    'SIR': 'markllm.watermark.sir.SIR',
    'XSIR': 'markllm.watermark.xsir.XSIR',
    'EWD': 'markllm.watermark.ewd.EWD',
    'EXP': 'markllm.watermark.exp.EXP',
    'EXPEdit': 'markllm.watermark.exp_edit.EXPEdit',
    'ITSEdit': 'markllm.watermark.its_edit.ITSEdit'
}

def watermark_name_from_alg_name(name):
    """Get the watermark class name from the algorithm name."""
    for algorithm_name, watermark_name in WATERMARK_MAPPING_NAMES.items():
        if name == algorithm_name:
            return watermark_name
    return None

class AutoWatermark:
    """
        This is a generic watermark class that will be instantiated as one of the watermark classes of the library when
        created with the [`AutoWatermark.load`] class method.

        This class cannot be instantiated directly using `__init__()` (throws an error).
    """

    def __init__(self):
        raise EnvironmentError(
            "AutoWatermark is designed to be instantiated "
            "using the `AutoWatermark.load(algorithm_name, algorithm_config, transformers_config)` method."
        )

    def load(algorithm_name, algorithm_config=None, transformers_config=None, *args, **kwargs):
        """Load the watermark algorithm instance based on the algorithm name."""
        watermark_name = watermark_name_from_alg_name(algorithm_name)
        module_name, class_name = watermark_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        watermark_class = getattr(module, class_name)
        watermark_instance = watermark_class(algorithm_config, transformers_config)
        return watermark_instance

