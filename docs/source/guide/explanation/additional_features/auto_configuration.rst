Auto-configuration
==================

Auto-configuration for a deep learning framework means the automatic finding of the most appropriate settings for the training parameters, based on the dataset and the specific task at hand.
Auto-configuration can help to save time, it eases the process of interaction with OTX CLI and gives a better baseline for the given dataset.

At this end, we developed a simple auto-configuration functionality to ease the process of training and validation utilizing our framework.
Basically, to start the training and obtain a good baseline with the best trade-off between accuracy and speed we need to pass only a dataset in the right format without specifying anything else:

.. code-block::

    $ otx train --train-data-root <path_to_data_root>

.. note::

    OTX supports also ``otx build`` mode with the auto-configuration feature. We can build OTX workspace with the following CLI command:

    .. code-block::

        $ otx build --train-data-root <path_to_data_root>

Moreover, our dataset can have no train/val splits at all. The Datumaro manager integrated into OTX will handle it on its own.
It will recognize the task by analyzing the dataset and if there is no splits for the validation - Datumaro will do a random auto-split, saving this split to the workspace. It could be used with ``otx optimize`` or ``otx train``.

.. note::

    Currently, Datumaro auto-split feature supports 3 formats: `Imagenet <https://www.image-net.org/>`_  (multi-class classification), `COCO <https://cocodataset.org/#format-data>`_ (detection) and `Cityscapes <https://openvinotoolkit.github.io/datumaro/docs/formats/cityscapes/>`_ (semantic segmentation).

After dataset preparation, the training will be started with the middle-sized template to achieve competitive accuracy preserving fast inference.

.. note::

    Supported dataset formats for each task:

    - classificaiton: `Imagenet <https://www.image-net.org/>`_, `COCO <https://cocodataset.org/#format-data>`_ (multi-label), :ref:`custom hierarchical <hierarchical_dataset>`
    - object detection: `COCO <https://cocodataset.org/#format-data>`_, `Pascal-VOC <https://openvinotoolkit.github.io/datumaro/docs/formats/pascal_voc/>`_, `YOLO <https://openvinotoolkit.github.io/datumaro/docs/formats/yolo/>`_
    - semantic segmentation: `Common Semantic Segmentation <https://openvinotoolkit.github.io/datumaro/docs/formats/common_semantic_segmentation/>`_, `Pascal-VOC <https://openvinotoolkit.github.io/datumaro/docs/formats/pascal_voc/>`_, `Cityscapes <https://openvinotoolkit.github.io/datumaro/docs/formats/cityscapes/>`_, `ADE20k <https://openvinotoolkit.github.io/datumaro/docs/formats/ade20k2020/>`_
    - action classification: `CVAT <https://opencv.github.io/cvat/docs/manual/advanced/xml_format/>`_
    - action : `CVAT <https://opencv.github.io/cvat/docs/manual/advanced/xml_format/>`_
    - anomaly classificaiton: `MVTec <https://www.mvtec.com/company/research/datasets/mvtec-ad>`_
    - anomaly detection: `MVTec <https://www.mvtec.com/company/research/datasets/mvtec-ad>`_
    - anomaly segmentation: `MVTec <https://www.mvtec.com/company/research/datasets/mvtec-ad>`_
    - instance segmentation: `COCO <https://cocodataset.org/#format-data>`_, `Pascal-VOC <https://openvinotoolkit.github.io/datumaro/docs/formats/pascal_voc/>`_

    If we have a dataset format occluded with other tasks, for example ``COCO`` format, we should directly emphasize the task type and use `otx build` first with an additional CLI option. If not, OTX automatically chooses the task type that you might don't intend:

    .. code-block::

        $ otx build --train-data-root <path_to_data_root> --task {CLASSIFICATION, DETECTION, SEGMENTATION, ACTION_CLASSIFICATION, ACTION_DETECTION, ANOMALY_CLASSIFICATION, ANOMALY_DETECTION, ANOMALY_SEGMENTATION, INSTANCE_SEGMENTATION}

    It will create a task-specific workspace folder with configured template and auto dataset split if supported.

    Move to this folder and simply run without any options to start training:

    .. code-block::

        $ otx train
