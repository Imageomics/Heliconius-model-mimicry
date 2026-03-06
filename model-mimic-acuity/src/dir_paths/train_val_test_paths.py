#2. TRAIN/VAL/TEST SPLITS
'''These are all assumed to be dorsal only'''

regular_classification = {
    'no_acuity_white_background' : '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_WHITE_dorsal/',
    'no_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_dorsal/',
    'heliconius_male_behavioral_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal/',
    'heliconius_female_behavioral_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal/',
    'heliconius_male_morphological_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal/',
    'heliconius_female_morphological_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal/',
    'kingfisher_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal/'
}

erato_net = {
    'no_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/EratoNet/model_mimic_images_256_256_removed_background_dorsal/',
    'heliconius_male_behavioral_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/EratoNet/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal/',
    'heliconius_female_behavioral_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/EratoNet/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal/',
    'heliconius_male_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/EratoNet/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal/',
    'heliconius_female_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/EratoNet/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal/',
    'kingfisher_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/EratoNet/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal/'
}

melpomene_net = {
    'no_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MelpomeneNet/model_mimic_images_256_256_removed_background_dorsal/',
    'heliconius_male_behavioral_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MelpomeneNet/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal/',
    'heliconius_female_behavioral_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MelpomeneNet/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal/',
    'heliconius_male_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MelpomeneNet/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal/',
    'heliconius_female_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MelpomeneNet/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal/',
    'kingfisher_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MelpomeneNet/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal/'
}

mimics_net = {
    'no_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MimicsNet/model_mimic_images_256_256_removed_background_dorsal/',
    'heliconius_male_behavioral_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MimicsNet/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal/',
    'heliconius_female_behavioral_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MimicsNet/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal/',
    'heliconius_male_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MimicsNet/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal/',
    'heliconius_female_morphological_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MimicsNet/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal/',
    'kingfisher_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MimicsNet/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal/'
}

malleti_lativitta = {
    'no_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MalletiLativittaClassification/model_mimic_images_256_256_removed_background_dorsal/',
    'heliconius_male_behavioral_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MalletiLativittaClassification/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal/',
    'heliconius_female_behavioral_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MalletiLativittaClassification/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal/',
    'heliconius_male_morphological_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MalletiLativittaClassification/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal/',
    'heliconius_female_morphological_acuity': '/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MalletiLativittaClassification/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal/',
    'kingfisher_acuity':'/fs/ess/PAS2136/Butterfly/Model_Mimic/Data_Splits/MalletiLativittaClassification/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal/'

}

model_splits = {'RegularSpeciesClassification': regular_classification,
                'EratoNet': erato_net,
                'MelpomeneNet': melpomene_net,
                'MimicsNet': mimics_net,
                'MalletiLativitta': malleti_lativitta}

def get_split_csvs(acuity, model_name, high_res=False):
    if high_res:
        return model_splits[model_name][acuity].replace('_256_256_removed_background', '')
    return model_splits[model_name][acuity]