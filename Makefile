.ONESHELL:
run:
	python detector.py 50 "data/1day/clusters.sortedby.clusterid.csv" -o results/1day-50.csv
	python detector.py 50 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-50.csv
	python detector.py 10 "data/7days/clusters.sortedby.clusterid.csv" -o results/7days-10.csv
evaluate:
	python eval.py results/1day-50.csv > results/eval-1day-50.txt
	python eval.py results/7days-50.csv > results/eval-7days-50.txt
	python eval.py results/7days-10.csv > results/eval-7days-10.txt
evaluate_professor:
	python eval.py data/1day/clusters.sortedby.clusterid.csv > results/professor-1day.txt
	python eval.py data/7days/clusters.sortedby.clusterid.csv > results/professor-7days.txt
	