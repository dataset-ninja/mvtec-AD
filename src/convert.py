import glob
import os

import supervisely as sly
from cv2 import connectedComponents
from supervisely.io.fs import dir_exists, file_exists, get_file_ext, get_file_name


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "THE MVTEC AD"
    dataset_path = "APP_DATA/mvtec_anomaly_detection"
    batch_size = 30

    train_images_pathes = "train/good"
    test_images_pathes = "test"
    masks_pathes = "ground_truth"
    mask_suffix = "_mask"

    img_ext = ".png"

    def create_ann(image_path, defect_class_name):
        labels = []
        tag_names_ = []

        mask_name = get_file_name(image_path) + mask_suffix + img_ext
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]
        mask_path = os.path.join(masks_path, defect_class_name, mask_name)
        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            mask = mask_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                curr_label = sly.Label(curr_bitmap, defect_to_obj_class[defect_class_name])
                labels.append(curr_label)

        if "good" in image_path:
            tag_names_.append("good")
        tag_names_.append(image_path.split("/")[-4])

        tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name in tag_names_]

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    tag_names = [
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
        "good",
    ]
    tag_metas = [sly.TagMeta(name, sly.TagValueType.NONE) for name in tag_names]

    objects = os.listdir(dataset_path)
    defect_to_obj_class = {}

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(tag_metas=tag_metas)
    api.project.update_meta(project.id, meta.to_json())

    def count_images(base_directory, dir):
        folders = glob.glob(os.path.join(base_directory, f"**/{dir}"), recursive=True)
        file_count = 0
        for folder in folders:
            file_count += len(glob.glob(os.path.join(folder, "*")))
        return file_count

    for ds_name in ["test", "train"]:
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)
        progress = sly.Progress(
            "Create dataset {}".format(ds_name),
            count_images(dataset_path, ds_name),
        )
        for curr_object in objects:
            ds_path = os.path.join(dataset_path, curr_object, ds_name)
            if dir_exists(ds_path):
                for defect_class_name in os.listdir(ds_path):
                    if (
                        defect_class_name not in list(defect_to_obj_class.keys())
                        and defect_class_name != "good"
                    ):
                        new_obj_class = sly.ObjClass(defect_class_name, sly.Bitmap)
                        defect_to_obj_class[defect_class_name] = new_obj_class
                        meta = meta.add_obj_class(new_obj_class)
                        api.project.update_meta(project.id, meta.to_json())

                    images_path = os.path.join(ds_path, defect_class_name)
                    images_names = os.listdir(images_path)

                    for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                        images_pathes_batch = [
                            os.path.join(images_path, image_name) for image_name in img_names_batch
                        ]

                        new_img_names_batch = [
                            curr_object + "_" + defect_class_name + "_" + image_name
                            for image_name in img_names_batch
                        ]

                        anns_batch = [
                            create_ann(image_path, defect_class_name)
                            for image_path in images_pathes_batch
                        ]

                        img_infos = api.image.upload_paths(
                            dataset.id, new_img_names_batch, images_pathes_batch
                        )
                        img_ids = [im_info.id for im_info in img_infos]
                        api.annotation.upload_anns(img_ids, anns_batch)

                        progress.iters_done_report(len(img_names_batch))
    return project
