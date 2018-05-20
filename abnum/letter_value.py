#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: letter_value.py


# 3 letter script codes
# http://pydoc.net/Python/Pytomo/3.0.1/pytomo.kaa_metadata.language/
greek      = 'grc' # ancient greek
hebrew     = 'heb'
coptic     = 'cop'
english    = 'eng'
sanskrit   = 'san'
arabic     = 'ara'
aramaic    = 'arm'
syriaic    = 'syc' #classical
phoenician = 'phn'
finnish    = 'fin'
brahmi     = 'brh'
#ethiopia = 'eth'

data = dict()

data[greek] = (
# letters from α to θ (1 to 9)
	[1, 'alpha'], [2, 'beta'], [3, 'gamma'], [4, 'delta'], [5, 'epsilon'], [6, 'digamma'], [7, 'zeta'], [8, 'eta'], [9, 'theta'],
# letters from ι to ϙ (10 to 90)
	[10, 'iota'], [20, 'kappa'], [30, 'lambda'], [40, 'mu'], [50, 'nu'], [60, 'xi'], [70, 'omicron'], [80, 'pi'], [90, 'qoppa'],
# letters from ρ to ϡ (100 to 900)
	[100, 'rho'], [200, 'sigma'], [300, 'tau'], [400, 'upsilon'], [500, 'phi'], [600, 'chi'], [700, 'psi'], [800, 'omega'], [900, 'sampi'],
# letters from ạ to ṭ (1000 to 9000)
	[1000, 'alpha_m'], [2000, 'beta_m'], [3000, 'gamma_m'], [4000, 'delta_m'], [5000, 'epsilon_m'], [6000, 'digamma_m'], [7000, 'zeta_m'], [8000, 'eta_m'], [9000, 'theta_m'],
# letters from ṃ to ? (10000 to ?)
	[10000, 'mu_m']
)

data[hebrew] = (
# letters from א to ט (1 to 9)
	[1, 'alef'], [2, 'beth'], [3, 'gimel'], [4, 'daleth'], [5, 'he'], [6, 'vau'], [7, 'zayin'], [8, 'heth'], [9, 'teth'],
# letters from י to צ (10 to 90)
	[10, 'yod'], [20, 'kaph'], [30, 'lamed'], [40, 'mem'], [50, 'num'], [60, 'samekh'], [70, 'ayin'], [80, 'pe'], [90, 'tsade'],
# letters from ק to ץ (100 to 900)
	[100, 'qoph'], [200, 'resh'], [300, 'shin'], [400, 'tau'], [500, 'final_kaph'], [600, 'final_mem'], [700, 'final_nun'], [800, 'final_pe'], [900, 'final_tsade']
)

data[english] = (
# letters from a to z (1 to 7 and back, Marty Leeds)
	[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd'], [5, 'e'], [6, 'f'], [7, 'g'], [6, 'h'], [5, 'i'], [4, 'j'], [3, 'k'], [2, 'l'], [1, 'm'],
	[1, 'n'], [2, 'o'], [3, 'p'], [4, 'q'], [5, 'r'], [6, 's'], [7, 't'], [6, 'u'], [5, 'v'], [4, 'w'], [3, 'x'], [2, 'y'], [1, 'z']
)

data[finnsh] = (
# letters from a to ö (1 - 29) ordinary numbers
	[1, 'a'],  [2, 'b'],  [3, 'c'],  [4, 'd'],  [5, 'e'],  [6, 'f'],  [7, 'g'],  [8, 'h'],  [9, 'i'],
	[10, 'j'], [11, 'k'], [12, 'l'], [13, 'm'], [14, 'n'], [15, 'o'], [16, 'p'], [17, 'q'], [18, 'r'],
	[19, 's'], [20, 't'], [21, 'u'], [22, 'v'], [23, 'w'], [24, 'x'], [25, 'y'], [26, 'z'], [27, 'å'],
	[28, 'ä'], [29, 'ö']
)

data[coptic] = (
# letters from ⲁ to ⲑ (1 - 9)
	[1, 'alpha'], [2, 'beta'], [3, 'gamma'], [4, 'delta'], [5, 'ei'], [6, 'so'], [7, 'zeta'], [8, 'eta'], [9, 'theta'],
# letters from ⲓ to ϥ (10 - 19)
	[10, 'yota'], [20, 'kappa'], [30, 'lambda'], [40, 'me'], [50, 'ne'], [60, 'eksi'], [70, 'o'], [80, 'pi'], [90, 'fay'],
# letters from ⲣ to ⳁ (100 - 900)
	[100, 'ro'], [200, 'sima'], [300, 'taw'], [400, 'epsilon'], [500, 'fi'], [600, 'khe'], [700, 'epsi'], [800, 'ou'], [900, 'nine']
)

data[aramaic] = (
# letters from 𐡀‬ to 𐡈
	[1, 'alap'], [2, 'beth'], [3, 'gamal'], [4, 'dalath'], [5, 'he'], [6, 'waw'], [7, 'zain'], [8, 'heth'], [9, 'teth'],
# letters from 𐡉 to 𐡑
	[10, 'yodh'], [20, 'kap'], [30, 'lamadh'], [40, 'mem'], [50, 'num'], [60, 'semkath'], [70, 'e'], [80, 'pe'], [90, 'sadhe'],
# letters from 𐡒 to 𐡕
	[100, 'qop'], [200, 'resh'], [300, 'shin'], [400, 'taw']
# Finals?
#[500, 'final_kap'], [600, 'final_mem'], [700, 'final_nun'], [800, 'final_pe'], [900, 'final_sadhe']
)

data[arabic] = (
# letters from ا to غ
	[1, 'alif'], [2, 'ba'], [3, 'jim'], [4, 'dal'], [5, 'ha'], [6, 'waw'], [7, 'zayn'], [8, 'ha'], [9, 'ta'],
	[10, 'ya'],  [20, 'kaf'], [30, 'lam'], [40, 'mim'], [50, 'nun'], [60, 'sin'], [70, 'ayn'], [80, 'fa'], [90, 'sad'],
	[100, 'qaf'], [200, 'ra'], [300, 'shin'], [400, 'ta'], [500, 'tha'], [600, 'kha'], [700, 'dhal'], [800, 'dad'], [900, 'za'],
	[1000, 'ghayn']
)

data[syriaic] = (
# letters from ܐ to ܛ
	[1, 'alap'], [2, 'beth'], [3, 'gamal'], [4, 'dalath'], [5, 'he'], [6, 'waw'], [7, 'zain'], [8, 'heth'], [9, 'teth'],
# letters from ܝ to ܨ
	[10, 'yodh'], [20, 'kap'], [30, 'lamadh'], [40, 'mem'], [50, 'num'], [60, 'semkath'], [70, 'e'], [80, 'pe'], [90, 'sadhe'],
# letters from ܩ to ܬ
	[100, 'qop'], [200, 'resh'], [300, 'shin'], [400, 'taw']
# Finals?
#[500, 'final_kap'], [600, 'final_mem'], [700, 'final_nun'], [800, 'final_pe'], [900, 'final_sadhe']
)

data[phoenician] = (
# letters from 𐤀‬ to 𐤈‬
	[1, 'alep'], [2, 'bet'], [3, 'giml'], [4, 'dalet'], [5, 'he'], [6, 'waw'], [7, 'zayin'], [8, 'het'], [9, 'tet'],
# letters from 𐤉‬ to 𐤑‬
	[10, 'yod'], [20, 'kap'], [30, 'lamed'], [40, 'mem'], [50, 'num'], [60, 'semek'], [70, 'ayin'], [80, 'pe'], [90, 'sade'],
# letters from 𐤒‬ to 𐤕‬
	[100, 'qop'], [200, 'res'], [300, 'sin'], [400, 'taw']
# Finals?
#[500, 'final_kap'], [600, 'final_mem'], [700, 'final_nun'], [800, 'final_pe'], [900, 'final_sadhe']
)

data[brahmi] = (
# letters from 𑀅 to 𑀣
	[1, 'a'], [2, 'ba'], [3, 'ga'], [4, 'dha'], [5, 'ha'], [6, 'va'], [7, 'ja'], [8, 'gha'], [9, 'tha'],
# letters from 𑀬 to 𑀲
	[10, 'ya'], [20, 'ka'], [30, 'la'], [40, 'ma'], [50, 'na'], [60, 'sha'], [70, 'e'], [80, 'pa'], [90, 'sa'],
# letters from 𑀔 - 𑀢
	[100, 'kha'], [200, 'ra'], [300, 'ssa'], [400, 'ta']
# Finals?
#[500, 'final_kap'], [600, 'final_mem'], [700, 'final_nun'], [800, 'final_pe'], [900, 'final_sadhe']
)

data[sanskrit] = ()
