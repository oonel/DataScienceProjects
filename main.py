import pandas as pd
import boto3
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns



def download_data_from_s3(bucket_name: str, file_key: str) -> pd.DataFrame:
    """
    Download a CSV file from an S3 bucket and load it into a DataFrame.

    Args:
    - bucket_name (str): The name of the S3 bucket.
    - file_key (str): The key (file path) of the file in the S3 bucket.

    Returns:
    - pd.DataFrame: A Pandas DataFrame with the loaded data.
    """
    # Initialize a boto3 S3 client
    s3 = boto3.client("s3")

    try:
        # Get the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)

        # Read the CSV content from the body of the response
        csv_content = response["Body"].read().decode("utf-8")

        # Use StringIO to convert the CSV content into a Pandas DataFrame
        data = pd.read_csv(StringIO(csv_content))

        return data

    except Exception as e:
        print("""There is no actual data on S3- this is just for illustrative purposes.
              Read from space_mission_data.csv instead if you wish to test the code.""")
        return None


# Perform exploratory data analysis
def exploratory_data_analysis(df: pd.DataFrame) -> None:
    """
    Generate some exploratory data visualizations.

    Args:
    - df (pd.DataFrame): The dataset to analyze.
    """
    # Plot distribution of each numerical column
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        plt.show()

    # Create a pairplot for the numerical features
    sns.pairplot(df.select_dtypes(include=["int64", "float64"]))
    plt.suptitle("Pairplot of Numerical Features", y=1.02)
    plt.show()


# Summarize basic statistics of the dataset
def summarize_data(df: pd.DataFrame) -> None:
    """
    Print basic summary statistics of the dataset.

    Args:
    - df (pd.DataFrame): The dataset to summarize.
    """
    print("Data Summary:")
    print(df.describe())


def main() -> None:
    """
    Main function to download, visualize, and summarize data.
    """
    # Mock S3 bucket and file path
    bucket_name = "space-missions-dataset"
    file_key = "space_mission_data.csv"

    df = download_data_from_s3(bucket_name, file_key)

    if df is not None:
        # Summarize data
        summarize_data(df)

        # Perform exploratory data analysis
        exploratory_data_analysis(df)


if __name__ == "__main__":
    main()
