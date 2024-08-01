import requests
import socketio
import numpy as np
import pandas as pd
import time
import logging
from threading import Event, Thread
from cryptography.fernet import Fernet
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VeoxServiceUnavailable(Exception):
    pass

class Smarties:
    def __init__(self, drop='first', sparse=False, handle_unknown='ignore'):
        self.drop = drop
        self.sparse = sparse
        self.handle_unknown = handle_unknown
        self.encodings_ = {}
        self.columns_ = None

    def fit(self, X, y=None):
        if not isinstance(X, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        self.columns_ = X.columns.tolist()
        
        for column in self.columns_:
            if X[column].dtype == 'object' or X[column].dtype.name == 'category':
                unique_values = X[column].unique()
                if self.drop == 'first':
                    unique_values = unique_values[1:]
                elif self.drop is False:
                    pass
                else:
                    raise ValueError("drop must be either 'first' or False")
                
                self.encodings_[column] = {val: i for i, val in enumerate(unique_values)}
        return self

    def transform(self, X):
        if not hasattr(self, 'encodings_') or not hasattr(self, 'columns_'):
            raise ValueError("Smarties instance is not fitted yet. Call 'fit' with appropriate arguments before using this method.")
        
        if not isinstance(X, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        
        result = []
        for column in self.columns_:
            if column in self.encodings_:
                dummies = self._encode_column(X[column], self.encodings_[column])
                result.append(dummies)
            else:
                result.append(X[[column]])
        encoded_df = pd.concat(result, axis=1)
        return encoded_df

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)

    def _encode_column(self, series, encoding):
        encoded = pd.DataFrame(index=series.index)
        for category, code in encoding.items():
            col_name = f'{series.name}_{category}'
            if self.handle_unknown == 'error':
                encoded[col_name] = (series == category).astype(int)
            else:  # 'ignore'
                encoded[col_name] = (series == category).astype(int)
                encoded[col_name] = encoded[col_name].fillna(0)
        if self.sparse:
            return encoded.astype(pd.SparseDtype("int", 0))
        return encoded

class DataProtector:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.column_map = {}
        self.smarties = Smarties(drop='first', sparse=False, handle_unknown='ignore')
        self.scaler = StandardScaler()

    def fit_transform(self, X, y=None):
        logger.info("Fitting and transforming data for protection")
        X_encoded = self.smarties.fit_transform(X)
        X_scaled = self.scaler.fit_transform(X_encoded)
        X_protected = pd.DataFrame(X_scaled, columns=X_encoded.columns)

        self.column_map = {col: self._encrypt_string(col) for col in X_protected.columns}
        X_protected.rename(columns=self.column_map, inplace=True)

        if y is not None:
            y_protected = self._protect_series(y)
            return X_protected, y_protected
        return X_protected

    def transform(self, X):
        logger.info("Transforming data for protection")
        X_encoded = self.smarties.transform(X)
        X_scaled = self.scaler.transform(X_encoded)
        X_protected = pd.DataFrame(X_scaled, columns=X_encoded.columns)
        X_protected.rename(columns=self.column_map, inplace=True)
        return X_protected

    def _protect_series(self, series):
        if series.dtype == 'object':
            return series.apply(self._encrypt_string)
        elif series.dtype in ['int64', 'float64']:
            return (series - series.min()) / (series.max() - series.min())
        else:
            return series

    def _encrypt_string(self, s):
        return self.cipher_suite.encrypt(str(s).encode()).decode()

    def inverse_transform(self, X):
        # Implement the inverse transformation if needed
        pass

class RemoteModel:
    def __init__(self, session_id, server_url):
        self.session_id = session_id
        self.server_url = server_url
        self.sio = socketio.Client(logger=True, engineio_logger=True, reconnection=True, reconnection_attempts=5)
        self.status = 'initialized'
        self.training_complete = Event()
        self.prediction_complete = Event()
        self.prediction_result = None
        self.probability_result = None
        self.data_protector = DataProtector()
        self.connected = Event()
        self.connect_to_server()

    def connect_to_server(self):
        try:
            @self.sio.event
            def connect():
                logger.info(f"Connected to server: {self.server_url}")
                self.connected.set()

            @self.sio.event
            def disconnect():
                logger.warning(f"Disconnected from server: {self.server_url}")
                self.connected.clear()
                self.check_training_status()

            @self.sio.on('fit_complete')
            def on_fit_complete(data):
                logger.info(f"Received fit_complete event: {data}")
                if data['session_id'] == self.session_id:
                    self.status = data['status']
                    self.training_complete.set()
                    logger.info("Training complete")

            @self.sio.on('progress')
            def on_progress(data):
                logger.info(f"Training progress: {data['progress']}%")

            @self.sio.on('predictions')
            def on_predictions(data):
                self.prediction_result = np.array(data['predictions'])
                self.prediction_complete.set()

            @self.sio.on('probabilities')
            def on_probabilities(data):
                self.probability_result = np.array(data['probabilities'])
                self.prediction_complete.set()

            self.sio.connect(self.server_url, transports=['websocket', 'polling'])
            
            # Wait for the connection to be established
            if not self.connected.wait(timeout=10):
                raise socketio.exceptions.ConnectionError("Failed to establish connection within timeout")

        except socketio.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to server {self.server_url}: {str(e)}")
            raise VeoxServiceUnavailable(f"Veox service at {self.server_url} is unreachable at this moment.")

    def check_training_status(self):
        try:
            response = requests.get(f"{self.server_url}/training_status", params={"session_id": self.session_id}, timeout=10)
            response.raise_for_status()
            status_data = response.json()
            if status_data['status'] == 'trained':
                self.status = 'trained'
                self.training_complete.set()
                logger.info("Training complete (checked via HTTP)")
            else:
                logger.info(f"Training status: {status_data['status']}, progress: {status_data['progress']}%")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check training status: {str(e)}")

    def fit(self, X, y, tokens=1):
        logger.info(f"Starting fit method with {tokens} tokens")
        X_protected, y_protected = self.data_protector.fit_transform(X, y)
        logger.info("Data encrypted and transformed")

        self.training_complete.clear()

        # Ensure connection is established before emitting
        if not self.connected.is_set():
            logger.warning("Connection not established. Attempting to reconnect...")
            self.connect_to_server()

        # Emit with retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.sio.emit('fit', {
                    'session_id': self.session_id,
                    'X': X_protected.to_dict(orient='list'),
                    'y': y_protected.tolist(),
                    'tokens': tokens
                })
                break
            except Exception as e:
                logger.error(f"Emit failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)  # Wait before retrying

        timeout = max(300, 60 * tokens)  # Minimum 5 minutes, or 1 minute per token
        logger.info(f"Waiting for training to complete (timeout: {timeout} seconds)")
        start_time = time.time()
        while not self.training_complete.is_set():
            if time.time() - start_time > timeout:
                logger.error(f"Training timed out after {timeout} seconds")
                raise TimeoutError(f"Training timed out after {timeout} seconds")
            time.sleep(5)  # Check every 5 seconds
            self.check_training_status()  # Check status via HTTP

        logger.info("Fit method completed successfully")
        return self

    def predict(self, X):
        return self._predict_internal(X, 'predict')

    def predict_proba(self, X):
        return self._predict_internal(X, 'predict_proba')

    def _predict_internal(self, X, method):
        logger.info(f"Starting {method} method")
        if self.status != 'trained':
            raise ValueError("Model is not trained yet. Call fit() first.")

        X_protected = self.data_protector.transform(X)
        logger.info("Data encrypted and transformed for prediction")

        try:
            response = requests.post(f"{self.server_url}/{method}", 
                                     json={"session_id": self.session_id, "X": X_protected.to_dict(orient='list')},
                                     timeout=60)
            response.raise_for_status()
            result = response.json()['result']
            logger.info(f"{method.capitalize()} completed successfully via HTTP")
            return np.array(result)
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP {method} request failed: {str(e)}")
            raise

def init(key, server_urls=None):
    if server_urls is None:
        server_urls = ['http://x.veox.ai:5000', 'http://y.veox.ai:5000']
    
    for server_url in server_urls:
        logger.info(f"Attempting to initialize connection to server at {server_url}")
        try:
            response = requests.post(f'{server_url}/init', json={'key': key}, timeout=10)
            response.raise_for_status()
            session_id = response.json()['session_id']
            logger.info(f"Successfully initialized connection to {server_url}. Session ID: {session_id}")
            return RemoteModel(session_id, server_url)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to initialize connection to {server_url}: {str(e)}")
    
    logger.error("All VEOX servers are currently unreachable")
    raise VeoxServiceUnavailable("All VEOX servers are currently unreachable. Please try again later.")
