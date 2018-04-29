def run_formula(dv, param=None):
	
	alpha120 = dv.add_formula('Alpha120','Rank(vwap-close)/Rank(vwap+close)',is_quarterly=False,add_data=False)
	
	return alpha120