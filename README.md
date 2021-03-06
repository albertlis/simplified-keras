# simplified keras
Common used actions in keras

## Table of contents
* [General info](#general-info)
* [Libraries](#libraries)
* [Setup](#setup)
* [Documentation](#documentation)
* [PyPi](#pypi)
* [TODO](#todo)
* [Development](#development)
* [Status](#status)
* [Contact](#contact)

## General info
This package is a set of common used actions in keras. At this moment includes (**may be outdated**):
- Main package
    * [Default callbacks](#default-callbacks)
    * [Restore callbacks](#restore-callbacks)
    * [Generators](#generators)
- Plots
    * [Accuracy and Loss plot](#accuracy-and-loss-plot)
    * [Predictions with image plot](#predictions-with-image-plot)
    * [Histogram with CDF and image plot](#histogram-with-cdf-and-image-plot)
    * [Confusion matrix](#confusion-matrix-plot)
- Metrics
    * [Confusion matrix](#confusion-matrix)
    * [Model Statistics](#model-statistics)
    * [Folder Statistics](#folder-statistics)
    * [Model memory usage](#model-memory-usage)
- Transformations
    * [Convert predictions to classes array](#convert-predictions-to-classes-array)
    * [Convert one hot encoding to sparse](#convert-one-hot-encoding-to-sparse)
    * [Unfreeze model](#unfreeze-model)
    * [Stretch histogram](#stretch-histogram)
    * [Normalize histogram clahe](#normalize-histogram-clahe) 
    * [Replace activations](#replace-activations)
    * [Layers](#layers)
  

## Libraries
- Matplotlib - version 3.3.3
- NumPy - version 1.19.4
- Tensorflow - version 2.4.1
- Pandas - version 1.1.5
- Seaborn - version 0.11.1

## Setup
* Install from PyPi: `pip install simplified-keras`

## Documentation

### Main package
#### Generators
###### default generators
```python
from keras.preprocessing.image import ImageDataGenerator
from simplified_keras.generators import get_train_val_generators, get_val_test_generators

img_size = (48, 48)
img_datagen = ImageDataGenerator(rescale=1/255)

# same for get_val_test_generators
# default: data_dir='../data', color_mode='rgb', batch_size=128, class_mode='categorical'
train_generator, validation_generator = get_train_val_generators(img_datagen, data_dir='../data/normal',
                                                                 color_mode='grayscale', target_size=img_size)
val_generator, test_generator = get_val_test_generators(img_datagen, batch_size=32)
```
###### numpy_memmap_generator
```python
from simplified_keras.generators import numpy_memmap_generator

# default batch_size=128, shuffle_array=True
train_gen = numpy_memmap_generator('imgs.npy', 'labels.npy', batch_size=64, shuffle_array=False)
```
### Default callbacks

```python
from simplified_keras.callbacks import get_default_callbacks

callbacks = get_default_callbacks('models/vgg16_calssifier.h5', monitor='val_loss', verbose=0)

hist = model.fit(train_generator, steps_per_epoch=train_steps, validation_data=validation_generator,
                 validation_steps=valid_steps, epochs=100, callbacks=callbacks, verbose=2)
```
Signature:

```python
def get_default_callbacks(model_path, monitor='val_acc', base_patience=3, lr_reduce_factor=0.5, min_lr=1e-7, verbose=1):
    return [
        ReduceLROnPlateau(monitor=monitor, factor=lr_reduce_factor, min_lr=min_lr, patience=base_patience, verbose=verbose),
        EarlyStopping(monitor=monitor, patience=(2 * base_patience + 1), verbose=verbose),
        ModelCheckpoint(monitor=monitor, filepath=model_path, save_best_only=True, verbose=verbose)
    ]
```

### Restore callbacks
Used to restore callback after paused learning. Model should come from last checkpoint.

```python
from simplified_keras.callbacks import restore_callbacks, get_default_callbacks

callbacks = get_default_callbacks('models/vgg16_calssifier.h5', monitor='val_loss', verbose=0)
acc, loss = model.evaluate(val_ds)

# acc or loss depending on the compiled model metrics
restore_callbacks(callbacks, acc)
```
### Plots
#### Accuracy and Loss plot

```python
from simplified_keras.plots.history_plots import plot_acc_and_loss

history = model.fit(train_gen, teps_per_epoch=train_steps, epochs=5, validation_data=val_gen, 
                    validation_steps=val_steps, callbacks=callbacks)

fig = plot_acc_and_loss(history)
```

Result:

[![history.png](https://i.postimg.cc/YqYgStNM/t.png)](https://postimg.cc/8jksKQn0)

#### Predictions with image plot

```python
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from simplified_keras.generators import get_train_val_generators
from simplified_keras.plots import plot_predictions_with_img

img_size = (48, 48)
img_datagen = ImageDataGenerator(rescale=1 / 255)

_, validation_generator = get_train_val_generators(img_datagen, data_dir='../data/normal',
                                                   color_mode='grayscale', target_size=img_size)
model = load_model('../models/standard_model.h5')

batch, labels = validation_generator.next()
preds = model.predict(batch)

named_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
fig = plot_predictions_with_img(1, preds, labels, batch, named_labels, grayscale=True)
```

Result:

[![p.png](https://i.postimg.cc/Hs2dD4Tw/p.png)](https://postimg.cc/ykkw0Rgx)

#### Histogram with CDF and image plot

```python
import cv2
from simplified_keras.plots import plot_gray_img_with_histogram

img = cv2.imread(f'{src_train_path}/0/241.png', 0)
fig1 = plot_gray_img_with_histogram(img)
img2 = stretch_histogram(img)
fig2 = plot_gray_img_with_histogram(img2)
```

Result:

[![history1.png](https://i.postimg.cc/JzwN3Pc3/h1.png)](https://i.postimg.cc/JzwN3Pc3/h1.png)
[![history2.png](https://i.postimg.cc/x1KK6Mtw/h2.png)](https://i.postimg.cc/x1KK6Mtw/h2.png)

#### Confusion matrix plot

```python
from simplified_keras.transformations import predictions_to_classes, one_hot_to_sparse
from simplified_keras.metrics import get_confusion_matrixes
from simplified_keras.plots import plot_confusion_matrix

predictions = model.predict(validation_images)
predicted_classes = predictions_to_classes(predictions)
sparse_labels = one_hot_to_sparse(validation_labels)

cm, cm_normalized = get_confusion_matrixes(predicted_classes, sparse_labels)
classes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
f1 = plot_confusion_matrix(cm, classes)
f2 = plot_confusion_matrix(cm_normalized, classes, figsize=(10, 8))
```
Results:

<p align="center">
  <img src = "https://i.postimg.cc/cC7hsXpz/cm.png" width=400>
  <img src = "https://i.postimg.cc/7PSmMZ5N/cm-normalized.png" width=400>
</p>

### Metrics

#### Confusion matrix

```python
from simplified_keras.transformations import predictions_to_classes, one_hot_to_sparse
from simplified_keras.metrics import get_confusion_matrixes

predictions = model.predict(validation_images)
predicted_classes = predictions_to_classes(predictions)
sparse_labels = one_hot_to_sparse(validation_labels)

# Returns two numpy arrays: standard and normalized
cm, cm_normalized = get_confusion_matrixes(predicted_classes, sparse_labels)
```

#### Model Statistics
Calculates:
- FP
- FN
- TP
- TN
- TPR # Sensitivity/true positive rate
- TNR # Specificity/true negative rate
- PPV # Precision/positive predictive value
- NPV # Negative predictive value
- FPR # Fall out or false positive rate
- FNR # False negative rate
- FDR # False discovery rate
- ACC # Overall accuracy for each class
- Much more and still increasing

```python
from simplified_keras.transformations import predictions_to_classes, one_hot_to_sparse
from simplified_keras.metrics import get_confusion_matrixes
from simplified_keras.metrics import get_model_statistics

predictions = model.predict(validation_images)
predicted_classes = predictions_to_classes(predictions)
sparse_labels = one_hot_to_sparse(validation_labels)

cm, cm_normalized = get_confusion_matrixes(predicted_classes, sparse_labels)

stats = get_model_statistics(cm)
classes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
fig = stats.visualize(classes)
print(stats.TN) #[2890 3530 2874 2361 2591 3000 2661]
```
Visualization:
[![stat-visualization.png](https://i.postimg.cc/bvpf9BT6/stat-visualization.png)](https://postimg.cc/w1fr6FnJ)

#### Folder statistics
```python
from simplified_keras.metrics import get_folders_statistics

stat = get_folders_statistics('../data/normal/train')
print(stat.nr_of_elements, stat.info) # 28709 {'0': 3995, '1': 436, '2': 4097, '3': 7215, '4': 4830, '5': 3171, '6': 4965}
fig = stat.bar_plot()
```
Result:

<img src="https://i.postimg.cc/yxFcXyvq/folder-stat1.png" alt="drawing" width="500"/>

#### Model memory usage
```python
from simplified_keras.metrics import get_model_memory_usage

batch_size = 64
# outputs usage in GB
usage = get_model_memory_usage(batch_size, model)
print(usage, 'GB') # 8.34 GB
```

### Transformations

#### Convert predictions to classes array

```python
from simplified_keras.transformations import predictions_to_classes

predictions = model.predict(validation_images)
predicted_classes = predictions_to_classes(predictions)
print(pedicted_classes) #[6 3 3 ... 6 2 0]
```

#### Convert one hot encoding to sparse

```python
from simplified_keras.transformations import one_hot_to_sparse

sparse_labels = one_hot_to_sparse(validation_labels)
print(sprase_labels) #[6 6 6 ... 6 2 0]
```
#### Stretch histogram
```python
from simplified_keras.transformations import stretch_histogram

# default color_mode='rgb'
stretch_histogram(image, color_mode='grayscale')
```

#### Unfreeze model
```python
from simplified_keras.transformations import unfreeze_model
from tensorflow.keras.optimizers import Adam

# default params: optimizer=Adam(learning_rate=1e-5), metrics="acc"
unfreeze_model(model, optimizer=Adam(learning_rate=1e-4), metrics="loss")
```

#### Normalize histogram clahe
```python
from simplified_keras.transformations import normalize_histogram_clahe

# default clip_limit=2.0, tile_grid_size=(8, 8), color_mode='rgb'
normalize_histogram_clahe(image)
```
#### Replace activations
Replaces all activation functions in given model
```python
from simplified_keras.transformations import replace_activations
from tensorflow.keras.layers import LeakyReLU

l_relu = LeakyReLU()
replace_activations(model, l_relu)
```
#### Layers
Augumentation layers build on tensorflow image operations

```python
from simplified_keras.transformations import RandomSaturation, RandomHue, RandomBrightness
from tensorflow.keras import Sequential

# for more informations about parameters see tf.image docs
augument_layers = Sequential([
  RandomSaturation(0.5, 1.5),
  # must be [0 - 0,5]
  RandomHue(0.2),
  RandomBrightness(0.2)
])
```

## PyPi
[simplified-keras](add-link)

## TODO
- Add tests and a lot of features :)

## Development
Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

* Fork the repo
* Create a new branch (`git checkout -b improve-feature`)
* Make the appropriate changes in the files
* **Verify if they are correct**
* Add changes to reflect the changes made
* Commit changes
* Push to the branch (`git push origin improve-feature`)
* Create a Pull Request

## Status
Library is: _in progress_

## Contact
albert.lis.1996@gmail.com - feel free to contact me!
