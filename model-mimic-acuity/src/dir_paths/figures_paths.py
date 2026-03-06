
regular_classification = {
'no_acuity_white_background' : '/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_WHITE_dorsal',
'no_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_dorsal",
'heliconius_male_behavioral_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal",
'heliconius_female_behavioral_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal",
'heliconius_male_morphological_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal",
'heliconius_female_morphological_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal",
'kingfisher_acuity':"/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/RegularSpeciesClassification/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal"
}

erato_net = {
'no_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/EratoNet/model_mimic_images_256_256_removed_background_dorsal",
'heliconius_male_behavioral_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/EratoNet/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal",
'heliconius_female_behavioral_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/EratoNet/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal",
'heliconius_male_morphological_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/EratoNet/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal",
'heliconius_female_morphological_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/EratoNet/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal",
'kingfisher_acuity':"/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/EratoNet/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal"
}

melpomene_net = {
'no_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MelpomeneNet/model_mimic_images_256_256_removed_background_dorsal",
'heliconius_male_behavioral_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MelpomeneNet/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal",
'heliconius_female_behavioral_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MelpomeneNet/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal",
'heliconius_male_morphological_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MelpomeneNet/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal",
'heliconius_female_morphological_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MelpomeneNet/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal",
'kingfisher_acuity':"/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MelpomeneNet/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal"
}

mimics_net = {
'no_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MimicsNet/model_mimic_images_256_256_removed_background_dorsal",
'heliconius_male_behavioral_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MimicsNet/model_mimic_images_256_256_removed_background_heliconius_male_behavioral_acuity_dorsal",
'heliconius_female_behavioral_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MimicsNet/model_mimic_images_256_256_removed_background_heliconius_female_behavioral_acuity_dorsal",
'heliconius_male_morphological_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MimicsNet/model_mimic_images_256_256_removed_background_heliconius_male_morphological_acuity_dorsal",
'heliconius_female_morphological_acuity': "/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MimicsNet/model_mimic_images_256_256_removed_background_heliconius_female_morphological_acuity_dorsal",
'kingfisher_acuity':"/fs/ess/PAS2136/Butterfly/Model_Mimic/Figures/MimicsNet/model_mimic_images_256_256_removed_background_kingfisher_acuity_dorsal"
}

model_figure_paths = {'RegularSpeciesClassification': regular_classification,
                      'EratoNet': erato_net,
                      'MelpomeneNet': melpomene_net,
                      'MimicsNet': mimics_net
                    }

def get_figures_path(acuity, model_name):
    return model_figure_paths[model_name][acuity]