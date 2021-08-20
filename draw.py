import numpy as np
import matplotlib.pyplot as plt
import json

def removeNumberFromStr(s):
    return ''.join([i for i in s if not i.isdigit()])

def getNameFromPath(p):
    return removeNumberFromStr(p.split('-')[-1])

datapaths = ['general0-mysql0-oltp_read_write1', 'general0-mysql0-oltp_delete2', 'general0-mysql0-oltp_read_only3', 'general0-mysql0-oltp_insert4', 'general0-mysql0-oltp_point_select5', 'general0-mysql0-oltp_update_index6', 'general0-mysql0-oltp_update_non_index7', 'general0-mysql0-oltp_write_only8', 'general0-mysql0-select_random_points9', 'general0-mysql0-select_random_ranges10']
datas = []
names = []
oltp_path = "./images/oltp"

for i in range(len(datapaths)):
    f = open("%s.json" % datapaths[i])
    d = json.load(f)
    if d != {}:
        datas.append(d)
        names.append(getNameFromPath(datapaths[i]))

# draw SQL statistics
x = np.arange(8)
total_width, n = 35, len(datas)
width = total_width / (n*8)
# x = x - (total_width - width) / 2
for i in range(len(datas)):
    name = names[i]
    plt.figure()
    plt.title("SQL statistics: %s" % name)
    labels = ["read", "write", "other", "total", "transactions", "queries", "ignored errors", "reconnects"]
    if datas[i] != {}:
        d = datas[i]["SQL statistics"]
        t = [
            d["queries performed"]["read"], d["queries performed"]["write"], d["queries performed"]["other"], d["queries performed"]["total"],
            d["transactions"], d["queries"], d["ignored errors"], d["reconnects"]
        ]
        print(t)
        bars = plt.bar(x, t, tick_label = labels,width=width,  label=name)
        plt.xticks(fontsize=6)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + 1000, yval, fontsize=6)
        plt.savefig("%s/SQL statistics/%s.png" % (oltp_path, name))

plt.show()

# draw Throughput graph
x = np.arange(3)
total_width, n = 35, len(datas)
width = total_width / (n*8)
for i in range(len(datas)):
    name = names[i]
    plt.figure()
    plt.title("Throughput: %s" % name)
    labels = ["events/s (eps)", "time elapsed (s)", "total number of events"]
    if datas[i] != {}:
        d = datas[i]["Throughput"]
        t = [
            d["events/s (eps)"], d["time elapsed (s)"], d["total number of events"]
        ]
        print(t)
        bars = plt.bar(x, t, tick_label = labels,width=width,  label=name)
        plt.xticks(fontsize=12)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval, yval, fontsize=10)
        plt.savefig("%s/Throughput/%s.png" % (oltp_path, name))
plt.show()


# Latency
x = np.arange(5)
total_width, n = 35, len(datas)
width = total_width / (n*8)
for i in range(len(datas)):
    name = names[i]
    plt.figure()
    plt.title("Latency: %s" % name)
    labels = ["min(ms)", "avg(ms)", "max(ms)", "95th percentile", "sum(ms)"]
    if datas[i] != {}:
        d = datas[i]["Latency"]
        t = [
            d["min(ms)"], d["avg(ms)"], d["max(ms)"], d["95th percentile"], d["sum(ms)"]
        ]
        print(t)
        bars = plt.bar(x, t, tick_label = labels,width=width,  label=name)
        plt.xticks(fontsize=10)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x()+0.02, yval, yval, fontsize=10)
        plt.savefig("%s/Latency/%s.png" % (oltp_path, name))
plt.show()



#
