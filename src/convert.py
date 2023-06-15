import os
import supervisely as sly

from supervisely.io.fs import (    
    get_file_name,
    file_exists,
    dir_exists,
    get_file_ext,
)
from cv2 import connectedComponents


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = "MVTEC_AD"
    batch_size = 30

    train_images_pathes = "train/good"
    test_images_pathes = "test"
    masks_pathes = "ground_truth"
    mask_suffix = "_mask"


    def create_ann_train(image_path):
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        tag = sly.Tag(meta=tag_meta_train)

        return sly.Annotation(img_size=(img_height, img_wight), labels=[], img_tags=[tag])


    def create_ann_test(image_path):
        labels = []

        mask_name = get_file_name(image_path) + mask_suffix + get_file_ext(image_path)
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]
        mask_path = os.path.join(masks_path, curr_defect_name, mask_name)
        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            mask = mask_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                curr_label = sly.Label(curr_bitmap, defect_to_obj_class[curr_defect_name])
                labels.append(curr_label)

        tag = sly.Tag(meta=tag_meta_test)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[tag])


    tag_meta_train = sly.TagMeta("train", sly.TagValueType.NONE)
    tag_meta_test = sly.TagMeta("test", sly.TagValueType.NONE)

    all_datasets = os.listdir(dataset_path)
    defect_to_obj_class = {}

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(tag_metas=[tag_meta_train, tag_meta_test])
    api.project.update_meta(project.id, meta.to_json())

    for curr_dataset in all_datasets:
        ds_path = os.path.join(dataset_path, curr_dataset)
        if dir_exists(ds_path):
            dataset = api.dataset.create(project.id, curr_dataset, change_name_if_conflict=True)

            train_images_path = os.path.join(ds_path, train_images_pathes)
            train_images_names = os.listdir(train_images_path)
            progress = sly.Progress(
                "Create dataset {}, add train images".format(curr_dataset), len(train_images_names)
            )

            for img_names_batch in sly.batched(train_images_names, batch_size=batch_size):
                images_pathes_batch = [
                    os.path.join(train_images_path, image_name) for image_name in img_names_batch
                ]
                img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]
                anns_batch = [create_ann_train(image_path) for image_path in images_pathes_batch]
                api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(img_names_batch))

            test_image_path = os.path.join(ds_path, test_images_pathes)
            masks_path = os.path.join(ds_path, masks_pathes)

            for curr_defect_name in os.listdir(test_image_path):
                if (
                    curr_defect_name not in list(defect_to_obj_class.keys())
                    and curr_defect_name != "good"
                ):
                    new_obj_class = sly.ObjClass(curr_defect_name, sly.Bitmap)
                    defect_to_obj_class[curr_defect_name] = new_obj_class
                    meta = meta.add_obj_class(new_obj_class)
                    api.project.update_meta(project.id, meta.to_json())

                curr_test_images_path = os.path.join(test_image_path, curr_defect_name)
                curr_test_images_names = os.listdir(curr_test_images_path)
                progress = sly.Progress(
                    "Create dataset {}, add test images, defect {}".format(
                        curr_dataset, curr_defect_name
                    ),
                    len(curr_test_images_names),
                )

                for img_names_batch in sly.batched(curr_test_images_names, batch_size=batch_size):
                    images_pathes_batch = [
                        os.path.join(curr_test_images_path, image_name)
                        for image_name in img_names_batch
                    ]

                    new_img_names_batch = [
                        get_file_name(image_name) + "_" + curr_defect_name + get_file_ext(image_name)
                        for image_name in img_names_batch
                    ]

                    anns_batch = [create_ann_test(image_path) for image_path in images_pathes_batch]

                    img_infos = api.image.upload_paths(
                        dataset.id, new_img_names_batch, images_pathes_batch
                    )
                    img_ids = [im_info.id for im_info in img_infos]
                    api.annotation.upload_anns(img_ids, anns_batch)

                    progress.iters_done_report(len(img_names_batch))

    return project
