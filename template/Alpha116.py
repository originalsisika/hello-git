def run_formula(dv, param=None):
	import pandas as pd
	import talib as ta
	
	default_param = {'t':20}
	if not param:
		param = default_param
	t = param['t']
	
	close = dv.get_ts("close_adj").dropna(how='all', axis=1)
	Alpha116 = pd.DataFrame({sec_symbol: ta.LINEARREG_SLOPE(value.values, t) for sec_symbol, value in close.iteritems()}, index=close.index)
	dv.append_df(Alpha116,'Alpha116')
	
	return dv.get_ts("Alpha116")