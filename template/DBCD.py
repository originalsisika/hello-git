def run_formula(dv, param=None):
	default_param = {'N':5,'M':16,'T':17}
	if not param:
		param = default_param
	
	BIAS = dv.add_formula('BIAS_J',"(close/Ta('MA',0,close,close,close,close,close,%d)-1)*100" %(param['N']),is_quarterly=False,add_data=True)
	
	DIF = dv.add_formula('DIF_J','BIAS-Delay(BIAS,%d)' % (param['M']),is_quarterly=False,add_data=True)
	
	def sma(df, n, m):
		a = n / m - 1
		r = df.ewm(com=a, axis=0, adjust=False)
		return r.mean()
	
	DBCD = dv.add_formula('DBCD_J',"SMA(DIF,%d,1)" % (param['T']),is_quarterly=False,add_data=False,register_funcs={"SMA":sma})
	
	return DBCD