import keras


def get_small_model(input_shape: tuple[int, int, int]):
    return keras.Sequential(
        [
            keras.layers.Input(input_shape),
            keras.layers.ZeroPadding2D(padding=3, data_format="channels_first"),
            keras.layers.Conv2D(48, (7, 7), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D(padding=2, data_format="channels_first"),
            keras.layers.Conv2D(32, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D(padding=2, data_format="channels_first"),
            keras.layers.Conv2D(32, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D(padding=2, data_format="channels_first"),
            keras.layers.Conv2D(32, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.Flatten(),
            keras.layers.Dense(512),
            keras.layers.Activation("relu"),
            keras.layers.Dense(361, activation="softmax"),
        ]
    )


def get_large_model(input_shape: tuple[int, int, int]):
    return keras.Sequential(
        [
            keras.layers.Input(input_shape),
            keras.layers.ZeroPadding2D((3, 3), data_format="channels_first"),
            keras.layers.Conv2D(
                64, (7, 7), padding="valid", data_format="channels_first"
            ),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D((2, 2), data_format="channels_first"),
            keras.layers.Conv2D(64, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D((2, 2), data_format="channels_first"),
            keras.layers.Conv2D(64, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D((2, 2), data_format="channels_first"),
            keras.layers.Conv2D(48, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D((2, 2), data_format="channels_first"),
            keras.layers.Conv2D(48, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D((2, 2), data_format="channels_first"),
            keras.layers.Conv2D(32, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.ZeroPadding2D((2, 2), data_format="channels_first"),
            keras.layers.Conv2D(32, (5, 5), data_format="channels_first"),
            keras.layers.Activation("relu"),
            keras.layers.Flatten(),
            keras.layers.Dense(1024),
            keras.layers.Activation("relu"),
            keras.layers.Dense(361, activation="softmax"),
        ]
    )
