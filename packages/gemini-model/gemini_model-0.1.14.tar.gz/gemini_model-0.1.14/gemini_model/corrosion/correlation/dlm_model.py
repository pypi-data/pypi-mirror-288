import math
from gemini_model.model_abstract import Model


class DLM(Model):
    """
    The original DLM (C. de Waard; U. Lotz; D. E. Milliams, 1991)
    model proposed in the article "Predictive Model
    for CO2 Corrosion Engineering in Wet Natural Gas Pipelines"
    https://doi.org/10.5006/1.3585212
    """

    def __init__(self):
        self.parameters = {}
        self.output = {}

    def update_parameters(self, parameters):
        """ To update model parameters

        Parameters
        ----------
        parameters: dict
            parameters dict as defined by the model
        """
        for key, value in parameters.items():
            self.parameters[key] = value

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """
        pass

    def update_state(self, u, x):
        """update the state based on input u and state x"""
        pass

    def calculate_output(self, u, x):
        self.output['corrosion_rate'] = self.get_corrosion_rate(u)

    def get_output(self):
        """get output of the model"""
        return self.output

    def get_corrosion_rate(self, u):
        """
        Calculate the corrosion rate based on various parameters.

        Parameters:
        u (dict): Dictionary containing the required
        parameters for corrosion rate calculation.

        Returns:
        float: Corrosion rate in mm/year
        """
        co2_fraction = u["co2_fraction"]
        pressure = u["pressure"]
        temperature_celsius = u["temperature"]

        co2_fugacity = self._calculate_co2_fugacity(co2_fraction,
                                                    pressure,
                                                    temperature_celsius)  # [bar]
        temperature_kelvin = self._convert_celsius_to_kelvin(temperature_celsius)
        corrosion_rate = (10 ** (5.8 - 1710 / temperature_kelvin + 0.67 * math.log10(co2_fugacity))
                          * self._calculate_scaling_factor(temperature_celsius, co2_fugacity))
        return corrosion_rate

    def _calculate_co2_fugacity(self, co2_fraction, pressure, temperature_celsius):
        """
        Calculate the fugacity of CO2.

        Parameters:
        co2_fraction (float): Fraction of CO2 [-]
        pressure (float): Pressure in the system [bar]
        temperature_celsius (float): Temperature in Celsius

        Returns:
        float: Fugacity of CO2 in [bar]
        """
        temperature_kelvin = self._convert_celsius_to_kelvin(temperature_celsius)

        # Fugacity coefficient calculation
        if pressure <= 250:
            fugacity_coefficient = 10 ** (pressure * (0.0031 - 1.4 / temperature_kelvin))
        else:
            fugacity_coefficient = 10 ** (250 * (0.0031 - 1.4 / temperature_kelvin))

        # CO2 partial pressure
        co2_partial_pressure = co2_fraction * pressure
        return fugacity_coefficient * co2_partial_pressure

    def _calculate_scaling_factor(self, temperature_celsius, co2_fugacity):
        """
        Calculate the scaling correction factor.

        Parameters:
        temperature_celsius (float): Temperature in Celsius
        co2_fugacity (float): Fugacity of CO2 in [bar]

        Returns:
        float: Scaling correction factor
        """
        temperature_kelvin = self._convert_celsius_to_kelvin(temperature_celsius)
        scaling_temperature_threshold = 2400 / (6.7 + 0.6 * math.log10(co2_fugacity))
        scaling_factor = 10 ** (2400 / temperature_kelvin - 0.6 * math.log10(co2_fugacity) - 6.7)

        return min(scaling_factor, 1) if temperature_kelvin >= scaling_temperature_threshold else 1

    @staticmethod
    def _convert_celsius_to_kelvin(temperature_celsius):
        """
        Convert temperature from Celsius to Kelvin.

        Parameters:
        temperature_celsius (float): Temperature in Celsius

        Returns:
        float: Temperature in Kelvin
        """
        return temperature_celsius + 273.15
