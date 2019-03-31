# Cross Valid Learner Configuration Store

PKT_COLUMNS   = 90
WINDOW_SIZE   = 1000 # How many packets in one detection
SLIDE_SIZE    = 200 # Packet interval in learning (Window-making interval)
THRESHOLD     = 60 # If specific action continues after [WINDOW_SIZE * THRESHOLD / 100], that window will be recognized as that action

SOURCE_DIR    = "./Dataset/"
MERGED_DIR    = "./Input/"
SOURCE_PATH   = SOURCE_DIR + "{0}_{1}*.csv"
MERGED_PATH   = MERGED_DIR + "{0}_{1}.csv"
OUTPUT_PATH   = "./Output_LR{0}_BATCH{1}_NHIDDEN{2}/{3}"

ACTIONS       = ["sit_down", "stand_up", "to_bad", "to_good"]

LEARNING_RATE = 0.0001
N_ITERATIONS  = 2000
BATCH_SIZE    = 200
DISPLAY_STEP  = 100

N_INPUT = 90
N_STEPS = WINDOW_SIZE
N_HIDDEN = 200
N_CLASSES = len(ACTIONS) + 1
