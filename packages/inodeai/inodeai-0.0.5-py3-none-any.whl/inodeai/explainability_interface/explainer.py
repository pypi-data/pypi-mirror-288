import abc
import eli5
from typing import Any, Optional, Dict
from .modelhandler import GeneralHandler, NeuralNetworkHandler

MODEL_TYPE_MAPPINGS: Dict[str, Any] = {
    "general": GeneralHandler,
    "neuralNetwork": NeuralNetworkHandler
}

class Explainer(abc.ABC):
    """
    Abstract explainer class for different model explainers.
    """

    def __init__(self, model: Any, data: Any, model_type: str = "general") -> None:
        self.model = model
        self.data = data
        self.model_type = model_type

    @abc.abstractmethod
    def explainWeights(self) -> Any:
        """
        Abstract method to explain model weights.
        :return: Explanation object or visualization.
        """
        pass

    @abc.abstractmethod
    def explainPredictions(self, dataPoint: Any) -> Any:
        """
        Abstract method to explain model predictions.
        :param dataPoint: Single data point to explain.
        :return: Explanation object or visualization.
        """
        pass


class SHAPExplainer(Explainer):
    """
    Concrete class for SHAP explainer.
    """

    def __init__(self, model: Any, data: Any, model_type: str = "general") -> None:
        super().__init__(model, data, model_type)
        self.modelHandler = self._makeModelHandler()

    def _makeModelHandler(self) -> Any:
        """
        Dynamically create the appropriate model handler instance based on model type.
        :return: Instance of a model handler class.
        """
        try:
            handler_class = MODEL_TYPE_MAPPINGS[self.model_type]
            instance = handler_class()
            return instance
        except KeyError:
            raise ValueError(f"Invalid model type: {self.model_type}")

    def getExplanationObject(self) -> Any:
        """
        Get the explanation object from the model handler.
        :return: Explanation object.
        """
        return self.modelHandler.getExplainer(self.model, self.data)

    def getBarPlotJson(
        self,
        explanationObject: Any,
        max_features: int = 5,
        output_labels: Optional[Any] = None,
        feature_labels: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Get bar plot JSON data from the explanation object.
        :param explanationObject: Explanation object.
        :param max_features: Maximum number of features to display.
        :param output_labels: Optional output labels.
        :param feature_labels: Optional feature labels.
        :return: JSON data for bar plot visualization.
        """
        return self.modelHandler.getBarPlotJson(
            explanationObject,
            self.data,
            max_features,
            output_labels,
            feature_labels
        )


class ELI5Explainer(Explainer):
    """
    Concrete class for ELI5 explainer.
    """

    def __init__(self, model: Any, data: Any, model_type: str = "general") -> None:
        super().__init__(model, data, model_type)

    def explainWeights(self) -> Any:
        """
        Explain model weights using ELI5.
        :return: Explanation object or visualization.
        """
        try:
            return eli5.explain_weights(self.model, feature_names=self.data.columns.tolist())
        except Exception as e:
            raise RuntimeError(f"Failed to explain model weights: {e}")

    def explainPredictions(self, dataPoint: Any) -> Any:
        """
        Explain model predictions using ELI5 for a single data point.
        :param dataPoint: Single data point to explain.
        :return: Explanation object or visualization.
        """
        try:
            return eli5.explain_prediction(self.model, dataPoint)
        except Exception as e:
            raise RuntimeError(f"Failed to explain prediction for data point: {e}")
