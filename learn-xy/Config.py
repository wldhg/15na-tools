# Cross Validation Learner Configuration

### Packet Details ###
PKT_HZ = 4000  # pps (packets-per-second)
PKT_COLUMNS = 90  # Get first {PKT_COLUMNS} columns of each packet data
WINDOW_SIZE = int(PKT_HZ * 0.5)  # How many packets in one detection; depends on pps and the length of time of the action
SLIDE_SIZE = int(WINDOW_SIZE / 5)  # Packet interval in learning (Window-making interval)
THRESHOLD = 60  # If specific action continues after [WINDOW_SIZE * THRESHOLD / 100], that window will be recognized as that action

### Actions ###
ACTIONS = ["sitdown", "standup", "tobad-a", "tobad-b", "togood-a", "togood-b"]

### Learning Parameters ###
LEARNING_RATE = 0.0001
N_ITERATIONS = 352  # epoch
BATCH_SIZE = 64

### Learning Details ###
KFOLD = 7
N_SKIPROW = 4
N_INPUT = PKT_COLUMNS  # (Fixed) WiFi activity data input (img shape: PKT_COLUMNS * WINDOW_SIZE)
N_STEPS = 500  # (Fixed) timesteps
N_HIDDEN = 540  # hidden layer num of features original 200
N_CLASSES = len(ACTIONS) + 1  # (Fixed) All actions + "No Activity"
N_VALID_CLASSES = len(ACTIONS)  # (Fixed) All actions
USE_NOACTIVITY = False  # Set "True" will include NoActivity windows in learning

### Path ###
SOURCE_DIR = "./Dataset/"
MERGED_DIR = "./Input_WINDOW{0}_COL{1}_TH{2}/"
SOURCE_PATH = SOURCE_DIR + "{0}_{1}*.csv"
MERGED_PATH = MERGED_DIR + "{3}_{4}.csv"
OUTPUT_PATH = "./Output_LR{0}_BATCH{1}_HIDDEN{2}/{3}"
LOG_PATH = "./Log_LR{0}_BATCH{1}_HIDDEN{2}/{3}"
