import abc
import shap
import numpy as np
from typing import List, Union, Optional, Dict

class ModelHandlerSHAP(abc.ABC):
    """
    Abstract base class for SHAP model handlers.
    """

    @abc.abstractmethod
    def getExplainer(self, model, data: Optional[np.ndarray] = None) -> shap.Explainer:
        """
        Abstract method to get the SHAP explainer.
        
        :param model: The model to explain.
        :param data: Optional data used for the explainer (used in some explainer types).
        :return: An instance of a SHAP explainer.
        """
        pass

class GeneralHandler(ModelHandlerSHAP):
    """
    Handler for general models using SHAP.
    """

    def getExplainer(self, model, data: Optional[np.ndarray] = None) -> shap.Explainer:
        """
        Get SHAP explainer for a general model.

        :param model: The model to explain.
        :param data: Optional data used for the explainer (not used in this handler).
        :return: A SHAP explainer object.
        """
        explainer = shap.Explainer(model)
        return explainer

    def getBarPlotJson(
        self,
        explanationObject: shap.Explanation,
        processed_data: np.ndarray,
        max_features: int = 5,
        output_labels: Optional[List[str]] = None,
        feature_labels: Optional[List[str]] = None
    ) -> Dict[Union[int, str], Dict[str, Union[List[int], List[float], Optional[Dict[int, str]]]]]:
        """
        Get the SHAP bar plot in JSON form. Handles both 2D and 3D arrays.

        :param explanationObject: SHAP explanation object.
        :param processed_data: The data used to generate SHAP values.
        :param max_features: Maximum number of features to display.
        :param output_labels: Optional labels for outputs.
        :param feature_labels: Optional labels for features.
        :return: JSON data for bar plot visualization.
        """
        def getShapBarGraphJson(array: np.ndarray, n: int = max_features) -> List[Union[np.ndarray, List[float], Optional[Dict[int, str]]]]:
            """
            Helper function to take a 2D numpy array and return a tuple containing the indices of the SHAP values and the SHAP values.

            :param array: 2D numpy array of SHAP values.
            :param n: Number of features to display.
            :return: Tuple of indices, SHAP values, and optional feature labels mapping.
            """
            nonlocal feature_labels
            means = array.mean(axis=0)
            ix = np.argsort(means)
            shap_values = np.abs(means[ix])

            if feature_labels:
                if len(shap_values) < n:
                    feature_dict = {i: feature_labels[i] for i in ix}
                else:
                    feature_dict = {i: feature_labels[i] for i in ix[:n]}
            else:
                feature_dict = None

            if len(shap_values) < n:
                return [ix.tolist(), shap_values.tolist(), feature_dict]
            else:
                shap_values_toRet = list(shap_values[:n])
                sum_shap = np.sum(shap_values[n:])
                shap_values_toRet.append(sum_shap)
                return [ix[:n].tolist(), shap_values_toRet, feature_dict]

        output_dict: Dict[Union[int, str], Dict[str, Union[List[int], List[float], Optional[Dict[int, str]]]]] = {}
        shap_values = explanationObject(processed_data)

        if feature_labels and shap_values.shape[1] != len(feature_labels):
            raise ValueError("Please ensure that the length of the feature_labels list exactly matches the number of features expected by the model.")

        if len(shap_values.shape) > 2:
            # Handle each categorical variable
            if output_labels and len(output_labels) != shap_values.shape[-1]:
                raise ValueError("Please ensure that the output_labels list corresponds exactly to the outputs expected by the model.")
            for z in range(shap_values.shape[2]):
                key = output_labels[z] if output_labels else z
                output_dict[key] = getShapBarGraphJson(shap_values[:, :, z])
        else:
            # Single handling
            if output_labels and len(output_labels) > 1:
                raise ValueError("Please ensure that the output_labels list corresponds exactly to the outputs expected by the model.")
            output_dict = getShapBarGraphJson(shap_values)

        return output_dict

class NeuralNetworkHandler(ModelHandlerSHAP):
    """
    Handler for neural network models using SHAP.
    """

    def getExplainer(self, model, data: np.ndarray) -> shap.Explainer:
        """
        Get SHAP explainer for a neural network model using KernelExplainer.

        :param model: The model to explain.
        :param data: Data used for the explainer (e.g., background data).
        :return: A SHAP KernelExplainer object.
        """
        explainer = shap.KernelExplainer(model, data)
        return explainer
