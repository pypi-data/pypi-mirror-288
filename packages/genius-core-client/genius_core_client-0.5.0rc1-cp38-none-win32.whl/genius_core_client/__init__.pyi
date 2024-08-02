from typing import Any, Dict, List, Optional, Union

class PyClient:    
    def query(self, query: str) -> Dict[str, Any]: 
        """
        Executes a query on Genius Core and returns the result as a 
        dictionary.
        """
        ...
    def get_inference(self) -> 'PyInference': 
        """
        Returns an instance of PyInference for performing Bayesian inference.
        """
        ...
    @property
    def inference(self) -> 'PyInference': 
        """
        Property that returns an instance of PyInference for performing 
        Bayesian inference.
        """
        ...

class PyInference:
    def get_probability(self, variables: List[str], evidence: Optional[Dict[str, Any]]) -> Any: 
        """
        Returns the probability of a set of variables given some evidence.
        """
        ...
    def clear_observations(self, variables: Optional[List[str]]) -> Any: 
        """
        Clears the observations of a set of variables.
        """
        ...

def new_with_oauth2_token(protocol: str, host: str, port: str, token: str, timeout: Optional[int], retries: Optional[int]) -> 'PyClient': 
    """
    Initializes a PyClient instance with an OAuth2 token.
    """
    ...
def make_swid(swid_class: str) -> str: 
    """
    Generates a SWID using the provided class.
    """
    ...

class auth:
    class utils:
        @staticmethod
        def retrieve_auth_token_client_credentials(client_id: str, client_secret: str, token_url: str, audience: Optional[str], scope: Optional[str]) -> Dict[str, str]: 
            """
            Retrieves an auth token using client credentials.
            """
            ...