# Cross Valid Learner Configuration Store

PKT_HZ = 4000
PKT_COLUMNS = 90  # Get first {PKT_COLUMNS} columns of each packet data
WINDOW_SIZE = PKT_HZ  # How many packets in one detection
SLIDE_SIZE = int(PKT_HZ / 5)  # Packet interval in learning (Window-making interval)
THRESHOLD = 60  # If specific action continues after [WINDOW_SIZE * THRESHOLD / 100], that window will be recognized as that action

SOURCE_DIR = "./Dataset/"
MERGED_DIR = "./Input_WINDOW{0}_COL{1}_TH{2}/"
SOURCE_PATH = SOURCE_DIR + "{0}_{1}*.csv"
MERGED_PATH = MERGED_DIR + "{3}_{4}.csv"
OUTPUT_PATH = "./Output_LR{0}_BATCH{1}_HIDDEN{2}/{3}"
LOG_PATH = "./Log_LR{0}_BATCH{1}_HIDDEN{2}/{3}"

ACTIONS = ["sitdown"]

LEARNING_RATE = 0.0001
N_ITERATIONS = 2000  # epoch
BATCH_SIZE = 64

KFOLD = 10
N_SKIPROW = 0
N_INPUT = PKT_COLUMNS  # WiFi activity data input (img shape: 90 * WINDOW_SIZE)
N_STEPS = WINDOW_SIZE  # timesteps
N_HIDDEN = 200  # hidden layer num of features original 200
N_CLASSES = len(ACTIONS) + 1
N_VALID_CLASSES = len(ACTIONS)  # WiFi activity total classes
