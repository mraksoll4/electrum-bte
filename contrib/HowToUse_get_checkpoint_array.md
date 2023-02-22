First you need full node with configurated rpc with txindex=1

Next run python3.7 get_checkpoint_array.py rpc-user prc-password rpc-port

You will recive as example 

get_checkpoint_array.py:38: DeprecationWarning: encodestring() is a deprecated alias since 3.1, use encodebytes()
  base64string = base64.encodestring(('%s:%s' % (username, password)).encode()).decode().replace('\n', '')
Blocks: 118862
Done.


and find file checkpoints_output.json
rename it to checkpoints.json
and place to electrum