import os
import shutil

import keras.callbacks as kc
import keras.optimizers as ko
import keras.utils as ku
import numpy as np
import sklearn.utils as sku

import Config as conf
import CSV as csv
from DenseNet import DenseNet

# Import & shuffle CSV data
xs, ys = csv.getCSV()
for a in conf.ACTIONS:
    xs[a], ys[a] = sku.shuffle(xs[a], ys[a], random_state=0)

# Setup Keras DenseNet Model (DenseNet-BC)
nadam = ko.Nadam(lr=conf.LEARNING_RATE)
model = DenseNet(
    input_shape=(conf.WINDOW_SIZE, conf.N_COLUMNS, 1),
    dense_blocks=5,
    growth_rate=conf.N_FILTERS,
    nb_classes=conf.N_VALID_CLASSES,
    dropout_rate=0.2,
    bottleneck=True,
    compression=0.5,
    weight_decay=1e-4,
    depth=conf.DEPTH
).build_model()
model.compile(
    loss="categorical_crossentropy", optimizer=nadam, metrics=["accuracy"])

# Check output directory and prepare tensorboard
outputDir = conf.OUTPUT_PATH.format(conf.LEARNING_RATE, conf.BATCH_SIZE,
                                    conf.N_FILTERS, "")
if os.path.exists(outputDir):
    shutil.rmtree(outputDir)
os.makedirs(outputDir)
logDir = conf.LOG_PATH.format(conf.LEARNING_RATE, conf.BATCH_SIZE,
                              conf.N_FILTERS, "")
if os.path.exists(logDir):
    shutil.rmtree(logDir)
os.makedirs(logDir)
tensorboard = kc.TensorBoard(
    log_dir=logDir,
    histogram_freq=0,
    batch_size=conf.BATCH_SIZE,
    write_graph=True,
    write_grads=True,
    write_images=True,
    update_freq=10)
print(
    "If you have tensorboard in this environment, you can type below to see the result in tensorboard:"
)
print("    tensorboard --logdir=" + logDir)
print("Keras checkpoints and final result will be saved in here:")
print("    " + outputDir)

# Run KFold
for i in range(conf.KFOLD):
    # Roll the data
    for a in conf.ACTIONS:
        xs[a] = np.roll(xs[a], int(len(xs[a]) / conf.KFOLD), axis=0)
        ys[a] = np.roll(ys[a], int(len(ys[a]) / conf.KFOLD), axis=0)

    # Data separation
    xTrain = []
    yTrain = []
    xEval = []
    yEval = []
    for a in conf.ACTIONS:
        if xTrain == []:
            xTrain = xs[a][int(len(xs[a]) / conf.KFOLD):]
        else:
            xTrain = np.r_[xTrain, xs[a][int(len(xs[a]) / conf.KFOLD):]]
        if yTrain == []:
            yTrain = ys[a][int(len(ys[a]) / conf.KFOLD):]
        else:
            yTrain = np.r_[yTrain, ys[a][int(len(ys[a]) / conf.KFOLD):]]
        if xEval == []:
            xEval = xs[a][:int(len(xs[a]) / conf.KFOLD)]
        else:
            xEval = np.r_[xEval, xs[a][:int(len(xs[a]) / conf.KFOLD)]]
        if yEval == []:
            yEval = ys[a][:int(len(ys[a]) / conf.KFOLD)]
        else:
            yEval = np.r_[yEval, ys[a][:int(len(ys[a]) / conf.KFOLD)]]

    if not conf.USE_NOACTIVITY:
        # Remove NoActivity from ys
        yTrain = yTrain[:, 1:]
        yEval = yEval[:, 1:]

        # If there exists only one action, convert Y to binary form
        if yEval.shape[1] == 1:
            yTrain = ku.to_categorical(yTrain)
            yEval = ku.to_categorical(yEval)

    # Setup Keras Checkpoint
    checkpoint = kc.ModelCheckpoint(
        outputDir + "Checkpoint_K" + str(i + 1) + "_EPOCH{epoch}_ACC{val_acc:.6f}.h5", period=conf.CP_PERIOD)

    # Fit model (learn)
    print(
        str(i + 1) + " th fitting started. Endpoint is " + str(conf.KFOLD) +
        " th.")

    model.fit(
        xTrain,
        yTrain,
        batch_size=conf.BATCH_SIZE,
        epochs=conf.N_EPOCH,
        verbose=1,
        callbacks=[tensorboard, checkpoint],
        validation_data=(xEval, yEval))  # , validation_freq=2)
print("Epoch completed!")

# Saving model
print("Saving model & model information...")
modelYML = model.to_yaml()
with open(outputDir + "model.yml", "w") as yml:
    yml.write(modelYML)
modelJSON = model.to_json()
with open(outputDir + "model.json", "w") as json:
    json.write(modelJSON)
model.save(outputDir + "model.h5")
print('Model saved! Congratulations! You finished all processes of ML!')
