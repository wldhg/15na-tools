# Cross Valid Learner Configuration Store

PKT_COLUMNS = 270  # Get first {PKT_COLUMNS} columns of each packet data
WINDOW_SIZE = 200  # How many packets in one detection
SLIDE_SIZE = 20  # Packet interval in learning (Window-making interval)
THRESHOLD = 12  # If specific action continues after [WINDOW_SIZE * THRESHOLD / 100], that window will be recognized as that action

SOURCE_DIR = "./Dataset/"
MERGED_DIR = "./Input_WINDOWSIZE{0}_COLUMN{1}/"
SOURCE_PATH = SOURCE_DIR + "{0}_{1}*.csv"
MERGED_PATH = MERGED_DIR + "{2}_{3}.csv"
OUTPUT_PATH = "./Output_LR{0}_BATCH{1}_NHIDDEN{2}/{3}"
LOG_PATH = "./Log_LR{0}_BATCH{1}_NHIDDEN{2}/{3}"

ACTIONS = ["sit_down", "stand_up", "to_bad", "to_good"]

LEARNING_RATE = 0.0001
N_ITERATIONS = 2000  # epoch
BATCH_SIZE = 64

KFOLD = 11
N_SKIPROW = 0
N_INPUT = PKT_COLUMNS  # WiFi activity data input (img shape: 90 * WINDOW_SIZE)
N_STEPS = WINDOW_SIZE  # timesteps
N_HIDDEN = 600  # hidden layer num of features original 200
N_CLASSES = len(ACTIONS) + 1
N_VALID_CLASSES = len(ACTIONS)  # WiFi activity total classes
