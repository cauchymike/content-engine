import pandas as pd
import time
import sqlite3
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from chat import initialize_chatbot
import sys



class ContentEngine(object):

    def __init__(self, database_path: str, ds: pd.DataFrame):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self.ds = ds 
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS similarity_scores (
                item_id TEXT PRIMARY KEY,
                similar_items TEXT
            )
        ''')
        self.conn.commit()

    def train(self):
        start = time.time()
        
        logging.info("Training data ingested in %s seconds." % (time.time() - start))

        # Flush the stale training data from SQLite
        self.cursor.execute("DELETE FROM similarity_scores")
        self.conn.commit()

        start = time.time()
        self._train()
        logging.info("Engine trained in %s seconds." % (time.time() - start))

    def _train(self):
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=1, stop_words='english')
        tfidf_matrix = tf.fit_transform(self.ds['description'])

        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        for idx, row in self.ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]

            # Convert similar_indices to strings before joining
            similar_items = ",".join(str(self.ds['item_id'][i]) for i in similar_indices)

            self.cursor.execute("INSERT INTO similarity_scores (item_id, similar_items) VALUES (?, ?)",
                            (row['item_id'], similar_items))
            self.conn.commit()

    def predict(self, item_id, num):
        query = "SELECT similar_items FROM similarity_scores WHERE item_id = ?"
        self.cursor.execute(query, (item_id,))
        row = self.cursor.fetchone()

        if row:
            similar_items = row[0].split(',')
            recommendations = []

            for item in similar_items[:num]:
                item_id= item  # Split only at the first comma
                item_name = self.ds.loc[self.ds['item_id'] == int(item_id), 'description'].values[0]  # Extract item name from ds
                item_name = item_name.split("-")[0].strip()
                recommendations.append({"id": item_id, "name": item_name})

            return recommendations
        else:
            return []


    def close(self):
        self.conn.close()


# usage:
if __name__ == "__main__":

    # Configure logging settings
    logging.basicConfig(
        filename="myapp.log",  # Specify the log file path
        level=logging.INFO,    # Set the log level (INFO, DEBUG, WARNING, ERROR, etc.)
        format="%(asctime)s [%(levelname)s] %(message)s",  # Define the log message format
        datefmt="%Y-%m-%d %H:%M:%S"  # Define the date-time format
    )

    # Get user input using the chatbot
    user_input = input("User: ")  

    # Use the chat_with_bot function to get the chatbot's response
    chatbot_response = initialize_chatbot(user_input)

    # Load your dataset here
    ds = pd.read_csv("sample-data.csv")

    # Path to SQLite database file
    db_path = "mydatabase.db"

    content_engine = ContentEngine(db_path, ds)  # Pass ds as an argument

    # Train the engine with data source 
    content_engine.train()


    # Make predictions 
    recommendations = content_engine.predict(chatbot_response, num=5)

    print("Recommended items:", recommendations)

    # Close the database connection when done
    content_engine.close()
