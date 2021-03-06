# call this file to begin processing a set of trips from 
# stored vehicle locations. It will ask which trips from 
# the db to process. You can either process individual 
# trips or a range of trips given sequential trip_ids 

import multiprocessing as mp
from time import sleep
from trip import trip
import db

# let mode be one of ('single','range?')
mode = raw_input('Processing mode (single, range, or route) --> ')

def process_trip(valid_trip_id):
	"""worker process called when using multiprocessing"""
	print 'starting trip:',valid_trip_id
	db.reconnect()
	t = trip.fromDB(valid_trip_id)
	t.process()

# single mode enters one trip at a time and stops when 
# a non-integer is entered
if mode in ['single','s']:
	trip_id = raw_input('trip_id to process--> ')
	while trip_id.isdigit():
		if db.trip_exists(trip_id):
			# create a trip object
			this_trip = trip.fromDB(trip_id)
			# process
			this_trip.process()
		else:
			print 'no such trip'
		# ask for another trip and continue
		trip_id = raw_input('trip_id to process --> ')

# 'range' mode does all valid ids in the given range
elif mode == 'range':
	id_range = raw_input('trip_id range as start:end --> ')
	id_range = id_range.split(':')
	# get a list of block id's in the range
	trip_ids = db.get_trip_ids_by_range(id_range[0],id_range[1])
	print len(trip_ids),'trips in that range'
	# how many parallel processes to use?
	max_procs = int(raw_input('max processes --> '))
	# create a pool of workers and pass them the data
	p = mp.Pool(max_procs)
	p.map(process_trip,trip_ids,chunksize=1)
	print 'COMPLETED!'

# process only a certain route, then a subset of that route's trips
elif mode == 'route':
	route_id = raw_input('route_id --> ')
	trip_ids = db.get_trip_ids_by_route(route_id)
	print len(trip_ids),'trips on that route'
	i_range = raw_input('of these, index range as start:end --> ')
	i_range = i_range.split(':')
	# subset to the given range
	trip_ids = trip_ids[int(i_range[0]):int(i_range[1])]
	# start dispatching
	# how many parallel processes to use?
	max_procs = int(raw_input('max processes --> '))
	# create a pool of workers and pass them the data
	p = mp.Pool(max_procs)
	p.map(process_trip,trip_ids,chunksize=1)
	print 'COMPLETED!'

else:
	print 'invalid entry mode given' 







