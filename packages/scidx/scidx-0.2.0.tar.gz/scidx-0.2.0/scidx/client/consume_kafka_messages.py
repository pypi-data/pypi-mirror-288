import requests

def consume_kafka_messages(self, topic: str) -> list:
    """
    Consume Kafka messages from a given topic using the API.

    Parameters
    ----------
    topic : str
        The Kafka topic to consume messages from.

    Returns
    -------
    list
        A list of consumed messages.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    url = f"{self.api_url}/stream"
    params = {"topic": topic}
    headers = self._get_headers()
    response = requests.get(url, params=params, headers=headers, stream=True)

    if response.status_code == 200:
        messages = []
        try:
            for line in response.iter_lines():
                if line:
                    messages.append(line.decode('utf-8'))
        except requests.exceptions.RequestException as e:
            error_message = f"Error consuming Kafka messages: {str(e)}"
            raise requests.exceptions.HTTPError(error_message)
        finally:
            # Cleanup or additional processing if needed
            pass
        return messages
    else:
        error_message = (
            f"Failed to consume Kafka messages. "
            f"Request URL: {url}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
