from collections import Counter
from scipy.spatial import distance

from django.utils.datastructures import SortedDict
import numpy

from analysis.computation.optics import amyxzhang


def flatten(seq):
    return [el for l in seq for el in l]


def normal_distribution(x, mu, sigma):
    first = 1 / (sigma * numpy.sqrt(2 * numpy.pi))
    second = -1/2 * (((x - mu) / sigma) ** 2)

    return first * (numpy.e ** second)


def normalization(value, mu, sigma):
    return (value - mu) / sigma


def normalize_array(array, column=0):
    c_array = array[:,column]
    mean = c_array.mean()
    std = c_array.std()
    if std != 0:
        array[:, column] = (array[:, column] - mean) / std

    return array


def special_counter(seq, proportional=False, normalized=False):
    counted = Counter(seq)
    total = len(seq)

    if proportional:
        for key in counted.keys():
            counted[key] /= total

    if normalized:
        values = counted.values()
        mean = numpy.mean(values)
        std_dev = numpy.std(values)

        for key in counted.keys():
            counted[key] = normalization(counted[key], mean, std_dev)

    return counted


def get_frequency_distance(small_seq, coll_dic):
    counted = special_counter(small_seq, True)
    for key in coll_dic.keys():
        if key not in counted.keys():
            counted[key] = 0

    small_array = numpy.array([v for _, v in sorted(counted.items())])
    coll_array = numpy.array([v for _, v in sorted(coll_dic.items())])

    return distance.euclidean(small_array, coll_array)


def aux_basic_stats(data_seq, string, flat=False):
    if flat:
        data_seq = flatten(data_seq)

    freq = Counter(data_seq)
    freq_values = list(freq.values())

    data = SortedDict([
        ('Value Min', min(data_seq)),
        ('Value Max', max(data_seq)),
        ('Value Mean', numpy.mean(data_seq)),
        ('Value Median', numpy.median(data_seq)),
        ('Value Standard deviation', numpy.std(data_seq)),
        ('Value Quartile 1', numpy.percentile(data_seq, 25)),
        ('Value Quartile 3', numpy.percentile(data_seq, 75)),
        ('Amount with most common', max(freq.values())),
        ('Amount with less common', min(freq.values())),
        ('Amount Mean', numpy.mean(freq_values)),
        ('Amount Median', numpy.median(freq_values)),
        ('Amount Standard deviation', numpy.std(freq_values)),
        ('Amount Quartile 1', numpy.percentile(freq_values, 25)),
        ('Amount Quartile 3', numpy.percentile(freq_values, 75)),
        (string, len(data_seq)),
    ])
    return data


# chart functions #

def histogram(int_sequence, bins, label, swap=True, string=True):
    hist_data = numpy.histogram(int_sequence, bins)
    r = [label]

    for i in range(bins):
        pair = [hist_data[1][i], hist_data[0][i]]
        if swap:
            pair.reverse()
        if string:
            pair[0] = str(pair[0])
        r.append(pair)

    return r


def boxplot(basic_data):
    minimum = basic_data['Value Min']
    maximum = basic_data['Value Max']
    quartile_1 = basic_data['Value Quartile 1']
    quartile_3 = basic_data['Value Quartile 3']

    return ['', maximum, quartile_3, quartile_1, minimum]


def aux_pie_chart(counted_dic):
    return sorted(([str(k), v] for k, v in counted_dic.items()), key = lambda x: x[1], reverse=True)


def distribution(data_seq, basic_stats, amount=False):

    if amount:
        label = 'Amount'
        data_seq = Counter(data_seq).values()
    else:
        label = 'Value'

    mu = basic_stats[label + ' Mean']
    sigma = basic_stats[label + ' Standard deviation']

    label = label + ' distribution'

    normalized = [normalization(value, mu, sigma) for value in data_seq]

    bins = 10
    histogram = numpy.histogram(normalized, bins)
    total = histogram[0].sum()

    r = [['Sigma', 'Histogram', label, 'Normal distribution']]

    values = zip(histogram[0], histogram[1])

    for v, k in values:
        r.append([k, v / total, v/total, normal_distribution(k, 0, 1)])

    return r


def frequency_distance_scatter(compositions, small_nested_seq, coll_dic, norm=False):
    dist_seq = [get_frequency_distance(s, coll_dic) for s in small_nested_seq]
    if norm:
        arr = numpy.array(dist_seq)
        mu = arr.mean()
        sigma = arr.std()
        new = (arr - mu) / sigma
        dist_seq = new.tolist()
    zipped = zip(compositions, dist_seq)
    pairs = [[c.music_data.score.code, s] for c, s in zipped]
    pairs.insert(0, ['Composition', 'Value'])
    return pairs


def frequency_distance_scatter_group(compositions, freq_data, norm=False):
    main_pair = []
    header = ['Composition']

    for label, small_nested_seq, coll_dic in freq_data:
        header.append(label)
        dist_seq = [get_frequency_distance(s, coll_dic) for s in small_nested_seq]
        if norm:
            arr = numpy.array(dist_seq)
            mu = arr.mean()
            sigma = arr.std()
            new = (arr - mu) / sigma
            dist_seq = new.tolist()
        main_pair.append(dist_seq)

    main_pair = numpy.array(main_pair).transpose().tolist()
    seq = [header]

    for composition, data in zip(compositions, main_pair):
        code = composition.music_data.score.code
        data.insert(0, code)
        seq.append(data)

    return seq


# music functions #

def get_music_data_attrib(compositions, attrib, method='extend'):
    seq = []
    for composition in compositions:
        # seq.extend(getattr(composition.music_data, attrib))
        getattr(seq, method)(getattr(composition.music_data, attrib))
    return seq


def comparison(pair):
    a, b = pair
    return (a > b) - (a < b)


# cluster functions #

def _make_reachability_plot_data(array, min_pts=9):
    reachability_plot = amyxzhang.optics(array, min_pts)[0]
    return list(map(list, enumerate(reachability_plot)))


def make_reachability_plot(array, min_pts=9):
    reachability_plot = _make_reachability_plot_data(array, min_pts)

    reachability_plot.insert(0, ['Piece', 'Reachability value'])
    return reachability_plot


def make_reachability_and_order(array, min_pts=9):
    # run the OPTICS algorithm on the points, using a min_pts value (0 = no min_pts)
    reach_dist, core_dist, order = amyxzhang.optics(array, min_pts)
    reach_plot = []
    reach_points = []

    for item in order:
        reach_plot.append(reach_dist[item]) # Reachability Plot
        reach_points.append([array[item][0], array[item][1]]) # points in their order determined by OPTICS

    return reach_plot, reach_points, order


def get_optics_data(array, min_pts=9):
    reach_plot, reach_points, order = amyxzhang.order_reach_plot(array, min_pts)

    #hierarchically cluster the data
    root_node = amyxzhang.automatic_cluster(reach_plot, reach_points, order)

    #array of the TreeNode objects, position in the array is the TreeNode's level in the tree
    array = amyxzhang.get_array(root_node, 0, [0])

    #get only the leaves of the tree
    leaves = amyxzhang.get_leaves(root_node, [])

    return root_node, reach_plot, reach_points, leaves


def make_optics_plot_data(array, min_pts=9):
    root_node, reach_plot, reach_points, leaves = get_optics_data(array, min_pts)

    # graph the points and the leaf clusters that have been found by OPTICS

    leaves = sorted(leaves, key=lambda x: len(x.points), reverse=True)
    seq = []
    size = len(leaves)
    for n, leave in enumerate(leaves):
        for x, y in leave.points:
            row = ["null"] * size # add null string for google chart
            row[n] = y
            row.insert(0, x)
            seq.append(row)

    header = ['G{}'.format(str(n)) for n in range(1, size + 1)]
    header.insert(0, 'Z')
    seq.insert(0, header)

    return seq


def make_clusters(compositions, array, min_pts):
    leaves = get_optics_data(array, min_pts)[-1]

    clusters = []
    if not leaves: return clusters
    for leave_number, leave in enumerate(leaves):
        l_dic = {}
        l_dic['number'] = 'G' + str(leave_number + 1)
        l_dic['size'] = len(leave.order)
        songs = []
        for n in leave.order:
            composition = compositions[int(n)]
            title = composition.title
            code = composition.music_data.score.code
            length = composition.music_data.total_duration
            songs.append({'title': title, 'code': code, 'first': False, 'length': length})

        songs[0]['first'] = True
        l_dic['songs'] = songs


        clusters.append(l_dic)

    return clusters


