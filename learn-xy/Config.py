# Cross Validation Learner Configuration

### Packet Details ###
PKT_HZ = 4700  # pps (packets-per-second)
PKT_COLUMNS = 90  # Get first {PKT_COLUMNS} columns of each packet data
WINDOW_SIZE = int(PKT_HZ * 0.4)  # How many packets in one detection; depends on pps and the length of time of the action
SLIDE_SIZE = int(WINDOW_SIZE / 10)  # Packet interval in learning (Window-making interval)
THRESHOLD = 85  # If specific action continues after [WINDOW_SIZE * THRESHOLD / 100], that window will be recognized as that action

### Actions ###
ACTIONS = ["enh1", "enh2", "syncope", "noa", "walking"]

### Learning Parameters ###
LEARNING_RATE = 0.0001
N_ITERATIONS = 512  # epoch
BATCH_SIZE = 64

### Learning Details ###
KFOLD = 5
N_SKIPROW = 0
N_INPUT = PKT_COLUMNS  # (Fixed) WiFi activity data input (img shape: PKT_COLUMNS * WINDOW_SIZE)
N_HIDDEN = 720  # hidden layer num of features original 200
N_CLASSES = len(ACTIONS) + 1  # (Fixed) All actions + "No Activity"
N_VALID_CLASSES = len(ACTIONS)  # (Fixed) All actions
USE_NOACTIVITY = False  # Set "True" will include NoActivity windows in learning
USE_CUSTOM_NOACTIVITY = True  # Custom NoActivity (Not 0)
CUSTOM_NOACTIVITY_NO = 3  # Index number of custom NoActivity action (0 to len(ACTIONS) - 1)

### Path ###
SOURCE_DIR = "./Dataset/"
MERGED_DIR = "./Input_WINDOW{0}_COL{1}_TH{2}/"
SOURCE_PATH = SOURCE_DIR + "{0}_{1}*.csv"
MERGED_PATH = MERGED_DIR + "{3}_{4}.csv"
OUTPUT_PATH = "./Output_LR{0}_BATCH{1}_HIDDEN{2}/{3}"
LOG_PATH = "./Log_LR{0}_BATCH{1}_HIDDEN{2}/{3}"
