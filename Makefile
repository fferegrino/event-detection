.ONESHELL:
run:
	python detector.py 50 60 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-60-50.csv
	python detector.py 50 3600 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-3600-50.csv
	python detector.py 50 7200 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-7200-50.csv
	python detector.py 50 14400 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-14400-50.csv
	python detector.py 10 60 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-60-10.csv
	python detector.py 10 3600 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-3600-10.csv
	python detector.py 10 7200 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-7200-10.csv
	python detector.py 10 14400 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-14400-10.csv
	python detector.py 5 60 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-60-5.csv
	python detector.py 5 3600 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-3600-5.csv
	python detector.py 5 7200 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-7200-5.csv
	python detector.py 5 14400 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-14400-5.csv
	python detector.py 50 60 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-60-50.csv
	python detector.py 50 3600 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-3600-50.csv
	python detector.py 50 7200 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-7200-50.csv
	python detector.py 50 14400 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-14400-50.csv
	python detector.py 10 60 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-60-10.csv
	python detector.py 10 3600 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-3600-10.csv
	python detector.py 10 7200 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-7200-10.csv
	python detector.py 10 14400 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-14400-10.csv
	python detector.py 5 60 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-60-5.csv
	python detector.py 5 3600 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-3600-5.csv
	python detector.py 5 7200 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-7200-5.csv
	python detector.py 5 14400 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-14400-5.csv
evaluate_all:
	python eval.py results/
evaluate:
	python eval.py results/1day-60-50.csv> results/1day-60-50.txt
	python eval.py results/1day-3600-50.csv> results/1day-3600-50.txt
	python eval.py results/1day-7200-50.csv > results/1day-7200-50.txt
	python eval.py results/1day-14400-50.csv > results/1day-14400-50.txt
	python eval.py results/1day-60-5.csv> results/1day-60-5.txt
	python eval.py results/1day-3600-5.csv> results/1day-3600-5.txt
	python eval.py results/1day-7200-5.csv > results/1day-7200-5.txt
	python eval.py results/1day-14400-5.csv > results/1day-14400-5.txt
	python eval.py results/7days-60-50.csv> results/7days-60-50.txt
	python eval.py results/7days-3600-50.csv> results/7days-3600-50.txt
	python eval.py results/7days-7200-50.csv > results/7days-7200-50.txt
	python eval.py results/7days-14400-50.csv > results/7days-14400-50.txt
	python eval.py results/7days-60-5.csv > results/7days-60-5.txt
	python eval.py results/7days-3600-5.csv > results/7days-3600-5.txt
	python eval.py results/7days-7200-5.csv > results/7days-7200-5.txt
	python eval.py results/7days-14400-5.csv > results/7days-14400-5.txt
evaluate_professor:
	python eval.py data/1day/clusters.sortedby.clusterid.csv > results/professor-1day.txt
	python eval.py data/7days/clusters.sortedby.clusterid.csv > results/professor-7days.txt
	