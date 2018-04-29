def run_formula(dv, param=None):
	
	alpha73 = dv.add_formula('alpha73',"-1*(Ts_Rank(Decay_linear(Decay_linear(Correlation(close,volume,10),16),4),5)-Rank(Decay_linear(Correlation(vwap,Ts_Mean(volume,30),4),3)))",is_quarterly=False,add_data=False)
	
	return alpha73