"""MMDeploy config of ATSS model for Detection Task."""

_base_ = ["../../base/deployments/base_detection_dynamic.py"]

ir_config = dict(
    output_names=["boxes", "labels", "feature_vector", "saliency_map"],
)

backend_config = dict(
    model_inputs=[dict(opt_shapes=dict(input=[-1, 3, 736, 992]))],
)
