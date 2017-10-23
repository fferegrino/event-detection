run:
	python datareader.py 50 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-50.csv
	python datareader.py 50 "data/7days/clusters.sortedby.clusterid.csv" -o results/7day-50.csv
