import pvleopard

vars = {}
with open('.env') as f:
	for line in f:
		line = line.strip()
		if line and '=' in line:
			key, value = line.split('=', 1)
			vars[key.strip()] = value.strip("'\'")
   
leopard = pvleopard.create(
    access_key = vars['ACCESS_KEY'],
    model_path = 'Arco-STT.pv'
)