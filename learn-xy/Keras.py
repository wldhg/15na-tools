import os
import shutil

import keras.callbacks as kc
import keras.layers as kl
import keras.models as km
import keras.optimizers as ko
import keras.utils as ku
import numpy as np
import sklearn as sk
import sklearn.utils as sku

import Config as conf
import Input_Data as data

# Check output directory
outputDir = conf.OUTPUT_PATH.format(conf.LEARNING_RATE, conf.BATCH_SIZE,
                                    conf.N_HIDDEN, "")
if os.path.exists(outputDir):
    shutil.rmtree(outputDir)
os.makedirs(outputDir)
logDir = conf.LOG_PATH.format(conf.LEARNING_RATE, conf.BATCH_SIZE,
                              conf.N_HIDDEN, "")
if os.path.exists(logDir):
    shutil.rmtree(logDir)
os.makedirs(logDir)

# Setup Keras Callbacks
tensorboard = kc.TensorBoard(
    log_dir=logDir,
    histogram_freq=10,
    batch_size=conf.BATCH_SIZE,
    write_graph=True,
    write_grads=True,
    write_images=True,
    update_freq=2)
print(
    "If you have tensorboard in this environment, you can type below to see the result in tensorboard:"
)
print("    tensorboard --logdir=" + logDir)

checkpoint = kc.ModelCheckpoint(conf.OUTPUT_PATH.format("Checkpoint_EPOCH{0}.h5"), period=20)
print(
    "Keras checkpoints and final result will be saved in here:"
)
print("    " + outputDir)

# Setup Keras RNN Model
lstm = kl.LSTM(
    conf.N_HIDDEN,
    unit_forget_bias=True,
    input_shape=(conf.N_STEPS, conf.N_INPUT))
lstm.add_loss(1e-8)
adam = ko.Adam(lr=conf.LEARNING_RATE, amsgrad=True)
model = km.Sequential()
model.add(lstm)
model.add(kl.Dense(conf.N_VALID_CLASSES, activation="softmax"))
model.compile(
    loss="categorical_crossentropy", optimizer=adam, metrics=["accuracy"])

# Import CSV data
xs, ys = data.importCSV()

# Shuffle data
for a in conf.ACTIONS:
    xs[a], ys[a] = sku.shuffle(xs[a], ys[a], random_state=0)

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

    # Remove NoActivity from ys
    yTrain = yTrain[:, 1:]
    yEval = yEval[:, 1:]

    print(
        str(i) + " th fitting started. Endpoint is " + str(conf.KFOLD) +
        " th.")

    model.fit(
        xTrain,
        yTrain,
        batch_size=conf.BATCH_SIZE,
        epochs=conf.N_ITERATIONS,
        verbose=1,
        callbacks=[tensorboard, checkpoint],
        validation_data=(xEval, yEval))  #, validation_freq=2)

print("Epoch completed! Saving model & weights...")
modelYML = model.to_yaml()
with open("model.yml", "w") as yml:
    yml.write(modelYML)
model.save_weights(outputDir + "model.h5")
print('Model saved! Congratulations! You finished all processes of ML!')
