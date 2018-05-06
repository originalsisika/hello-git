def run_formula(dv, param=None):
	dv.add_field('PB')
	dv.add_field('LCAP')
	df, msg = api.daily(symbol='000906.SH', start_date=start,end_date=end, fields='close',adjust_mode='post')
	df = df.set_index('trade_date')
	R_M = df.close.pct_change()[1:]
	close = dv.get_ts('close')
	R = close/close.shift(1)-1
	returns = dv.get_ts('close').pct_change()
	PB = 1/dv.get_ts('PB')
	LCAP = dv.get_ts('LCAP')
	
	def percentile_30(row):
		s = row[1]
		point = np.percentile(s, 30)
		return {code: True for code in s[s<point].index}

	def percentile_70(row):
		s = row[1]
		point = np.percentile(s, 70)
		return {code: True for code in s[s>point].index}

	MB_30 = pd.DataFrame(map(percentile_30, LCAP.iterrows()), LCAP.index)
	MB_70 = pd.DataFrame(map(percentile_70, LCAP.iterrows()), LCAP.index)
	PB_30 = pd.DataFrame(map(percentile_30, PB.iterrows()), PB.index)
	PB_70 = pd.DataFrame(map(percentile_70, PB.iterrows()), PB.index)

	pipe = pd.Panel({'MB_30':MB_30, 'MB_70':MB_70, 'PB_30':PB_30, 'PB_70':PB_70,'returns':R_M})
	pipe['MB_30'].fillna(False, inplace=True)
	pipe['MB_70'].fillna(False, inplace=True)
	pipe['PB_30'].fillna(False, inplace=True)
	pipe['PB_70'].fillna(False, inplace=True)
	print(pipe)

	R_biggest = pipe[pipe['MB_70']]['returns'].groupby(level=0).mean()
	R_smallest = pipe[pipe['MB_30']]['returns'].groupby(level=0).mean()
	R_highpb = pipe[pipe['PB_70']]['returns'].groupby(level=0).mean()
	R_lowpb = pipe[pipe['PB_30']]['returns'].groupby(level=0).mean()

	SMB = R_smallest - R_biggest
	HML = R_highpb - R_lowpb
	
	import talib as ta
	constant = pd.Series(np.ones(len(R.index)), index=R.index)
	df = pd.DataFrame({'R': R,'M': R_M,'SMB': SMB,'HML': HML,'Constant': constant})
	df = df.dropna()

	model = pd.stats.ols.MovingOLS(y = df['R'], x=df[['M', 'SMB', 'HML']],window_type='rolling', window=60)
	alpha30 = df['R'] - model.y_predict
	alpha30 = ta.WMA(alpha30, timeperiod=20)
	dv.append_df(alpha30,'Alpha30')
	
	return dv.get_ts("Alpha30")