# Turing Segment: Quick Start

## Data Preparation
1. We can download the sample image with name `mosaic_DAPI_z{z_index}.tif` from official [Vizgen website](https://console.cloud.google.com/storage/browser/vz-ffpe-showcase/HumanUterineCancerPatient2-RACostain/images;tab=objects?prefix=&forceOnObjectsSortingFiltering=false).
2. If we want to segment multiple images, we must download at least 2 images.  
3. After download the data, we have the folder with the following structure:

    ```
    vizgen_images/
    ├── mosaic_DAPI_z0.tif
    ├── mosaic_DAPI_z1.tif
    ├── ...
    └── mosaic_DAPI_z6.tif
    ```
4. We can create folder for storing the results, or we can s the folder is not existed, the tool will auto create the folder if not existed.

*_Note_:* If we want to segment image with difference type, we must change the `--image-type` flag to the correct type. The tool supports `tiff`, `zarr` and `cv2` image types.

## Segmentation

### Single Image Segmentation

```bash
turing_segment infer \
--image-path vizgen_images/mosaic_DAPI_z0.tif \
--image-type tiff \
--output-dir vizgen_single_image_results/ \
--channels 0,1
```
The output folder `vizgen_single_image_results` will contain the segmentation results with the following structure:
```
vizgen_single_image_results/
├── metadata.json
└── polygons.parquet
```

### Multiple Images Segmentation

```bash
turing_segment infer \
--image-dir vizgen_images/ \
--image-type tiff \
--output-dir vizgen_multiple_image_results/ \
--channels 0,1
```
The output folder `vizgen_multiple_image_results` will contain the segmentation results for each image with the following structure:
```
vizgen_multiple_image_results/
├── configs.yml
├── mosaic_DAPI_z0/
│   ├── metadata.json
│   └── polygons.parquet
├── mosaic_DAPI_z1/
│   ├── metadata.json
│   └── polygons.parquet
├── ...
│
└── mosaic_DAPI_z6/
    ├── metadata.json
    └── polygons.parquet
```

## Draw Mask from Polygons

After segmentation, we can draw the mask from the polygons with the following command:

```bash
turing_segment poly2mask vizgen_single_image_results/ \
--output-dir vizgen_single_image_results/ 
```

We can change the `mask-shape` in the file `metadata.json` in the same folder with the polygons file.
If the `metadata.json` is not found, the tool will default the mask shape as max of the polygons coordinates.

After running the command, we have the output folder with the following structure:
```
vizgen_single_image_results/
├── metadata.json
├── polygons.parquet
└── mask.zarr
```

## 3D Stitching

We must change the `z_index` in the `configs.yml` file to indicate the z-index of the image before running the 3D stitching.

Example of `configs.yml` after changing the `z_index`:
```yaml
stitch:
- image_name: mosaic_DAPI_z0
  z_index: 0
- image_name: mosaic_DAPI_z0
  z_index: 1
- ...
- image_name: mosaic_DAPI_z6
  z_index: 6
```

After preparing the `configs.yml`, we can run the following command to stitch the segmentation results:

```bash 
turing_segment stitch vizgen_multiple_image_results/ \
--output-dir vizgen_multiple_image_results/ \
--num-process 16 \
--iou-threshold 0.5
```
*_Note:_* Increase the `--num-process` flag to run faster. If the flag is not provided, the tool will run in default 8 processes.

After running the command, we have the output folder with the following structure:

```
vizgen_multiple_image_results/
├── configs.yml
├── mosaic_DAPI_z0/
│   ├── metadata.json
│   └── polygons.parquet
├── mosaic_DAPI_z1/
│   ├── metadata.json
│   └── polygons.parquet
├── ...
├── mosaic_DAPI_z6/
│   ├── metadata.json
│   └── polygons.parquet
└── 3d_polygons.parquet
```


We can read the `3d_polygons.parquet` by using the `geopandas` library to get the 3D segmentation results.
``` python
import geopandas as gpd
data = gpd.read_parquet("vizgen_multiple_image_results/3d_polygons.parquet")
print(data)
#                                                geometry  z_index  cell_id
# 0     MULTIPOLYGON (((64 38, 62 40, 60 40, 58 41, 56...        0        1
# 1     MULTIPOLYGON (((135 45, 133 47, 129 47, 127 49...        0        2
# 2     MULTIPOLYGON (((96 94, 92 97, 90 97, 88 99, 88...        0        3
# 3     MULTIPOLYGON (((677 114, 675 116, 671 116, 669...        0        4
# 4     MULTIPOLYGON (((1545 97, 1543 99, 1540 99, 153...        0        5
# ...      

```