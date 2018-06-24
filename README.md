# Event Detection

## Approach

The approach taken is based on the lecture on Event Detection given by Andrew McMinn and Professor Joemon Jose.

### Reading the tweets from the clustered file

The first step in the process is to read the clustered files provided; this process can either be done using the file `clusters.sortedby.clusterid.csv` or the file `cluster.sortedby.time.csv`. At the time of development, only the file organised by clusters was used.

Apart from loading the all the tweets into memory, another three pieces of information were collected in this step:

- A dictionary using the Cluster Id as key and the entities found in it as value
- A dictionary to keep track of the tweets per cluster
- A three-column matrix containing the Cluster Id, timestamp and User Id for each tweet

These pieces of information are valuable summaries of the information read into memory.

### Filter out clusters with less than N tweets

After getting the tweets and all the other summaries into memory, the following step was to try to filter out all the clusters that contain less than N tweets, where N can be provided by the user. This is an important step since it helps us to focus on topics that got more than certain number of mentions, hence, more relevant to the users of Twitter.

Now that some clusters are not being considered, we then can do some further processing on the remaining ones. This processing includes calculating the time centroids for the now "relevant clusters" as well as separating the entities they contain and putting them into sets that allow a more faster processing time than comparing string by string.

### Burst detection

An optional step that could be taken is to make use of an algorithm to detect bursts on streams. In the case of this simple detector, an implementation of the burst detection algorithm proposed by Jon Kleinberg in 2002 in its paper "Bursty and Hierarchical Structure in Streams", was used.

From Kleinberg's algorithm, despite it having the capability of helping us determine a hierarchical structure within the stream, we will only use it to detect a sudden increase in activity around a topic.

### Merge clusters close to each other in time, based on the entities in them

Even though some clusters contain the same entities and refer to the same event, they are split due time constraints or any other reasons. That is why, based on a certain time window t provided by the user, the program tries to merge them into one single 'supercluster'.

This process is divided into two steps:

The first step is to find clusters that could refer to the same event based on the entities they contain, for this step, the program creates a dictionary of lists to keep track of the possible relationship between clusters. We refer to this dictionary of lists 'candidate similar clusters', the following pseudocode illustrates this algorithm:

```  
procedure Find_Similar_Clusters(Entities, Centroid, Delta)
    assign Candidates to empty dictionary
    sort Centroids by time
    for Centroid in Centroids
      assign WindowStart to Centroid.Time – Delta
      assign WindowEnd to Centroid.Time
      for OtherCentroid in Centroids
            if Centroid.Id not in Candidates
                insert empty list in Candidates[Centroid.Id]
            if Centroid.Id equals OtherCentroid.Id
                continue
            if WindowStart <= Centroid1.Value < WindowEnd
                if overlap between Centroid and OtherCentroid entities
                  append OtherCentroid.Id to Candidates [Centroid.Id]
```

This supercluster is created when two clusters have at least one entity in common, and the centroid of one is at most t seconds away from the other. To merge similar clusters a union-find data structure was used. The process is described in the following pseudocode:  

```
procedure Join_Superclusters(Entities, Candidates)
    assign Map to an empty list
  for Candidate in Candidates
        append Candidate.Id to Map
    assign Superclusters to empty dictionary
    for index, Cluster in Map
        assign Superclusters[index] to Entities[Cluster.Id]
        for Candidate in Candidates[Cluster.Id]
            if index and Map.IndexOf(Candidate) are joined
                continue
            join index, Map.IndexOf(Candidate)
            join Superclusters[index] with Entities[Candidate]
```

## Code description &amp; UML diagrams

To keep the project in an organised state all the working parts were divided into several files, containing both classes and functions. The intent is that the performance of the event detection script could be easily improved by changing the behaviour of each of the different modules that comprise it.

![Figure 1](https://i.imgur.com/TPNZ24o.png)

Figure 1 Package diagram for the detector script

### Reading the files

To read the tweets the Python's csv module was used, as described above; at the time of reading other summaries of the clusters are calculated and returned, the descriptions are:

- `clusters`: A dictionary using the `cluster_id` as key and a set f the entities detected for this cluster as values.
- `cluster_counts`: A dictionary using the `cluster_id` as key and the number of tweets per cluster as value.
- `intermediate_tweet_numbers`: a list of lists, where each of the elements of the final level list contains three numbers: `cluster_id`, `timestamp_ms` and `user_id`, this list of lists is later converted to a NumPy array.
- `tweets`: A list of tweets containing all the information in the file

This function, called `read_clustered` receives two parameters: the filename (`file`) and a boolean (`return_tweets`) that indicates whether the tweets should be loaded into memory.

### Filtering and centroid calculation

The filtering step is done taking into consideration the previously calculated `cluster_counts`; the program takes an integer that will use as a threshold to decide whether a cluster is relevant or not. At the time of filtering, and once it has been decided that a cluster is relevant, its time centroid is calculated and stored. The function's name to perform this task is called `threshold_filter`, its input parameters are

- `cluster_counts`: the dictionary with the number of tweets per cluster
- `timestamps`: a array with the timestamp information for each tweet
- `cluster_filter_threshold`: the number of tweets that a cluster should have to be considered relevant.

The return values for this function are:

- `filtered_clusters`: a set of integers, containing only the cluster_ids that contain more than the specified threshold
- `relevant_cluster_centroids`: a two-dimension NumPy array where the columns are `cluster_id` and the calculated `timestamp_centroid` for each cluster.

### Kleinberg filtering and centroid calculation

If the user of the script chooses to perform a second filtering step using the Kleinberg's Burst Detection algorithm the script performs a call to the `kleinberg_filter`, that receives the following parameters:

- `filtered_clusters`: a set of integers, containing only the already filtered clusters that are to be filtered further.
- `timestamps`: a `np.array` with the timestamp information for each tweet
- `s`: the base of the exponential distribution that is used for modeling the event frequencies
- `gamma`: coefficient for the transitions costs between states.

For the purposes of this test, the last two parameters were fixed to values of 2 and 0.6 respectively.

Before calling the actual algorithm, the function performs additional preparations for the code, such as sorting the timestamps in an ascending order and eliminating duplicate timestamps as the algorithm expects different offsets to work with.

After calling the function for each `cluster_id` and its related tweets, the function checks the result to test if the sequence of tweets inside that cluster represent a burst in the conversation, if they do, calculates the centroid for the said cluster, the function returns:

- `filtered_clusters`: a set of integers, containing only the `cluster_ids` that contain more than the specified threshold
- `relevant_cluster_centroids`: a two-dimension NumPy array where the columns are `cluster_id` and the calculated `timestamp_centroid` for each cluster.

### Find similar clusters based on time

This is the first non-trivial task performed by this program, the function name is `find_similar_clusters`, before describing the algorithm, we will describe the input parameters:

- `entities`: a dictionary containing the set of entities detected in each cluster
- `centroids`: the time centroids found for each relevant cluster
- `delta`: the seconds that could have passed between similar clusters to be considered as candidates to be merged.

The return value for this function is a dictionary, called `candidate_similar_clusters` within the body of the function. Each entry in this dictionary has a `cluster_id` as key and a list of possible mergeable `cluster_ids` as values.

This activity diagram models the algorithm implemented in the following piece of code 

```python
for centroid in centroids_sortedby_time:

    cluster_id = centroid[0]
    window_start = centroid[1] - window_timespan
    window_end = centroid[1]

    for centroid_ in centroids_sortedby_time:  # search again from the beginning
        other_id = centroid_[0]

        if cluster_id not in candidate_similar_clusters:
        candidate_similar_clusters[cluster_id] = []

        if cluster_id == other_id:
         continue

       if window_start <= centroid_[1] < window_end:
            overlap = entities[cluster_id].intersection(entities[other_id])
             if len(overlap) > 0:  # if there is overlap,
                 candidate_similar_clusters[cluster_id].append(other_id)
return candidate_similar_clusters
```

It is worth mentioning that the time complexity of this algorithm is O(n^2).

The previous source code is described by the activity diagram in Figure 2:

![Figure 2](https://i.imgur.com/0OOEsFU.png)

Figure 2 Activity diagram for the filtering step

### Cluster joining

Once the candidate clusters had been identified we can proceed to the merging phase, in this phase new clusters (from now on called 'superclusters') will be created by merging the candidate clusters.

For this process, a disjoint-set (also known as union-find) data structure was used as is one of the most helpful data structures to group certain things, in a efficient manner.

 This is also a non-trivial task, and as such, will be described after describing the input parameters as well as the return values.

Input parameters:

- `entities`: a dictionary containing the set of entities detected in each cluster
- `candidate_similar_clusters`: a dictionary where the key is a `cluster_id` and the value is a list of related clusters

Return values:

- `uf`: A union-find data structure containing the clusters merged together
- `cluster_map`: a list that serves as a map between the real cluster_id and the generated `cluster_id` used for the Union-Find structure
- `superclusters`: A dictionary where the key is the `cluster_id` and the value is a set containing the new, merged entities for each supercluster.

The following code is part of this method, and it shows how to work with the Union-Find data structure

```
for i, original_cluster in enumerate(cluster_map):

    superclusters[i] = entities[original_cluster]
    for candidate in candidate_similar_clusters[original_cluster]:

        if uf.find(i, cluster_map.index(candidate)):
            continue
        uf.union(i, cluster_map.index(candidate))
        superclusters[i] = superclusters[i] | entities[candidate]
```

The function works as described by the diagram in Figure 3:

![Figure 3](https://i.imgur.com/vqBn8Lm.png)

Figure 3 Activity diagram for the merging step

### Writing the result

Finally, all the tweets corresponding to the selected clusters are printed out to a CSV file with the same format as the input file, this is performed inside the actual script rather than in a separate module.

When writing the tweets, the script traverses through the complete collection of tweets and checks if the original cluster assigned to that tweet was selected as relevant by our algorithm, if so, it writes it to the file.

### Data and measures

To evaluate the performance of the event detector three different measures were used:

- Precision (positive predictive value), defined as:

    precision = |{relevantdocuments}∩{retrieveddocuments}| / |{retrieveddocuments}|

- Recall (sensitivity)

    recall = |{relevantdocuments}∩{retrieveddocuments}| / |{relevantdocuments}|

- _F-measure_ (F1 score)  

    F1 = 2 × precison × recall / (precission + recall)

These three values were calculated automatically by the `eval.py` script provided by the professor.

As the detector script allows to be customizable via parameters on the command line, several configurations were tried against both sets of data; the results were compared against each other, as well as against the original results calculated by using the input file without preprocessing:

The results of running the detector script using the file containing 1-day worth of information are summarised in the following table:

| Description1 | Events2 | Clusters3 | Recall | Precision | F-measure |
| --- | --- | --- | --- | --- | --- |
| **ORIGINAL DATA** | **506 / 19** | **8829 / 120** | **0.038** | **0.014** | **0.020** |
| T: 10    W: 60 K | 506 / 18 | 285 / 76 | 0.036 | 0.267 | 0.063 |
| T: 10    W: 60 | 506 / 18 | 347 / 82 | 0.036 | 0.236 | 0.062 |
| T: 10    W: 3600 K | 506 / 18 | 208 / 44 | 0.036 | 0.212 | 0.061 |
| T: 5     W: 60 K | 506 / 19 | 640 / 104 | 0.038 | 0.163 | 0.061 |
| T: 10    W: 14400 | 506 / 18 | 194 / 38 | 0.036 | 0.196 | 0.060 |
| T: 10    W: 3600 | 506 / 18 | 253 / 48 | 0.036 | 0.190 | 0.060 |
| T: 10    W: 7200 | 506 / 18 | 223 / 41 | 0.036 | 0.184 | 0.060 |
| T: 5     W: 3600 K | 506 / 19 | 469 / 66 | 0.038 | 0.141 | 0.059 |
| **T: 5     W: 60** | **506 / 19** | **951 / 117** | **0.038** | **0.123** | **0.058** |
| T: 5     W: 14400 | 506 / 19 | 486 / 52 | 0.038 | 0.107 | 0.056 |
| T: 5     W: 3600 | 506 / 19 | 661 / 72 | 0.038 | 0.109 | 0.056 |
| T: 5     W: 7200 | 506 / 19 | 569 / 59 | 0.038 | 0.104 | 0.055 |
| T: 50    W: 14400 | 506 / 13 | 44 / 16 | 0.026 | 0.364 | 0.048 |
| T: 50    W: 3600 | 506 / 13 | 47 / 17 | 0.026 | 0.362 | 0.048 |
| T: 50    W: 60 | 506 / 13 | 58 / 25 | 0.026 | 0.431 | 0.048 |
| T: 50    W: 7200 | 506 / 13 | 44 / 16 | 0.026 | 0.364 | 0.048 | 

 > 1. T: threshold used to filter out clusters, W: window timeframe used to consider two clusters to be related to the same event, K: Kleinberg algorithm was used as a second filter
 > 2. Events / Detected
 > 3. Found clusters / Matched to an event 

Table 1: Results of several evaluations sorted by F-measure value

From Table 1 we can see that the best value for the F-measure was obtained using a threshold of 10 tweets per cluster, a timeframe of one minute and by performing a second filtering stage using the burst detection algorithm.

Yet, the number of clusters events detected dropped by almost 30 in relation to the reference value. However, if we look at the results obtained when using a threshold of 5 tweets per cluster and the same timeframe we can see that the difference in F-measure between this and the best performance is only of 0.004, and the number of clusters matched to events is close to the original reference value.

It could be said that the best configuration for the detector is using a threshold of 5 and a time frame of 30 seconds.

Now, observe at Table 2 which contains the result of executing the same experiment but using the file containing a week-long data collection:

| Description1 | Events2 | Clusters3 | Recall | Precision | F-measure |
| --- | --- | --- | --- | --- | --- |
| **ORIGINAL DATA** | **506 / 106** | **50631 / 696** | **0.209** | **0.014** | **0.026** |
| T: 10 W: 60 K | 506 / 90 | 888 / 346 | 0.178 | 0.39 | 0.244 |
| T: 10    W: 60 | 506 / 94 | 1162 / 381 | 0.186 | 0.328 | 0.237 |
| T: 10 W: 3600 | 506 / 90 | 649 / 229 | 0.178 | 0.353 | 0.237 |
| T: 10    W: 14400 | 506 / 96 | 783 / 230 | 0.190 | 0.294 | 0.231 |
| T: 10    W: 3600 | 506 / 95 | 880 / 257 | 0.188 | 0.292 | 0.229 |
| T: 5 W: 60 K | 506 / 101 | 1778 / 478 | 0.2 | 0.269 | 0.229 |
| T: 10    W: 7200 | 506 / 95 | 847 / 245 | 0.188 | 0.289 | 0.228 |
| T: 5 W: 3600 K | 506 / 102 | 1324 / 337 | 0.202 | 0.255 | 0.225 |
| **T: 5     W: 60** | **506 / 106** | **3064 / 628** | **0.209** | **0.205** | **0.207** |
| T: 5     W: 7200 | 506 / 107 | 2055 / 416 | 0.211 | 0.202 | 0.207 |
| T: 5     W: 14400 | 506 / 108 | 1740 / 347 | 0.213 | 0.199 | 0.206 |
| T: 5     W: 3600 | 506 / 107 | 2238 / 442 | 0.211 | 0.197 | 0.204 |
| T: 50    W: 60 | 506 / 48 | 195 / 113 | 0.095 | 0.579 | 0.163 |
| T: 50    W: 14400 | 506 / 48 | 152 / 77 | 0.095 | 0.507 | 0.160 |
| T: 50    W: 3600 | 506 / 48 | 154 / 78 | 0.095 | 0.506 | 0.160 |
| T: 50    W: 7200 | 506 / 48 | 153 / 77 | 0.095 | 0.503 | 0.160 

 > 1. T: threshold used to filter out clusters, W: window timeframe used to consider two clusters to be related to the same event, K: Kleinberg algorithm was used as a second filter
 > 2. Events / Detected
 > 3. Found clusters / Matched to an event 

Table 2: Results of several evaluations sorted by F-measure value

Again, when looking at the configuration with the best F-measure value, we can see that the number of clusters matched to events has dropped by almost 50% when compared to the reference value but has outperformed by almost ten times the F-measure of the reference.

If we observe the value obtained when using the configuration, we determined was the best for the one-day file, we can see that, though the F-measure is 0.030 less than the best, the number of clusters matched to events increased to almost the same as the reference while detecting the same number of events. This configuration is a good candidate to be considered one of the best and could be used as a baseline to work with more longer sets of data.

When trying to optimise the parameters such as the time frame window, the threshold to filter tweets or the gamma parameter you may improve the overall results such as the F-measure or the recall, however, you lose on the number of clusters detected by the algorithm, which may be an undesirable effect.

## Critical Discussion

Though some progress was made, the detector is far from perfect. There are several improvements that could be made to it, both to improve its efficiency and electiveness.

For the efficiency side, we could find a way to not load all the collection of tweets into memory from the beginning, probably by using a permanent storage system that allows to query and retrieve the tweets by cluster. Another improvement could be to find better data structures, for example, to map the original cluster_id to the one assigned when working with the Union-Find data structure as the time complexity of looking for a value in a list is linear.

As for the effectiveness, by visually inspecting the file one can perceive that there are certain patterns in some clusters. Some patterns found were that some of the clusters contain very similar tweets posted by different accounts with small variations such as the URLs in them or the accounts they were mentioning. Other sources of 'nosy' tweets are those referring to horoscopes or another kind of recurrent scheduled messages that do not belong to an event. And a third source of noise is automated tweets, originated by third-party applications because of user interaction with them, outside the twitter environment.

A proposed solution could be to examine the similarity of words between several tweets in the same cluster. One can strip the URLs and mentioned users, which in most of the cases are different, and then analyse the remaining text.

Another possible solution could be to identify the tweets that were posted automatically by third-party applications and decide whether that tweet relevant based on the interaction that originated it. For example, a tweet coming from a service like Foursquare or eBay is less likely to contain information about an event than other coming from the Twitter website or Twitter mobile applications.

To try to improve the effectiveness we could have played with the `s` and gamma parameters of the burst detection algorithm, this could lead to a different, possibly better, selection of clusters, increasing the number of clusters filtered.

By working using only the clustered data, it is difficult to identify this kind of _spammy_ clusters as further text processing is required to deal with the content of the tweet. Processing the tweet content would help to identify its possible _spammy_ origin and once recognized delete it from the cluster, deletion that could lead to the deletion of the entire cluster.

# Traffic event detection

A lot of previous works have been performed on the topic of traffic event detection using social media streams, in particular, Twitter due to its characteristics and accessibility. Several challenges have been found when trying to implement this kind of event detecting systems, not only for traffic but also for another kind of events.

The approach decided to take in this exercise consists of two phases: Preprocessing and Real-Time, these two will be explained using a simple, practical case of traffic event detection in Mexico City.

## Preprocessing

### Finding instances of first reporting

The first step in the construction of this traffic event detector is to identify the first tweets related to real traffic events occurrences. A good starting point could be starting our search from official city accounts reporting traffic events. As many people have previously noted, official accounts usually are not the first ones to report such events; but they do report proved events, and thus we can rely on them for their veracity.

We then would select some tweets from these accounts and try to find previous instances of tweets mentioning said events. We can use the time the official tweet was sent as a starting point to search retroactively. Once we get those tweets, we can analyse them to find patterns that indicate how people usually report such events: to which accounts they tweet at, what kind of language is used, and what hashtags they use.

For example, users tend to tweet mentioning television networks, police departments, or the so-called "live traffic reporting" accounts that several users set up for their own cities. Sometimes special hashtags are used in order to provide a notion of belonging or relation to a specific place. It is important for us to know these accounts, as users often tweet at them when it comes to reporting traffic events, whether it be to inform the general public or simply to complain to the city officials.

For Mexico City, these are some of the most popular accounts users tweet at:

| Official | Unofficial |
| --- | --- |
| @OVIALCDMX | @Isidrocorro |
| @072AvialCDMX | @Peaton_No |
| @GobCDMX | @ApoyoVial |
| @UCS_CDMX | @AA_DF |

Table 3 Official and unofficial accounts reporting traffic events in Mexico City

### Discover street names and localisms to form dictionaries

After discovering these patterns, we can start building a thesaurus of places, roads, buildings, and other significant city landmarks specific to each city where we want to detect events, as people living in a city usually tend not to refer to places using its official name but a pseudonym or a traditional name. Whether it be because of tradition or by the limitation set by Twitter itself of having messages no longer than 140 characters. The construction of this dictionary could be achieved by working with citizens, historians, or even the local government.

This is an important step since as much as we could rely on third-party services such as _GeoNames_ to identify places and assign proper geolocation tags given the entities in a tweet, it is hard to find geolocation for places not named by their real name. Using this thesaurus, we could provide these services with a "real", and official name. For example:

| Local name | Real name |
| --- | --- |
| La Diana | Fuente de La Diana Cazadora |
| El Ángel | Monumento a la Independencia |
| Peri | Anillo Periférico |
| La Suavicrema | La Estela de Luz |
| Panti | Pantitlán |

Table 4 Local names compared to official names

Another useful resource to build would be to create a dictionary of "traffic words", composed of localisms used to refer to common traffic events. Because "traffic jam" is not used everywhere to refer to a "traffic jam", take for example, in different Spanish speaking countries a traffic jam could be referred as: "trancadera", "taco", "trancón", "tapón", "atasco", "cola", "embotellamiento", "tranque", "presa", "atrancazón", "trabazón", o "tráfico". To do this we can rely on the same group of experts. We used to create the places thesaurus.

## Real-time processing

### Working with the stream

Once we have all the previous information we can continue to work with the Streaming API to retrieve tweets in real-time, for this phase, we can work using three different approaches: using our "traffic words", using our "traffic accounts" or using a bounding box on the stream.

#### "Traffic Words"

Using our dictionary of "traffic words" to keep track of such words, this will help us to reduce noise coming from the stream, saving us from having to process in our servers tweets that don't contain relevant information. This approach could lead us to capture tweets that mention the words but have no relation whatsoever to any traffic event or even worse: have nothing to do with the city we're working on.

As an example, check the tweets below: both come from the same official account, contain a "traffic-related word" but only one refers to a traffic event:

##### Not traffic related:

![](https://i.imgur.com/632Wukk.png)

Translation: Bicycles can be parked on sidewalks as long as they don block pedestrian transit. Art. 31. bit.ly/1K9m7sA

##### Traffic related:

![](https://i.imgur.com/q6FnxmM.png)

Translation: You will find slow transit in the Av. #Insurgentes from Anillo Periférico to Circuito Interior

#### "Traffic accounts"

Another approach, very similar to the one described previously, is to keep track of the accounts that are closely related to traffic events. This is again another option that would save us from having to do the resource consuming task of preprocessing vast amounts of data. However, we would still have to do certain filtering, since not all the mentions to these accounts correspond to traffic events.



##### Traffic related:

![](https://i.imgur.com/TG2fy2g.png)

Translation: @OVIALCDMX Good day  badly synchronized semaphores in Matias Romero crossing Av Coyoacan Adolfo Prieto and Gonzalez de Cossio in Col Del Valle Greetings @UCS_CDMX

##### Not traffic related:

![](https://i.imgur.com/pTcnUPz.png)

Translation: @UCS_CDMX how can someone request surveillance in the colonies? Col. Narvarte has a high index of car parts robbery @En_Narvarte

#### Bounding box

Another option that we have when working with the Streaming API, is the possibility to set a geographical rectangle from where we want to collect data from. The way it works is described thoroughly on the Twitter documentation, but it uses two factors to match tweets: the tweet location (if the user had it enabled) and the user location (if he had it filled). Other tweet that does not fall within those constraint is not considered. Of all the three approaches this is the most unreliable, since not all users have location enabled or city set up on their profiles. Also, getting all the tweets from a certain city would mean having to do a extensive filtering process on our side.

### After detection

For every tweet we get from the streaming API, we would have to process it to find out whether it contains all of some of the characteristics previously detected in the pre-processing phase. Once we determined it as a possible traffic-reporting tweet, and identified the key components of said tweet, we can move on to the next phase.

#### Perform narrowed searches

Once we get information from the streaming processing module we can start conducting more narrowed searches using the information obtained during the previous step of real-time processing. For these narrowed searches, we can use the Search endpoint in the REST APIs delegating this search to another sub systems. Since we know what to look for we could queue a series of searches based on location, hashtags, users, mentions, etc.

For this task, we propose a specific window of time for a possible event to "mature", this means that if another mention of the same event appears (whether it be on the stream or in any of our searches) we could increase the possibility of this tweet being related to a real traffic event. However, if time passes and no other mention appears we could consider discarding this as a non-worthy event.

## Critical discussion

The approach described in this document relies on previous knowledge of the place where we want to monitor the traffic events. What can be considered as one of its strengths, since it could lead to a more filtered stream of events, at the same time could be defined as one of its weaknesses, for that it cannot be generalised to be a solution that works right out of the box, but requires some time to be set up.

Like many other proposed solutions, the success of this implementation depends completely on how active the Twitter community is in terms of volume of tweets (quantitative factor), and what kind of interactions are they having (qualitative factor), even the best algorithm will have a bad performance if the data that it consumes is not enough to train or if the data is in bad shape and needs some form of costly transformation.
