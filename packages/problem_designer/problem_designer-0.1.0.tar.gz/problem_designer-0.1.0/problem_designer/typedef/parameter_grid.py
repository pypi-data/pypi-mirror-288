from sklearn.model_selection import ParameterGrid

from problem_designer.typedef.helper import SupportsParameterGrid
from problem_designer.typedef.spec import StrictBaseModel


class SpecParameterGrid(StrictBaseModel):
    def _build_basic_parameter_dict(self):
        result = {}
        for field_name, field in self:
            if isinstance(field, SupportsParameterGrid):
                result[field_name] = field.evaluate_for_parameter_grid()
            else:
                result[field_name] = field
        return result

    def get_parameter_grid(self):
        """
        Turns the base model into a scikit-parameter grid. To accomplish this some restructuring is done
        on the object
        Returns:

        """
        base_dict = self._build_basic_parameter_dict()
        for key in base_dict.keys():
            if not isinstance(base_dict[key], list):
                # parameter grid expects all values to be lists
                base_dict[key] = [base_dict[key]]
        # repackage the grid as the data class, makes later access easier
        return [self.__class__(**dict_) for dict_ in ParameterGrid(base_dict)]
