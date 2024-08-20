# Turing Segment: High-performance Cellpose Algorithm

***Turing Segment*** is a high-performance package for cell segmentation based on the popular [Cellpose](https://github.com/MouseLand/cellpose) algorithm. It is designed to provide lightning-fast performance while maintaining the accuracy and robustness of the original Cellpose model.

## Features
- Built on top of the Cellpose framework, leveraging its proven segmentation capabilities.
- Our new post-processing algorithm is significantly faster than the original Cellpose algorithm, reducing computational overhead and enabling faster processing times.
- Support Tiled processing that is optimized for handling large images. This allows for segmentation of high-resolution or whole-slide images without running into memory constraints.
- Turing Segment is highly parallelized, leveraging both CPU and GPU resources to achieve accelerated processing speeds.
- The package is designed to be easy to use. It provides a simple CLI for quick integration into your image analysis workflows.

## Requirements
- NVIDIA GPU (recommend 40xx series, but it should work on lower series as well)
- CUDA Runtime 11.7 or later
- Python 3.8 or later
- PyTorch 2.0 or later
- geopandas 1.0 or later

## Installation

We recommend using conda to install Turing Segment. Run the following command to create a new conda environment:

```bash
conda create -n turing_segment python=3.10
conda activate turing_segment
```

Make sure your PyTorch version is compatible with the CUDA Runtime version and select the correct PyTorch version from the [PyTorch website](https://pytorch.org/get-started/locally/). For example, if you have CUDA 12.1, use the following command to install PyTorch:

```bash
conda install pytorch pytorch-cuda=12.1 -c pytorch -c nvidia
```

Install Turing Segment using `pip`:

```bash
pip install --index-url https://pypi.bioturing.com/simple turing_segment
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

The tool also supports modifying some parameters of the segmentation process and post-processing. This can be done by using `--config-file` to specify a YAML configuration file containing the parameters:

```bash
turing_segment <image_path> --config-file <path_to_config_file>
```

A sample config file can be found from `configs/config.yaml`, the parameters from the file are also the default parameters for the segmentation process and post-processing:

```yaml
pipeline:
  infer_size: 1024              # Tile size (in pixels) to feed the model. The size is of the scaled tiles, not the original tiles from dividing the input image.
  overlap_margin: 32            # Margin (in pixels) to overlap between tiles during inference to reduce edge artifacts. Also of the scaled tiles.
  n_postprocess_processes: 32   # Number of parallel processes used for post-processing
  postprocess_queue_size: 128   # Size of the queue to store model output before post-processing
  n_merge_tile_processes: 16    # Number of parallel processes used to merge tiles into the final output

postprocess:
  niter: 200                    # Number of iterations for following the flow
  cellprob_threshold: 0         # Threshold for the probability of a pixel being part of a cell (in logit; 0 corresponds to 0.5 probability)
  flow_threshold: 0.4           # Threshold for the flow magnitude to filter out low-confidence regions
  min_size: 15                  # Minimum size (in pixels) for objects to be considered as cells
  resample: false               # Whether to resample the output to match the original image size when postprocessing (false to keep the inferred size). When scale > 1, set to true will improve postprocessing performance
```

To see the full list of available options, use the `--help` flag.

```bash
turing_segment --help
```

## Feedback

If you encounter any issues or bugs while using Turing Segment, please let us know by submitting an issue on this GitHub repository.

For other feedback or support, you can reach out to our dedicated support team at [support@bioturing.com](mailto:support@bioturing.com).


