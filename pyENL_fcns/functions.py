'''
Funciones propias de pyENL
'''

from fluids import atmosphere as atm
from fluids import compressible as comp
from fluids import control_valve as cv


def quadsum(x, y):
    return x**2 + y ** 2


def corriente(str1, a, str2, b):
    '''
    Ejemplo para funciones de usuario usando función sencilla para hallar
    la corriente dado un voltaje V y una resistencia R.
    La llamada es similar a como se llaman las funciones de propiedades
    Ejemplo en test/test4.txt
    '''
    V = ['V', 'v', 'voltaje', 'Voltaje']
    R = ['R', 'r', 'resistencia', 'Resistencia']
    try:
        if str1 in V and str2 in R:
            v, r = a, b
        if str1 in R and str2 in V:
            r, v = a, b
        return v / r
    except Exception as e:
        if 'by zero' in str(e):
            raise Exception
        else:
            # Esto es: A menos que el error sea por división por cero, lanzar
            # una excepción especial que será tomada por el algoritmo de
            # excepciones.
            raise ValueError(
                'No se tienen los valores requeridos por la función')


def fluids_atmosphere_1976(str1, Z, dt=0):
    '''
    US Standard Atmosphere 1976 class, which calculates T, P, rho, v_sonic,
    mu, k, and g as a function of altitude above sea level.
    '''
    obj = atm.ATMOSPHERE_1976(Z, dt)
    salida = ['T', 'P', 'rho', 'v_sonic', 'mu', 'k', 'g']
    out = [obj.T, obj.P, obj.rho, obj.v_sonic, obj.mu, obj.k, obj.g]
    if str1 in salida:
        return out[salida.index(str1)]
    else:
        raise Exception('Propiedad no listada')


def fluids_atmosphere_nrlmsise00(str1, Z, latitude=0, longitude=0, day=0, seconds=0,
                                 f107=150.0, f107_avg=150.0,
                                 geomagnetic_disturbance_indices=None):
    '''
    NRLMSISE 00 model for calculating temperature and density of gases in the
    atmosphere, from groud level to 1000 km, as a function of time of year,
    longitude and latitude, solar activity and earth’s geomagnetic disturbance.

    NRLMSISE standa for the US Naval Research Laboratory Mass Spectrometer
    and Incoherent Scatter Radar Exosphere model, released in 2001

    pyENL plus: Density of gases in mol/m^3
    '''
    NA = 6.022140857 * 1e23  # Avogadro number
    obj = atm.ATMOSPHERE_NRLMSISE00(Z, latitude, longitude, day, seconds,
                                    f107, f107_avg,
                                    geomagnetic_disturbance_indices)
    salida = ["rho", "T", "P", "He_density", "O_density", "N2_density", "O2_density",
              "Ar_density", "H_density", "N_density", "O_anomalous_density"]
    out = [obj.rho, obj.T, obj.P, obj.He_density / NA, obj.O_density / NA,
           obj.N2_density / NA, obj.O2_density / NA, obj.Ar_density / NA,
           obj.H_density / NA, obj.N_density / NA, obj.O_anomalous_density / NA]
    if str1 in salida:
        return out[salida.index(str1)]
    else:
        raise Exception('invalid syntax')

# PROBLEM: hwm93 y hwm14 funcionan con f2py, que no está portada a Python3
# def fluids_hwm93(str1, Z, latitude=0, longitude=0, day=0, seconds=0,
#                  f107=150.0, f107_avg=150.0, geomagnetic_disturbance_index=4):
#     '''
#     Horizontal Wind Model 1993, for calculating wind velocity in the
#     atmosphere as a function of time of year, longitude and latitude,
#     solar activity and earth’s geomagnetic disturbance.
#     '''
#
#     obj = atm.hwm93(Z, latitude, longitude, day, seconds,
#                     f107, f107_avg, geomagnetic_disturbance_index)
#
#     salida =


def fluids_Panhandle_A(SG, Tavg, L=None, D=None, P1=None, P2=None,
                       Q=None, Ts=288.7, Ps=101325.0, Zavg=1, E=0.92):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the Panhandle B formula. Can calculate any of the following,
    given all other inputs
        Parameters:

    SG : float

        Specific gravity of fluid with respect to air at the reference temperature and pressure Ts and Ps, [-]

    Tavg : float

        Average temperature of the fluid in the pipeline, [K]

    L : float, optional

        Length of pipe, [m]

    D : float, optional

        Diameter of pipe, [m]

    P1 : float, optional

        Inlet pressure to pipe, [Pa]

    P2 : float, optional

        Outlet pressure from pipe, [Pa]

    Q : float, optional

        Flow rate of gas through pipe, [m^3/s]

    Ts : float, optional

        Reference temperature for the specific gravity of the gas, [K]

    Ps : float, optional

        Reference pressure for the specific gravity of the gas, [Pa]

    Zavg : float, optional

        Average compressibility factor for gas, [-]

    E : float, optional

        Pipeline efficiency, a correction factor between 0 and 1

    Returns:

    Q, P1, P2, D, or L : float

        The missing input which was solved for [base SI]

    '''
    # Aa
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.Panhandle_A(SG, Tavg, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_Panhandle_B(SG, Tavg, L=None, D=None, P1=None, P2=None,
                       Q=None, Ts=288.7, Ps=101325.0, Zavg=1, E=0.92):
    # Aa
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the Panhandle B formula. Can calculate any of the following,
    given all other inputs
    '''
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.Panhandle_B(SG, Tavg, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_Weymouth(SG, Tavg, L=None, D=None, P1=None, P2=None,
                    Q=None, Ts=288.7, Ps=101325.0, Zavg=1, E=0.92):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the Weymouth formula. Can calculate any of the following,
    given all other inputs.
    '''
    # Aa
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.Weymouth(SG, Tavg, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_Spitzglass_high(SG, Tavg, L=None, D=None, P1=None, P2=None, Q=None,
                           Ts=288.7, Ps=101325.0, Zavg=1, E=1.0):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the Splitzglass (high pressure drop) formula. Can calculate
    any of the following, given all other inputs.
    '''
    # Aa
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.Spitzglass_high(SG, Tavg, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_Spitzglass_low(SG, Tavg, L=None, D=None, P1=None, P2=None, Q=None,
                          Ts=288.7, Ps=101325.0, Zavg=1, E=1.0):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the Splitzglass (low pressure drop) formula. Can calculate
    any of the following, given all other inputs.
    '''
    # Aa
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.Spitzglass_low(SG, Tavg, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_Fritzsche(SG, Tavg, L=None, D=None, P1=None, P2=None, Q=None,
                     Ts=288.7, Ps=101325.0, Zavg=1, E=1):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the Fritzsche formula.
    '''
    # Aa
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.Fritzsche(SG, Tavg, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_Oliphant(SG, Tavg, L=None, D=None, P1=None, P2=None, Q=None,
                    Ts=288.7, Ps=101325.0, Zavg=1, E=0.92):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the Oliphant formula.
    '''
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.Oliphant(SG, Tavg, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_Muller(SG, Tavg, mu, L=None, D=None, P1=None, P2=None, Q=None,
                  Ts=288.7, Ps=101325.0, Zavg=1, E=1):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the Muller formula.
    '''
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.Muller(SG, Tavg, mu, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_IGT(SG, Tavg, mu, L=None, D=None, P1=None, P2=None, Q=None,
               Ts=288.7, Ps=101325.0, Zavg=1, E=1):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline with the IGT formula.
    '''
    check = [L, D, P1, P2, Q]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.IGT(SG, Tavg, mu, L, D, P1, P2, Q, Ts, Ps, Zavg, E)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_isothermal_gas(rho, f, P1=None, P2=None, L=None, D=None, m=None):
    '''
    Calculation function for dealing with flow of a compressible gas in a
    pipeline for the complete isothermal flow equation.
    m mass flow
    '''
    check = [L, D, P1, P2, m]
    unknowns = check.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.isothermal_gas(rho, f, P1, P2, L, D, m)
    if output.imag != 0:
        # Hay parte imaginaria en la respuesta, lanzar excepción
        raise Exception
    return output


def fluids_isothermal_work_compression(P1, P2, T, Z=1):
    '''
    Calculates the work of compression or expansion of a gas going through
    an isothermal process.
    '''
    return comp.isothermal_work_compression(P1, P2, T, Z)


def fluids_polytropic_exponent(k, n=None, eta_p=None):
    '''
    Calculates either the polytropic exponent from polytropic efficiency
    or polytropic efficiency from the polytropic exponent.

    Returns isentropic exponent or polytropic efficiency, depending on input.
    '''
    inp = [n, eta_p]
    unknowns = inp.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.polytropic_exponent(k, n, eta_p)
    return output


def fluids_isentropic_work_compression(T1, k, Z=1, P1=None, P2=None, W=None,
                                       eta=None):
    '''
    Calculation function for dealing with compressing or expanding a gas going
    through an isentropic, adiabatic process assuming constant Cp and Cv.
    The polytropic model is the same equation; just provide n instead of k and
    use a polytropic efficienty for eta instead of a isentropic efficiency.
    Can calculate any of the following, given all the other inputs:

    W, Work of compression
    P2, Pressure after compression
    P1, Pressure before compression
    eta, isentropic efficiency of compression
    '''

    inp = [P1, P2, W, eta]
    unknowns = inp.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.isentropic_work_compression(T1, k, Z, P1, P2, W, eta)
    return output


def fluids_isentropic_efficiency(P1, P2, k, eta_s=None, eta_p=None):
    '''
    Calculates either isentropic or polytropic efficiency from the other
    type of efficiency. (isentropic or polytropic)
    '''
    inp = [eta_s, eta_p]
    unknowns = inp.count(None)
    if unknowns != 1:
        raise Exception('invalid syntax')
    output = comp.isentropic_efficiency(P1, P2, k, eta_s, eta_p)
    return output


def fluids_isentropic_T_rise_compression(T1, P1, P2, k, eta=1):
    '''
    Calculates the increase in temperature of a fluid which is compressed or
    expanded under isentropic, adiabatic conditions assuming constant Cp and Cv.
    The polytropic model is the same equation; just provide n instead of k and
    use a polytropic efficienty for eta instead of a isentropic efficiency.
    '''
    return comp.isentropic_T_rise_compression(T1, P1, P2, k, eta)


def fluids_T_critical_flow(T, k):
    '''
    Calculates critical flow temperature Tcf for a fluid with the given
    isentropic coefficient. Tcf is in a flow (with Ma=1) whose stagnation
    conditions are known. Normally used with converging/diverging nozzles.
    Parameters:

        T : float

    Stagnation temperature of a fluid with Ma=1 [K]

        k : float

    Isentropic coefficient []

    Returns:

        Tcf : float

    Critical flow temperature at Ma=1 [K]

    '''
    return comp.T_critical_flow(T, k)


def fluids_P_critical_flow(P, k):
    '''
    Calculates critical flow pressure Pcf for a fluid with the given isentropic coefficient. Pcf is in a flow (with Ma=1) whose stagnation conditions are known. Normally used with converging/diverging nozzles.

    Parameters:

        P : float

    Stagnation pressure of a fluid with Ma=1 [Pa]

        k : float

    Isentropic coefficient []

    Returns:

        Pcf : float

    Critical flow pressure at Ma=1 [Pa]

    '''
    return comp.P_critical_flow(P, k)


def fluids_P_isothermal_critical_flow(P, fd, D, L):
    '''
    Calculates critical flow pressure Pcf for a fluid flowing isothermally and
    suffering pressure drop caused by a pipe’s friction factor.
    Parameters:

        P : float

    Inlet pressure [Pa]

        fd : float

    Darcy friction factor for flow in pipe [-]

        L : float, optional

    Length of pipe, [m]

        D : float, optional

    Diameter of pipe, [m]

    '''
    return comp.P_isothermal_critical_flow(P, fd, D, L)


def fluids_is_critical_flow(P1, P2, k):
    '''
    Determines if a flow of a fluid driven by pressure gradient P1 - P2 is
    critical, for a fluid with the given isentropic coefficient. This function
    calculates critical flow pressure, and checks if this is larger than P2.
    If so, the flow is critical and choked.
    '''
    return comp.is_critical_flow(P1, P2, k)


def fluids_stagnation_energy(V):
    '''
    Calculates the increase in enthalpy dH which is provided by a fluid’s velocity V.

    Parameters:

        V : float

    Velocity [m/s]

    Returns:

        dH : float

    Incease in enthalpy [J/kg]

    '''
    return comp.stagnation_energy(V)


def fluids_P_stagnation(P, T, Tst, k):
    '''
    Calculates stagnation flow pressure Pst for a fluid with the given
    isentropic coefficient and specified stagnation temperature and normal
    temperature. Normally used with converging/diverging nozzles.
    Parameters:

    P : float

        Normal pressure of a fluid [Pa]

    T : float

        Normal temperature of a fluid [K]

    Tst : float

        Stagnation temperature of a fluid moving at a certain velocity [K]

    k : float

        Isentropic coefficient []

    Returns:

    Pst : float

        Stagnation pressure of a fluid moving at a certain velocity [Pa]

    '''
    return fluids_P_stagnation(P, T, Tst, k)


def fluids_T_stagnation(T, P, Pst, k):
    '''
    Calculates stagnation flow temperature Tst for a fluid with the given
    isentropic coefficient and specified stagnation pressure and normal
    pressure. Normally used with converging/diverging nozzles.

    Parameters:

    T : float

        Normal temperature of a fluid [K]

    P : float

        Normal pressure of a fluid [Pa]

    Pst : float

        Stagnation pressure of a fluid moving at a certain velocity [Pa]

    k : float

        Isentropic coefficient []

    Returns:

    Tst : float

        Stagnation temperature of a fluid moving at a certain velocity [K]
    '''
    return comp.T_stagnation(T, P, Pst, k)


def fluids_T_stagnation_ideal(T, V, Cp):
    '''
    Calculates the ideal stagnation temperature Tst calculated assuming the
    fluid has a constant heat capacity Cp and with a specified velocity V and
    tempeature T.

        Parameters:

    T : float

        Tempearture [K]

    V : float

        Velocity [m/s]

    Cp : float

        Ideal heat capacity [J/kg/K]

    Returns:

    Tst : float

        Stagnation temperature [J/kg]

    '''
    return comp.T_stagnation_ideal(T, V, Cp)
