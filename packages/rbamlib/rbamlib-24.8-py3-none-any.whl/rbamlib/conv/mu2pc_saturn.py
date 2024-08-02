import numpy as np
import rbamlib.models.dip
import rbamlib.conv.mu2pc


def mural2pc_saturn(mu, r, al=np.pi / 2):
    # Define a wrapper for the B0 function to include the 'planet' parameter
    def B0_saturn(r):
        return rbamlib.models.dip.B0(r, planet='Saturn')

    # Call the original mural2pc function with the modified B0 function
    return mu2pc(mu, r, al, B0=B0_saturn)
