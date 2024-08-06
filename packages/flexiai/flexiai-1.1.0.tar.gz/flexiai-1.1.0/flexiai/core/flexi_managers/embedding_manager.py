# flexiai/core/flexi_managers/embedding_manager.py
from openai import OpenAIError


class EmbeddingManager:
    """
    EmbeddingManager handles the creation of embeddings using OpenAI's API.

    Attributes:
        client (OpenAI or AzureOpenAI): The client for interacting with OpenAI or Azure OpenAI services.
        logger (logging.Logger): The logger for logging information and errors.
    """

    def __init__(self, client, logger):
        """
        Initializes the EmbeddingManager with the OpenAI client and logger.

        Args:
            client (object): The OpenAI client instance.
            logger (logging.Logger): The logger instance for logging information.
        """
        self.client = client
        self.logger = logger


    def create_embedding(self, text):
        """
        Creates an embedding for the given text using OpenAI's embedding model.

        Args:
            text (str): The text to create an embedding for.

        Returns:
            list: The generated embedding.

        Raises:
            OpenAIError: If the embedding API call fails.
            Exception: For any unexpected errors.
        """
        try:
            # self.logger.info(f"Creating embedding for text: {text[:50]}...")
            response = self.client.embeddings.create(input=text, model="text-embedding-ada-002")
            self.logger.info("Embedding created successfully.")
            return response.data[0].embedding
        except OpenAIError as e:
            self.logger.error(f"OpenAI error during embedding creation: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during embedding creation: {str(e)}", exc_info=True)
            raise
