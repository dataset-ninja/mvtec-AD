from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "MVTec AD"
PROJECT_NAME_FULL: Optional[str] = "MVTec AD: the MVTec Anomaly Detection"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.BY_NC_SA_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [
    Domain.Industrial(is_used=False),
    Research.AnomalyDetection(),
]
CATEGORY: Category = Category.Manufacturing()

CV_TASKS: List[CVTask] = [CVTask.SemanticSegmentation(), CVTask.Classification()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.SemanticSegmentation()]

RELEASE_DATE: Optional[str] = "2019-06-20"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None
HOMEPAGE_URL: str = "https://www.mvtec.com/company/research/datasets/mvtec-ad"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 2340907
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/mvtec-AD"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[
    Union[str, dict]
] = "https://www.mvtec.com/company/research/datasets/mvtec-ad"
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "liquid": [230, 25, 75],
    "defective": [60, 180, 75],
    "broken_large": [255, 225, 25],
    "broken_small": [0, 130, 200],
    "glue_strip": [245, 130, 48],
    "gray_stroke": [145, 30, 180],
    "oil": [70, 240, 240],
    "flip": [240, 50, 230],
    "squeeze": [210, 245, 60],
    "scratch": [250, 190, 212],
    "faulty_imprint": [0, 128, 128],
    "contamination": [220, 190, 255],
    "pill_type": [170, 110, 40],
    "fold": [255, 250, 200],
    "poke": [128, 0, 0],
    "fabric_border": [170, 255, 195],
    "fabric_interior": [128, 128, 0],
    "rough": [255, 215, 180],
    "squeezed_teeth": [0, 0, 128],
    "broken_teeth": [128, 128, 128],
    "split_teeth": [230, 25, 75],
    "scratch_neck": [60, 180, 75],
    "thread_side": [255, 225, 25],
    "thread_top": [0, 130, 200],
    "scratch_head": [245, 130, 48],
    "manipulated_front": [145, 30, 180],
    "bent": [70, 240, 240],
    "broken": [240, 50, 230],
    "glue": [210, 245, 60],
    "thread": [250, 190, 212],
    "metal_contamination": [0, 128, 128],
    "color": [220, 190, 255],
    "crack": [170, 110, 40],
    "print": [255, 250, 200],
    "cut": [128, 0, 0],
    "hole": [170, 255, 195],
    "missing_wire": [128, 128, 0],
    "cut_outer_insulation": [255, 215, 180],
    "cable_swap": [0, 0, 128],
    "poke_insulation": [128, 128, 128],
    "missing_cable": [230, 25, 75],
    "cut_inner_insulation": [60, 180, 75],
    "combined": [255, 225, 25],
    "bent_wire": [0, 130, 200],
    "cut_lead": [245, 130, 48],
    "misplaced": [145, 30, 180],
    "damaged_case": [70, 240, 240],
    "bent_lead": [240, 50, 230],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

PAPER: Optional[str] = [
    "https://link.springer.com/article/10.1007/s11263-020-01400-4",
    "https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/company/research/datasets/mvtec_ad.pdf",
]
CITATION_URL: Optional[str] = "https://www.mvtec.com/company/research/datasets/mvtec-ad"
AUTHORS: Optional[List[str]] = [
    "Paul Bergmann",
    "Kilian Batzner",
    "Michael Fauser",
    "David Sattlegger",
    "Carsten Steger",
]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = "MVTec Software GmbH, Germany"
ORGANIZATION_URL: Optional[Union[str, List[str]]] = "http://www.mvtec.com/"
SLYTAGSPLIT: Optional[Dict[str, List[str]]] = {
    "categories": [
        "bottle",
        "cable",
        "capsule",
        "carpet",
        "grid",
        "hazelnut",
        "leather",
        "metal_nut",
        "pill",
        "screw",
        "tile",
        "toothbrush",
        "transistor",
        "wood",
        "zipper",
    ],
    "__POSTTEXT__": "Additionally, there are 4096 ***good*** images with no defects are provided for classification purposes",
}
TAGS: List[str] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "license": LICENSE,
        "hide_dataset": HIDE_DATASET,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["project_name_full"] = PROJECT_NAME_FULL or PROJECT_NAME
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    return settings
