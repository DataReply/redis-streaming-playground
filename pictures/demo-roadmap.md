# Redis Demo

1. Dataset, append-log dataset.
	- Dataset from Majid.
	- Explore
	- S3 -> data reply aws test account


2. Have redis deployed in AWS.
	- Redis Service (Amazon Elastic Cache)
		- Cost
		- Features
		- ...
	- EC2 instance with redis installed
		- Install redis
		- Amazon image with redis already installed
		- Backcups?

3. Producer:
- Put part of the Majid's data in a separate s3 bucket.
- Have a lamba function read that data and produce to redis streams.


4. What should we do with the data residing in redis?
	- Aggragation functions (electricity spent per timely basis)
	- TOP 10 energy consumption locations.
	- Counters
		- Number of data points received per time period
	- Enriching the data ...
	- Anonymizing the data ...
	- Filtering 

	Data structures:
		- Redis streams
		- Redis sets, sorted sets, hashmaps, ...

5. Visualize the data at:
- Store the data in elastic search
- Visualize the data in Kibana
- Explore other tool for data visualization that are supported in AWS.


### Services to use:
	- S3
	- Lambda Function
	- Redis (Elastic Cache, or self hosted in EC2)
	- Elastic search
	- Kibana