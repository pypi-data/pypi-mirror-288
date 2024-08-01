Veox Client
Veox Client is a Python package that provides a client for interacting with the Veox remote machine learning service. It offers an sklearn-like API for easy integration into your existing machine learning workflows.
Installation
You can install Veox Client using pip:
Copypip install veox
Usage
Here's a basic example of how to use Veox Client:
pythonCopyimport veox as v
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Generate a sample dataset
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the remote model
model = v.init(key="YOUR_API_KEY", server_url="http://your-server-url:5000")

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Get prediction probabilities
y_prob = model.predict_proba(X_test)

# Calculate accuracy
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy:.4f}")
Note
This package requires access to a running Veox server. Contact your system administrator or the Veox team for server access and API keys.
License
This project is licensed under the MIT License - see the LICENSE file for details.
