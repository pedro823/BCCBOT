#dictionary containing exam dates for every course
def initExamDict():
		global examdict
		MAC121 = ['MAC121:', 'P3 - 24/11']
		MAT2454 = ['MAT2454:', 'P2 - 28/11', 'SUB - 05/12']
		MAC239 = ['MAC239:', 'P3 - 30/11']
		MAT122 = ['MAT122:', 'P2 - 01/12', 'SUB - 08/11']
		MAE119 = ['MAE119:', 'P2 - 02/12', 'SUB - 05/12']
		MAC216 = ['MAC216:', 'P2 - 08/11']
		examdict = {
				    'MAC121': MAC121,
					'MAT2454': MAT2454, 
					'MAC239': MAC239,
					'MAT122': MAT122,
					'MAE119': MAE119,
					'MAC216': MAC216
					}