import argparse
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_file(filename: str) -> pd.DataFrame:
    with open(filename, 'r') as f:
        df = pd.read_csv(f)
    return df

def prepare_dataset(df: pd.DataFrame) -> tuple:
    df_train = df.drop(["price", "index"], axis=1)
    target = df.price
    X_train, X_test, y_train, y_test = train_test_split(df_train, target, test_size=0.2, random_state=118)
    return X_train, X_test, y_train, y_test

def serialize_model(model, dv, filepath: str) -> None:
    with open(filepath, "wb") as f:
        pickle.dump((model, dv), f)
    
    logging.info(f"Model and DictVectorizer saved to {filepath}")
    
def main():
    parser = argparse.ArgumentParser(description="Train a model and save it.")
    parser.add_argument('-f', '--filename', type=str, default="./data/astana.csv", help="Path to the dataset file.")
    parser.add_argument('-o', '--output', type=str, default="./models/model.pkl", help="Path to save the trained model and DictVectorizer.")
    args = parser.parse_args()

    try:
        logging.info("Loading data...")
        df = load_file(args.filename)
    except FileNotFoundError:
        logging.error(f"File '{args.filename}' not found. Please provide a valid dataset path using the -f or --filename argument.")
        return  # Exit the function

    df.info()

    logging.info("Preparing dataset...")
    X_train, X_test, y_train, y_test  = prepare_dataset(df)
    logging.info(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")

    logging.info("Preparing DictVectorizer for categorical features...")
    dv = DictVectorizer(sparse=False)
    X_train_matrix = dv.fit_transform(X_train.to_dict(orient="records"))
    X_test_matrix = dv.transform(X_test.to_dict(orient="records"))

    logging.info("Training the model...")
    model = LinearRegression()
    model.fit(X_train_matrix, y_train)

    logging.info("Predicting on validation set...")
    y_test_pred = model.predict(X_test_matrix)

    logging.info("Calculating RMSE...")
    rmse = mean_squared_error(y_test, y_test_pred, squared=False)
    logging.info(f"Mean squared error: {round(rmse, 2)}")

    logging.info("Serializing model...")
    serialize_model(model, dv, args.output)

if __name__ == "__main__":
    main()
