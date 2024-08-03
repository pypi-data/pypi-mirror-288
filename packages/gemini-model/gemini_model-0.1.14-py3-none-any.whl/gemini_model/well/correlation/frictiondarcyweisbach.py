import math


class frictiondarcyweisbach:
    """ Class for calculating pressure drop in casings using Darcy-Weisbach correlation """

    @staticmethod
    def calculate_dp(us_l, rho_l, theta, eta_l, d_tube, K, l_cel):
        """ Function to calculate single phase pressure drop using Techo correlation

        Parameters
        ----------
        us_l : float
            superficial liquid flow velocity (m/s)
        rho_l : float
            liquid density (kg/m3)
        theta : float
            Inclination of 1 cell (rad)
        eta_l : float
            liquid vicosity (Pa s)
        d_tube : float
            well diameter of 1 cell (m)
        K : float
            roughness of 1 cell (m)
        l_cel : float
            length of 1 cell (m)

        Returns
        -------
        dp_fric: float
            pressure drop due to friction (Pa)
        dp_grav: float
            pressure drop due to gravity (Pa)
        """
        # constants
        g = 9.81  # acceleration due to gravity (m/s2)

        # friction
        Rem = abs(us_l) * rho_l * d_tube / eta_l
        fric_coeff = 0.25 / ((math.log10((K/(3.7 * d_tube))+(5.74 / (Rem ** (0.9))))) ** (2))

        # gravity
        dp_grav = rho_l * g * l_cel * math.sin(theta)

        # friction
        dp_fric = fric_coeff * rho_l * l_cel / d_tube * (us_l ** 2) / 2
        return dp_fric, dp_grav
