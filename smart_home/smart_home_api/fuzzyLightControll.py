import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import datetime

# INPUT_ILLUMINANCE = 54612

def fuzzy_controller(INPUT_ILLUMINANCE):
    # INPUT_ILLUMINANCE = 250
    INPUT_TIME = datetime.datetime.now().hour + (datetime.datetime.now().minute /60)
    # INPUT_TIME=12
    x_illuminance = np.arange(0, 54613, 1)
    x_timeOfDay = np.arange(0, 25, 1)
    x_outputIlluminance  = np.arange(0, 256, 1)

    qilluminance_v_lo = fuzz.trimf(x_illuminance, [0, 0, 13653])
    qilluminance_lo = fuzz.trimf(x_illuminance, [5461, 13653, 21844])
    qilluminance_md = fuzz.trimf(x_illuminance, [13653, 27306, 40959])
    qilluminance_hi = fuzz.trimf(x_illuminance, [32767, 40959, 49151])
    qilluminance_v_hi = fuzz.trimf(x_illuminance, [40959, 54612, 54612])

    timeOfDay_v_lo = fuzz.trapmf(x_timeOfDay, [0, 0, 5, 6])
    timeOfDay_lo = fuzz.trapmf(x_timeOfDay, [5, 6, 8, 9])
    timeOfDay_md = fuzz.trapmf(x_timeOfDay, [8, 9, 15, 16])
    timeOfDay_hi = fuzz.trapmf(x_timeOfDay, [15, 16, 17, 18])
    timeOfDay_v_hi = fuzz.trapmf(x_timeOfDay, [17, 18, 24, 24])

    output_qilluminance_off = fuzz.trimf(x_outputIlluminance, [0, 0, 0])
    output_qilluminance_v_lo = fuzz.trapmf(x_outputIlluminance, [0, 0, 20, 50])
    output_qilluminance_lo = fuzz.trimf(x_outputIlluminance, [20, 60, 100])
    output_qilluminance_md = fuzz.trapmf(x_outputIlluminance, [60, 100, 150, 190])
    output_qilluminance_hi = fuzz.trimf(x_outputIlluminance, [150, 190, 230])
    output_qilluminance_v_hi = fuzz.trapmf(x_outputIlluminance, [200, 230, 250, 250])

    # # Visualize these universes and membership functions
    # fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
    # ax0.plot(x_illuminance, qilluminance_v_lo, 'b', linewidth=1.5, label='Very low')
    # ax0.plot(x_illuminance, qilluminance_lo, 'b', linewidth=1.5, label='Low')
    # ax0.plot(x_illuminance, qilluminance_md, 'g', linewidth=1.5, label='Middle')
    # ax0.plot(x_illuminance, qilluminance_hi, 'r', linewidth=1.5, label='High')
    # ax0.plot(x_illuminance, qilluminance_v_hi, 'r', linewidth=1.5, label='Very High')
    # ax0.set_title('Illuminance')
    # ax0.legend()

    # ax1.plot(x_timeOfDay, timeOfDay_v_lo, 'b', linewidth=1.5, label='Night')
    # ax1.plot(x_timeOfDay, timeOfDay_lo, 'b', linewidth=1.5, label='Morning')
    # ax1.plot(x_timeOfDay, timeOfDay_md, 'g', linewidth=1.5, label='Day')
    # ax1.plot(x_timeOfDay, timeOfDay_hi, 'r', linewidth=1.5, label='Evening')
    # ax1.plot(x_timeOfDay, timeOfDay_v_hi, 'r', linewidth=1.5, label='Night')
    # ax1.set_title('Time of day')
    # ax1.legend()

    # ax2.plot(x_outputIlluminance, output_qilluminance_off, 'b', linewidth=1.5, label='OFF')
    # ax2.plot(x_outputIlluminance, output_qilluminance_v_lo, 'b', linewidth=1.5, label='Significantly decrease')
    # ax2.plot(x_outputIlluminance, output_qilluminance_lo, 'b', linewidth=1.5, label='Decrease')
    # ax2.plot(x_outputIlluminance, output_qilluminance_md, 'g', linewidth=1.5, label='Normal')
    # ax2.plot(x_outputIlluminance, output_qilluminance_hi, 'r', linewidth=1.5, label='Increase')
    # ax2.plot(x_outputIlluminance, output_qilluminance_v_hi, 'r', linewidth=1.5, label='Significantly increase')
    # ax2.set_title('Output Illuminance')
    # ax2.legend()
    # # Turn off top/right axes
    # for ax in (ax0, ax1, ax2):
    #     ax.spines['top'].set_visible(False)
    #     ax.spines['right'].set_visible(False)
    #     ax.get_xaxis().tick_bottom()
    #     ax.get_yaxis().tick_left()

    # plt.tight_layout()

    ill_level_v_lo = fuzz.interp_membership(x_illuminance, qilluminance_v_lo, INPUT_ILLUMINANCE[0])
    ill_level_lo = fuzz.interp_membership(x_illuminance, qilluminance_lo, INPUT_ILLUMINANCE[0])
    ill_level_md = fuzz.interp_membership(x_illuminance, qilluminance_md, INPUT_ILLUMINANCE[0])
    ill_level_hi = fuzz.interp_membership(x_illuminance, qilluminance_hi, INPUT_ILLUMINANCE[0])
    ill_level_v_hi = fuzz.interp_membership(x_illuminance, qilluminance_v_hi, INPUT_ILLUMINANCE[0])

    serv_level_v_lo = fuzz.interp_membership(x_timeOfDay, timeOfDay_v_lo, INPUT_TIME)
    serv_level_lo = fuzz.interp_membership(x_timeOfDay, timeOfDay_lo, INPUT_TIME)
    serv_level_md = fuzz.interp_membership(x_timeOfDay, timeOfDay_md, INPUT_TIME)
    serv_level_hi = fuzz.interp_membership(x_timeOfDay, timeOfDay_hi, INPUT_TIME)
    serv_level_v_hi = fuzz.interp_membership(x_timeOfDay, timeOfDay_v_hi, INPUT_TIME)

    # #morning & v l  
    rule1 = np.fmin(ill_level_v_lo, serv_level_v_lo)
    rule2 = np.fmin(ill_level_lo, serv_level_v_lo)
    rule3 = np.fmin(ill_level_md, serv_level_v_lo)
    rule4 = np.fmin(ill_level_hi, serv_level_v_lo)
    rule5 = np.fmin(ill_level_v_hi, serv_level_v_lo)

    rule6 = np.fmin(ill_level_v_lo, serv_level_lo)
    rule7 = np.fmin(ill_level_lo, serv_level_lo)
    rule8 = np.fmin(ill_level_md, serv_level_lo)
    rule9 = np.fmin(ill_level_hi, serv_level_lo)
    rule10 = np.fmin(ill_level_v_hi, serv_level_lo)

    rule11 = np.fmin(ill_level_v_lo, serv_level_md)
    rule12 = np.fmin(ill_level_lo, serv_level_md)
    rule13 = np.fmin(ill_level_md, serv_level_md)
    rule14 = np.fmin(ill_level_hi, serv_level_md)
    rule15 = np.fmin(ill_level_v_hi, serv_level_md)

    rule16 = np.fmin(ill_level_v_lo, serv_level_v_hi)
    rule17 = np.fmin(ill_level_lo, serv_level_v_hi)
    rule18 = np.fmin(ill_level_md, serv_level_v_hi)
    rule19 = np.fmin(ill_level_hi, serv_level_v_hi)
    rule20 = np.fmin(ill_level_v_hi, serv_level_v_hi)

    actovation_rule1 = np.fmin(rule1, output_qilluminance_off)
    actovation_rule2 = np.fmin(rule2, output_qilluminance_off)
    actovation_rule3 = np.fmin(rule3, output_qilluminance_off)
    actovation_rule4 = np.fmin(rule4, output_qilluminance_v_lo)
    actovation_rule5 = np.fmin(rule5, output_qilluminance_v_lo)

    actovation_rule6 = np.fmin(rule6, output_qilluminance_md)
    actovation_rule7 = np.fmin(rule7, output_qilluminance_md)
    actovation_rule8 = np.fmin(rule8, output_qilluminance_lo)
    actovation_rule9 = np.fmin(rule9, output_qilluminance_v_lo)
    actovation_rule10 = np.fmin(rule10, output_qilluminance_v_lo)

    actovation_rule11 = np.fmin(rule11, output_qilluminance_v_hi)
    actovation_rule12 = np.fmin(rule12, output_qilluminance_hi)
    actovation_rule13 = np.fmin(rule13, output_qilluminance_md)
    actovation_rule14 = np.fmin(rule14, output_qilluminance_lo)
    actovation_rule15 = np.fmin(rule15, output_qilluminance_v_lo)

    actovation_rule16 = np.fmin(rule16, output_qilluminance_md)
    actovation_rule17 = np.fmin(rule17, output_qilluminance_md)
    actovation_rule18 = np.fmin(rule18, output_qilluminance_lo)
    actovation_rule19 = np.fmin(rule19, output_qilluminance_v_lo)
    actovation_rule20 = np.fmin(rule20, output_qilluminance_v_lo)
    aggregated1 = np.fmax(
        np.fmax(actovation_rule1, actovation_rule2),
        np.fmax(actovation_rule3, actovation_rule4),
        )
    aggregated2 = np.fmax( np.fmax(actovation_rule5, actovation_rule6),
        np.fmax(actovation_rule7, actovation_rule8),
    )
    aggregated3 = np.fmax( np.fmax(actovation_rule9, actovation_rule10),
        np.fmax(actovation_rule11, actovation_rule12),
        )
    aggregated4 = np.fmax(np.fmax(actovation_rule13, actovation_rule14),
        np.fmax(actovation_rule15, actovation_rule16),
        )
    aggregated5= np.fmax(np.fmax(actovation_rule17, actovation_rule18),
        np.fmax(actovation_rule19, actovation_rule12),)

    aggregated = np.fmax(np.fmax(aggregated1, aggregated2), np.fmax(aggregated3, np.fmax(aggregated4, aggregated5)))
    # print(aggregated)
    result_centroid = fuzz.defuzz(x_outputIlluminance, aggregated, 'centroid')
    # tip_bisector = fuzz.defuzz(x_outputIlluminance, aggregated, 'bisector')
    # tip_mom = fuzz.defuzz(x_outputIlluminance, aggregated, "mom")
    # tip_som = fuzz.defuzz(x_outputIlluminance, aggregated, "som")
    # tip_lom = fuzz.defuzz(x_outputIlluminance, aggregated, "lom")

    # print(tip_centroid)
    # print(tip_bisector)
    # print(tip_mom)
    # print(tip_som)
    # print(tip_lom)
    return result_centroid

# fuzzy_controller(50000)