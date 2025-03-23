from typing import Annotated

import numpy as np
import typer
from keras import Sequential
from keras.src.layers import Dense

np.random.seed()


def main(features: str, labels: str, seed: Annotated[int, typer.Option("-s")] = 123):
    np.random.seed(seed)
    x = np.load(features)
    y = np.load(labels)
    samples = x.shape[0]
    board_size = 9 * 9

    x = x.reshape(samples, board_size)
    y = y.reshape(samples, board_size)

    train_samples = int(0.9 * samples)
    x_train, x_test = x[:train_samples], x[train_samples:]
    y_train, y_test = y[:train_samples], y[train_samples:]

    model = Sequential()
    model.add(Dense(1000, activation="sigmoid", input_shape=(board_size,)))
    model.add(Dense(500, activation="sigmoid"))
    model.add(Dense(board_size, activation="sigmoid"))
    model.summary()

    model.compile(loss="mean_squared_error", optimizer="sgd", metrics=["accuracy"])

    model.fit(
        x_train,
        y_train,
        batch_size=64,
        epochs=15,
        verbose=1,
        validation_data=(x_test, y_test),
    )

    score = model.evaluate(x_test, y_test, verbose=0)
    print("Test loss:", score[0])
    print("Test accuracy:", score[1])
    
    
    test_board = np.array([[
        0, 0,  0,  0,  0, 0, 0, 0, 0,
        0, 0,  0,  0,  0, 0, 0, 0, 0,
        0, 0,  0,  0,  0, 0, 0, 0, 0,
        0, 1, -1,  1, -1, 0, 0, 0, 0,
        0, 1, -1,  1, -1, 0, 0, 0, 0,
        0, 0,  1, -1,  0, 0, 0, 0, 0,
        0, 0,  0,  0,  0, 0, 0, 0, 0,
        0, 0,  0,  0,  0, 0, 0, 0, 0,
        0, 0,  0,  0,  0, 0, 0, 0, 0,
    ]])
    
    move_probs = model.predict(test_board)[0]
    i = 0
    for row in range(9):
        row_formatted = []
        for col in range(9):
            row_formatted.append(f"{move_probs[i]:.3f}")
            i += 1
        print(" ".join(row_formatted))


if __name__ == "__main__":
    typer.run(main)
