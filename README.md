# Turing Segment: High-performance Cellpose Algorithm

***Turing Segment*** is a high-performance package for cell segmentation based on the popular [Cellpose](https://github.com/MouseLand/cellpose) algorithm. It is designed to provide lightning-fast performance while maintaining the accuracy and robustness of the original Cellpose model.

## Features
- Built on top of the Cellpose framework, leveraging its proven segmentation capabilities.
- Our new post-processing algorithm is significantly faster than the original Cellpose algorithm, reducing computational overhead and enabling faster processing times.
- Support Tiled processing that is optimized for handling large images. This allows for segmentation of high-resolution or whole-slide images without running into memory constraints.
- Turing Segment is highly parallelized, leveraging both CPU and GPU resources to achieve accelerated processing speeds.
- The package is designed to be easy to use. It provides a simple CLI for quick integration into your image analysis workflows.

## Installation

```bash
pip install <FILL_IT_LATER>
```

## Usage

Basic usage is as follows:

```bash
turing_segment <image_path>
```

You can specify the image type explicitly using the `--image-type` flag. If the flag is not specified, the image type is inferred from the input file. Currently, `tiff`, `zarr` and `cv2` are supported image types.

```bash
turing_segment <image_path> --image-type tiff
```

To specify channels to segment, use the `--channels` flag. The channels are specified as a comma-separated list of channel indices where the first channel is for membrane and the second channel is for nucleus. If the nucleus channel is not specified, a zero channel is used.

```bash
turing_segment <image_path> --channels 0,1
```

By default, the model checkpoints are downloaded if they are not present in the cache directory. If you want to use a custom checkpoint from cellpose training pipeline, you can set the model type as `--model-type manual` and specify the paths to the model and size model checkpoints using the `--model-path` and `--size-model-path` flags, respectively. You may skip specifying `--size-model-path` if a provided scale is specified by ``--scale``.

```bash
turing_segment <image_path> --model-type manual --model-path <path_to_model_checkpoint> --size-model-path <path_to_size_model_checkpoint>
```

To see the full list of available options, use the `--help` flag.

```bash
turing_segment --help
```

## Feedback

If you encounter any issues or bugs while using Turing Segment, please let us know by submitting an issue on this GitHub repository.

For other feedback or support, you can reach out to our dedicated support team at [support@bioturing.com](mailto:support@bioturing.com).


