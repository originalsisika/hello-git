def run_formula(dv, param=None):
	
	alpha121 = dv.add_formula('Alpha121','(Rank(vwap-Ts_Min(vwap,12)))^(Ts_Rank(Correlation(Ts_Rank(vwap,20),Ts_Rank(Ts_Mean(volume,60),2),18),3))',is_quarterly=False,add_data=True)
	
	return alpha121