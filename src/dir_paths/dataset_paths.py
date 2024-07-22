#1. DATASET PATHS

dorsal_and_ventral_paths ={
    'no_acuity_white_background' :'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_WHITE/',
    'no_acuity' :'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background/',
    'heliconius_male_behavioral_acuity' : '/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity/',
    'heliconius_female_behavioral_acuity' :'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity/',
    'heliconius_male_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity/',
    'heliconius_female_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity/',
    'kingfisher_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_kingfisher_acuity/'
}

dorsal_paths ={
    'no_acuity_white_background' :'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_WHITE_dorsal/',
    'no_acuity' :'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_dorsal/',
    'heliconius_male_behavioral_acuity' : '/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal/',
    'heliconius_female_behavioral_acuity' :'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal/',
    'heliconius_male_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal/',
    'heliconius_female_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal/',
    'kingfisher_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal/'
}

def get_image_dataset_path(acuity, high_res=False, include_ventral=False):
    if include_ventral:
        if high_res:
            dorsal_and_ventral_paths[acuity].replace('_256_256_removed_background', '')
        else:
            return dorsal_and_ventral_paths[acuity]
    else:
        if high_res:
            return dorsal_paths[acuity].replace('_256_256_removed_background', '')
        else:
            return dorsal_paths[acuity]



