import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split


def load_user_data(user_id):
    filename = f"user{user_id}.csv"
    df = pd.read_csv(filename)
    orders = df.iloc[:, 1:].values
    return orders


def generate_input_output_pairs(user_data, sequence_length):
    input_seqs = []
    output_seqs = []
    for i in range(len(user_data) - sequence_length):
        input_seq = np.array(user_data[i:i + sequence_length])
        output_seq = np.array(user_data[i + sequence_length])
        input_seqs.append(input_seq)
        output_seqs.append(output_seq)
    return np.array(input_seqs), np.array(output_seqs)


def build_lstm_model(input_shape, lstm_units=64, dropout_rate=0.2):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(lstm_units, input_shape=input_shape, return_sequences=True),
        tf.keras.layers.Dropout(dropout_rate),
        tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(1, activation='sigmoid'))
    ])
    return model


def train_model(model, X_train, y_train, epochs=10, batch_size=32, validation_split=0.2):
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split)


def evaluate_model(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")


# Example usage
user_id = 1
sequence_length = 3  # Length of input sequences
user_data = load_user_data(user_id)
input_seqs, output_seqs = generate_input_output_pairs(user_data, sequence_length)

X_train, X_test, y_train, y_test = train_test_split(input_seqs, output_seqs, test_size=0.2, random_state=42)

input_shape = (X_train.shape[1], X_train.shape[2])  # Shape of input data (sequence_length, num_features)

model = build_lstm_model(input_shape)
train_model(model, X_train, y_train)
evaluate_model(model, X_test, y_test)
