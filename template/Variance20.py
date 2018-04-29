def run_formula(dv, param=None):
	defult_param = {'t':20}
	if not param:
		param = defult_param		
	t = param['t']
	
	variance20 = dv.add_formula('variance20_j','StdDev(close/Delay(close,1)-1,%d)^2*250'%(t), is_quarterly=False, add_data=False)
	
	return variance20