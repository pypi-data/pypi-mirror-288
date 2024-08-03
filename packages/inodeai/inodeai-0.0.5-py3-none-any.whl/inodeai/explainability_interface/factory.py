import abc
import shap
import eli5
from typing import Any
from .explainer import SHAPExplainer, ELI5Explainer

class ExplainabilityFactory(abc.ABC):
    """
    Abstract factory for different types of explainability options.
    """

    @abc.abstractmethod
    def create_explainer(self) -> Any:
        """
        Create and return an explainer instance.
        :return: Explainer instance.
        """
        pass


class SHAPFactory(ExplainabilityFactory):
    """
    Concrete factory for SHAP explainer.
    """

    def create_explainer(self) -> SHAPExplainer:
        """
        Create and return a SHAP explainer instance.
        
        :return: SHAPExplainer instance.
        """
        try:
            shap_explainer = SHAPExplainer()
            return shap_explainer
        except Exception as e:
            print(f"Error creating SHAP explainer: {e}")
            raise


class ELI5Factory(ExplainabilityFactory):
    """
    Concrete factory for ELI5 explainer.
    """

    def create_explainer(self) -> ELI5Explainer:
        """
        Create and return an ELI5 explainer instance.
        
        :return: ELI5Explainer instance.
        """
        try:
            eli5_explainer = ELI5Explainer()
            return eli5_explainer
        except Exception as e:
            print(f"Error creating ELI5 explainer: {e}")
            raise

