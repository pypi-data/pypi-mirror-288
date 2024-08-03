# -*- coding: utf-8 -*-
"""
UNIversal Correlations Neutron Stars package. 
"""


__bibtex__="""@ARTICLE{OSP24,
       author = {{Ofengeim}, Dmitry D. and {Shternin}, Peter S. and {Piran}, Tsvi},
        title = "{A three-parameter characterization of neutron stars' mass-radius relation and equation of state}",
      journal = {arXiv e-prints},
         year = 2024,
          eid = {arXiv:2404.17647},
        pages = {arXiv:2404.17647},
          doi = {10.48550/arXiv.2404.17647}
}
"""


__uri__="https://unicorrns.readthedocs.io"

__author__="Peter Shternin"
__email__="pshternin@gmail.com"
__lisence__="MIT"

from .unicorn import *

__all__=["get_Rsamp","get_Psamp","get_Psamp_Unc","Pressure","Radius",r"get_maxMtov"
         ,r"get_maxrhotov",r"get_MAP",r"MRcs_TOV",r"MR_sample"]