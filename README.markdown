## DC_bench ##
- Simple network benchmark tool using ping and download methods.

## Usage ##
- `dc_bench.py`
  Use command without argument will benchmark all Linode's datacenters
- `dc_bench.py -h`
	For more info
	<pre><code>
	usage: dc_bench.py [-h] [-m {all ,ping ,download}] [-t TIME]
                   [-s SIZE] [-i IP [IP ...]] [-f FILE [FILE ...]]

	Benchmark some datacenters.

	optional arguments:
		-h, --help            show this help message and exit
		-m {all ,ping ,download}, --method {all ,ping ,download}
		                      benchmark method, can be ping, download or all
		-t TIME, --time TIME  ping time default is 10
		-s SIZE, --size SIZE  download file size in MB, default is 0.1
		-i IP [IP ...], --ip IP [IP ...]
		                      host name or ip to ping, if you want to download
		                      benchmark so -f must be used to indicate which file
		                      associate with it
		-f FILE [FILE ...], --file FILE [FILE ...]
		                      file location to test download, if you want to ping
		                      benchmark, so -i must be used to indicate which host
		                      associate with it
	</code></pre>
