"""
Reads in a groudtruth for the events collection and produces precison / recall values
for a run of an event detection system
"""

"""
There is literally some horrible, horrible code here. Do yourself a favour and stop reading now...
This was written as a run once and throw away script. Funny how things never seem to work out as 
expected, isn't it?
"""

import sys
import csv
import os
from os import listdir
from os.path import isdir, isfile, join

MIN_PCT_COVERAGE_THRESHOLD = 5
MIN_TWEET_COVERAGE_THRESHOLD = 15


def main():
    """Attempts to load relevance information and parse evaluation file"""

    if len(sys.argv) < 2:
        print("You need to specify the path to the clusters file you want to evaluate.")
        print("The file should have the same format as clusters.sortedby.clusterid.csv, however row order does not matter.")
        print("example: python eval.py ../1day/clusters.sortedby.clusterid.csv")
        return

    eval_file = sys.argv[1]

    files_to_evaluate = []

    if isdir(eval_file):
        for f in listdir(eval_file):
            ff = join(eval_file, f)
            if isfile(ff) and ff.endswith(".csv"):
                k = 0
                try:
                    k = f.index("klein")
                except ValueError:
                    k = 0
                g1 = f.index('-', k)
                g2 = f.index('-', g1+1)
                d = f.index('.', g2+1)
                data = f[0:g1]
                time = f[g1+1:g2]
                t = f[g2+1:d]
                files_to_evaluate.append({
                    "file": ff,
                    "day": data,
                    "desc": "T: " +  t + "\tW: " +  time
                })
    else:
        files_to_evaluate.append({
            "file": eval_file,
            "day": "?",
            "desc": "Original file" + eval_file
        })

    events = {}
    descriptions = {}
    category = {}
    cat_count = {}
    tweets_per_event = {}
    category_counts = {}
    total_items_count = 0

    rels_file = open('eval/events.rel', 'r')
    for line in rels_file:
        event, tweet = line.strip().split(" ")
        events[tweet] = event

        if event not in tweets_per_event:
            tweets_per_event[event] = []
        tweets_per_event[event].append(tweet)

    desc_file = open('eval/events.desc', 'r')
    for line in desc_file:
        event, desc = line.strip().split(" ", 1)
        descriptions[event] = desc[1:-1].strip()

    cat_file = open('eval/events.category', 'r')
    for line in cat_file:
        event, cat = line.strip().split(" ", 1)
        category[event] = cat
        if cat not in cat_count:
            cat_count[cat] = 0
        cat_count[cat] = cat_count[cat] + 1


    with open("overall-results.csv", 'w', encoding='utf8', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(("Day",
                             "Evaluation params",
                             "Events",
                             "Clusters",
                             "Recall",
                             "Precission",
                             "F-measure"))
        for evaluation in files_to_evaluate:


            table = []

            candidates = {}

            # read as csv instead of raw file
            with open(evaluation["file"], 'r', encoding='utf-8') as reddit_posts_csv:
                reader = csv.reader(reddit_posts_csv, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                line = 0
                for row in reader:
                    line += 1
                    parts = row
                    if len(parts) < 2:
                        print("Line", line, "malformed, file " + evaluation["file"])
                        print("Expected:\t[cluster_id],[named_entity],[tweet_id]")
                        print("Or:\t\t[cluster_id],[tweet_id]")
                        print("\nGot:\t\t", row)
                        return

                    candidate = str(parts[0].strip())
                    tweet = str(parts[1].strip())
                    if len(parts) > 2:
                        tweet = str(parts[2].strip())

                    if candidate not in candidates:
                        candidates[candidate] = set()
                    candidates[candidate].add(tweet)

                valid_count = 0
                above_threshold = []
                found_above_threshold = []
                ret_cat_count = {}
                cat_ent_count = {}
                cat_event_count = {}
                relevant_tweets = []
                possible_tweets = []
                total_tweets = 0

                rel_found_event = {}

                #print("CLUSTER_ID\tTWEET COVERAGE\tEVENT DESCRIPTION FROM CROWDSOURCED EVALUATION")
                for candidate in sorted(candidates):
                    valid_count += 1
                    # print candidate, ",",

                    relevant = {}
                    for tweet in candidates[candidate]:
                        if tweet in events:
                            if events[tweet] not in relevant:
                                relevant[events[tweet]] = 0
                                rel_found_event[events[tweet]] = []
                            rel_found_event[events[tweet]].append(tweet)
                            relevant[events[tweet]] += 1
                            relevant_tweets.append(tweet)
                    total_tweets += len(candidates[candidate])

                for candidate in sorted(candidates):
                    relevant = {}
                    rt = []
                    for tweet in candidates[candidate]:
                        if tweet in events:
                            if events[tweet] not in relevant:
                                relevant[events[tweet]] = 0
                            relevant[events[tweet]] += 1
                            rt.append(tweet)

                    if len(relevant) >= 0:
                        # print "Event ID:", candidate, "\tContains", str(len(candidates[candidate]))

                        passed = []
                        tr = 0
                        for e in relevant:
                            e = str(e)

                            if relevant[e] > 5 and (int(100.0 / len(candidates[candidate]) * relevant[e]) >= MIN_PCT_COVERAGE_THRESHOLD or relevant[e] >= MIN_TWEET_COVERAGE_THRESHOLD):
                                if category[e] not in ret_cat_count:
                                    ret_cat_count[category[e]] = 0
                                    cat_ent_count[category[e]] = []
                                    cat_event_count[category[e]] = 0

                                possible_tweets += tweets_per_event[e]

                                if e not in found_above_threshold:
                                    ret_cat_count[category[e]] = ret_cat_count[category[e]] + 1
                                cat_event_count[category[e]] += 1

                                above_threshold.append(candidate)
                                found_above_threshold.append(e)

                                if category[e] not in category_counts:
                                    category_counts[category[e]] = 0
                                category_counts[category[e]] += 1
                                total_items_count += 1

                                #print(candidate, "\t\t", str(relevant[e]) + "/" + str(len(set(tweets_per_event[e]))) + " (" + str(int(100.0 / len(candidates[candidate]) * relevant[e])) + "%)\t", descriptions[e][:120])
                            # else:
                                # print "\t\t", str(relevant[e]) + "/" + str(len(set(tweets_per_event[e]))) + "(" + str(int(100.0 / len(candidates[candidate]) * relevant[e])) + "%)\t", descriptions[e][:120]

                            passed.append(e)
                            tr += relevant[e]

                        # print ""

                if valid_count > 0 and len(set(above_threshold)) > 0 and len(set(found_above_threshold)) > 0:
                    event_recall = float(
                        len(set(found_above_threshold))) / len(descriptions)
                    event_precision = float(len(set(above_threshold))) / valid_count
                    f_measure = 2 * ((event_precision * event_recall) / (event_precision + event_recall))


                    csv_writer.writerow((evaluation["day"],
                                         evaluation["desc"],
                                         str(len(descriptions)) + " / " + str(len(set(found_above_threshold))),
                                         str(valid_count) + " / " + str(len(set(above_threshold))),
                                         "%1.3f" % (event_recall),
                                         "%1.3f" % (event_precision),
                                         "%1.3f" % (f_measure)))

                    print("-------   EVENTS   -------\t")
                    print()
                    print("EVENTS / CLUSTER STATISTICS:")
                    print(" - Of", len(descriptions), "events,", len(set(found_above_threshold)), "were detected.")
                    print(" - Of", valid_count, "clusters,", len(set(above_threshold)), "could be matched back to an event.")
                    print("")
                    print("Event Recall:\t\t%1.3f" % (event_recall))
                    print("Cluster Precision:\t%1.3f" % (event_precision))
                    print("Overall F-Measure:\t%1.3f" % (f_measure))

                    print()
                    print()
                    print("----- CATEGORIES  -----")
                    print()
                    print("%-30s    RECALL" % ("CATEGORY NAME"))
                    for cat in sorted(ret_cat_count): # order dictionary for easier comparison
                        print("%-30s  %3d/%d\t(%1.3f)" % (cat, ret_cat_count[cat], cat_count[cat], ret_cat_count[cat] / float(cat_count[cat])))
                    print("")

                    print()
                else:
                    print("Didn't find any event clusters that could be matched to an event.")


if __name__ == "__main__":
    main()
