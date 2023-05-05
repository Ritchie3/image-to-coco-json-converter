"""Script to convert RGB segmented mask to COCO format for use in CVAT."""
"""
1. create a project in CVAT and create the required labels. 

2. Copy the created label id's to this script:
    category_ids
    category_colors
    
2. select the folder with the mask png files.
    if the png file has colors that are not in the category_colors dict, the script will fail.
    if needed run the script 'colorize_mask_file.py' to build an image set with rgb masks.

3. run get_unique_colors_from_folder(folder_path) to get the colors in the masks.
    update the dict category_colors with the colors in the masks.

4. run the script

5. upload the images to CVAT in a new task

6. in the CVAT task, upload the annotations.json file as annotations

"""




import glob
import datetime
from src.create_annotations import *


licensesdict = [{"name": "Ritchie Heirmans",
                "id": 0,
                "url": "invilab.be"
                }]

infodict = {"contributor": "Ritchie",
            "date_created": str(datetime.date.today()),
            "description": "dataset annotated for Inspect4.0",
            "url": "invilab.be",
            "version": "1",
            "year": "2023"
            }

# Label ids of the dataset

category_ids = {'Dicht + onaanvaardbaar': 84,
                'Dicht + ernstig': 85,
                'Dicht + licht': 86,
                'Open + onaanvaardbaar': 87,
                'Open + ernstig': 88,
                'Open + licht': 89,
                'kettingfout': 90,
                'garenfout': 91,
                'plooi': 92}

# Define which colors match which categories in the images
category_colors = {
    "(0, 0, 0)": 84,
    "(255, 0, 0)": 85,
    "(255, 255, 0)": 86,
    "(128, 0, 255)": 87,
    "(255, 128, 0)": 88,
    "(0, 0, 255)": 89,
    "(128, 255, 255)":  90,
    "(0, 255, 0)":  91,
    "(128, 128, 128)": 92
}

# Define the ids that are a multiplolygon.
#multipolygon_ids = [0,1,2,3,4,5,6,7,8]
multipolygon_ids = []

# Get "images" and "annotations" info
def images_annotations_info(maskpath) -> (list, list):
    # This id will be automatically increased as we go
    annotation_id = 1
    image_id = 1
    annotations = []
    images = []

    for mask_image in glob.glob(maskpath + "*.png"):
        print(mask_image)
        # The mask image is *.png but the original image is *.jpg.
        # We make a reference to the original file in the COCO JSON file
        original_file_name = os.path.basename(mask_image).replace("_mask.png", ".jpg")
        # Open the image and (to be sure) we convert it to RGB
        mask_image_open = Image.open(mask_image).convert("RGB")
        w, h = mask_image_open.size

        # "images" info
        image = create_image_annotation(original_file_name, w, h, image_id)
        images.append(image)

        sub_masks = create_sub_masks(mask_image_open, w, h)
        for color, sub_mask in sub_masks.items():
            category_id = category_colors[color]

            # "annotations" info
            polygons, segmentations = create_sub_mask_annotation(sub_mask)

            # Check if we have classes that are a multipolygon
            if category_id in multipolygon_ids:
                # Combine the polygons to calculate the bounding box and area
                multi_poly = MultiPolygon(polygons)

                annotation = create_annotation_format(multi_poly, segmentations, image_id, category_id, annotation_id)

                annotations.append(annotation)
                annotation_id += 1
            else:
                for i in range(len(polygons)):
                    # Cleaner to recalculate this variable
                    segmentation = [np.array(polygons[i].exterior.coords).ravel().tolist()]

                    annotation = create_annotation_format(polygons[i], segmentation, image_id, category_id,
                                                          annotation_id)

                    annotations.append(annotation) # Add annotation to annotations list
                    annotation_id += 1
        image_id += 1
    return images, annotations, annotation_id


if __name__ == "__main__":


    if 0:
        "in case the data is split up in train/val/test folders:"
        coco_format = get_coco_json_format()
        for keyword in ["train", "val"]:
            mask_path = "dataset/{}_mask/".format(keyword)

            # Create category section
            coco_format["categories"] = create_category_annotation(category_ids)

            # Create images and annotations sections
            coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(mask_path)

            with open("output/{}.json".format(keyword), "w") as outfile:
                json.dump(coco_format, outfile)

            print("Created %d annotations for images in folder: %s" % (annotation_cnt, mask_path))

    if 1:
        "in case the data is in one folder:"
        # Get the standard COCO JSON format
        mask_path = r"C:\dataset_inspect40\picanol_sabrina_pro\full_size\masks_png_colorized/"

        # Get the standard COCO JSON format
        coco_format = get_coco_json_format()
        coco_format["licenses"] = licensesdict #add licences
        coco_format["info"] = infodict #add info
        coco_format["categories"] = create_category_annotation(category_ids) #add categories
        # Create images and annotations sections
        coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(mask_path)

        savepath = f"{mask_path}/masks.json"
        print(f'saving to {savepath}')
        with open(savepath, "w") as outfile:
            json.dump(coco_format, outfile)

        print("Created %d annotations for images in folder: %s" % (annotation_cnt, mask_path))

        print(f"{mask_path}/masks.json")


    if 0:
        "run on the test set with only 1 image:"

        mask_path = r"C:\dataset_inspect40\picanol_sabrina_pro\test\masks/"


        # Get the standard COCO JSON format
        coco_format = get_coco_json_format()
        coco_format["licenses"] = licensesdict #add licences
        coco_format["info"] = infodict #add info
        coco_format["categories"] = create_category_annotation(category_ids) #add categories
        # Create images and annotations sections
        coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(mask_path)

        savepath = f"{mask_path}/masks.json"
        print(f'saving to {savepath}')
        with open(savepath, "w") as outfile:
            json.dump(coco_format, outfile)

        print("Created %d annotations for images in folder: %s" % (annotation_cnt, mask_path))

        print(f"{mask_path}/masks.json")