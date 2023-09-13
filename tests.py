import unittest
from engines import ContentEngine
from chat import initialize_chatbot
import pandas as pd

class ContentEngineTestCase(unittest.TestCase):

    def setUp(self):
        # Initialize the content engine and chatbot
        training_data = pd.read_csv("sample-data.csv")
        self.content_engine = ContentEngine("mydatabase.db", training_data)

    def test_integration(self):
        # Train the content engine with sample data
        self.content_engine.train()

        # Simulate user input to the chatbot
        user_input = "Tell me about item 1"
        chatbot_response = initialize_chatbot(user_input)

        # Use the chatbot's response as the item for recommendations
        recommendations = self.content_engine.predict(chatbot_response, num=5)

        # Assert that recommendations are not empty
        self.assertTrue(len(recommendations) > 0)

        # Assert that recommendations contain item names and IDs
        for recommendation in recommendations:
            self.assertIn("id", recommendation)
            self.assertIn("name", recommendation)

    def tearDown(self):
        # Close the content engine connection
        self.content_engine.close()

if __name__ == '__main__':
    unittest.main()
