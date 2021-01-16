import matplotlib.pyplot as plt
import numpy as np


def plot_predictions_with_img(i, predictions, labels, img, named_labels=None, grayscale=False):
    predictions, labels, img = predictions[i], labels[i], img[i]
    predicted_label = np.argmax(predictions)
    true_value = np.argmax(labels)

    if not named_labels:
        named_labels = np.arange(len(labels))

    fig = plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)

    plt.yticks(np.arange(len(labels)), named_labels)
    thisplot = plt.barh(range(len(predictions)), predictions, color="gray")
    thisplot[predicted_label].set_color('r')
    thisplot[true_value].set_color('g')

    plt.subplot(1, 2, 2)

    if grayscale:
        plt.imshow(np.squeeze(img), cmap='gray')
    else:
        plt.imshow(img)
    plt.xlabel("Predicted: {} {:2.0f}% (Real: {})".format(named_labels[predicted_label], 100 * np.max(predictions),
                                                          named_labels[true_value]))
    plt.show()
    return fig


# grayscale only
def plot_gray_img_with_histogram(img, figsize=(10, 5), brightness_range=(0, 255)):
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])

    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    ax1.plot(cdf_normalized, color='b')
    ax1.hist(img.flatten(), 256, [0, 256], color='r')
    ax1.set_xlim([0, 256])

    vmin, vmax = brightness_range
    ax2.imshow(img, cmap='gray', vmin=vmin, vmax=vmax)
    return fig