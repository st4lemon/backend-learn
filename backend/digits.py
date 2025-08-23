import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split

def load_digits_data(filename: str | None = None):
    if filename:
        # Load custom dataset from file
        data = datasets.load_digits(n_class=10)  # Placeholder for actual file loading logic
    else:
        # Load default digits dataset
        data = datasets.load_digits(n_class=10)
    
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
