.ONESHELL:
run:
	python detector.py 10 60 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-60-10.csv
	python detector.py 10 3600 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-3600-10.csv
	python detector.py 5 60 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-60-5.csv
	python detector.py 5 3600 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-3600-5.csv
	python detector.py 10 60 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-60-10.csv
	python detector.py 10 3600 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-3600-10.csv
	python detector.py 5 60 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-60-5.csv
	python detector.py 5 3600 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-3600-5.csv
	python detector.py 10 60 "data/1day/clusters.sortedby.clusterid.csv" -k True -o results/1day-klein-60-10.csv
	python detector.py 10 3600 "data/1day/clusters.sortedby.clusterid.csv" -k True -o results/1day-klein-3600-10.csv
	python detector.py 5 60 "data/1day/clusters.sortedby.clusterid.csv" -k True -o results/1day-klein-60-5.csv
	python detector.py 5 3600 "data/1day/clusters.sortedby.clusterid.csv" -k True -o results/1day-klein-3600-5.csv
	python detector.py 10 60 "data/7days/clusters.sortedby.clusterid.csv" -k True -o results/7days-klein-60-10.csv
	python detector.py 10 3600 "data/7days/clusters.sortedby.clusterid.csv" -k True -o results/7days-klein-3600-10.csv
	python detector.py 5 60 "data/7days/clusters.sortedby.clusterid.csv" -k True -o results/7days-klein-60-5.csv
	python detector.py 5 3600 "data/7days/clusters.sortedby.clusterid.csv" -k True -o results/7days-klein-3600-5.csv
evaluate_all:
	python eval.py results/
evaluate_professor:
	python eval.py data/7days/clusters.sortedby.clusterid.csv > results/professor-7days.txt
clean:
	rm -r results/*