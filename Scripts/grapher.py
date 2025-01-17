import os, math, json

from bokeh.layouts import row,column
from bokeh.charts import Histogram, output_file, show, HeatMap, bins,Bar
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from collections import Counter

#length of packet responses



def main():
	ipids = []
	ttls = []
	responses = []
	blocked, allowed, total, errors = 0,0,0,0
	seen_domains = []
	metadatafile = open("../metadata.txt",'w')
	print("Beginning file walk")
	for subdir, dirs, files in os.walk("../Results"):
		print("Now in: ",subdir)
		for file in files:
			data = json.load(open(subdir+"/"+file))
			domains = data["domains"]
			blocked+=data["meta"]["blocked"]
			allowed+=data["meta"]["allowed"]
			total+=data["meta"]["tried"]
			errors+=data["meta"]["errors"]
			for k,v in domains.items():
				if k not in seen_domains:
					seen_domains.append(k)
					ipid = domains[k]["ipid"]
					ipids.append(ipid)
					ttl = domains[k]["ttl"]
					ttls.append(ttl)
					response = domains[k]["responses"]
					responses.append(response)
				else:
					total-=1
					blocked-=1

	
	output_file("../Figures/graphs.html")
	p1 = Histogram(ipids,title="IPID Distribution")
	p1.xaxis.axis_label = "IPID Values"
	p1.yaxis.axis_label = "Count"

	p2 = Histogram(ttls,title="TTL Distribution")
	p2.xaxis.axis_label = "TTL Values"
	p2.yaxis.axis_label = "Count"

	p3 = Histogram(responses,title="Response Number")
	p3.xaxis.axis_label = "Number of Responses"
	p3.yaxis.axis_label = "Count"
	print()
	categories = ["blocked","allowed"]
	print("current stats")
	print("-------------")
	quants = [blocked,allowed]
	print("blocked: ",blocked)
	metadatafile.write("blocked: %d\n" %blocked)
	metadatafile.write("allowed: %d\n" %allowed)
	metadatafile.write("tried: %d\n" %total)
	metadatafile.write("errors: %d\n" %blocked)	
	print("allowed: ",allowed)
	print("total: ",total)
	print("errors: ",errors)
	p4 = figure(x_range=categories,title="Blocked vs Allowed")
	p4.vbar(x=categories,top=quants,width=0.3)

	cnt = Counter(ttls)
	print("top 5 ttls (most common, frequency)",cnt.most_common(5))
	metadatafile.write("top 5 ttls (most common, frequency)\n")
	metadatafile.write(str(cnt.most_common(5)))
	p5 = figure(x_range=["April 2014","April 2018"],title="April 2014 v April 2018")
	p5.vbar(x=["April 2014", "April 2018"],top=[35332,blocked],width=0.3)
	metadatafile.close()
	#hmdata = {"ttl":ttls,"ipids":ipids}
	#p3 = HeatMap(hmdata,x=bins("ipids"),y=bins("ttl"),stat='mean')
	show(column(row(p1,p2),row(p3,p4),row(p5)))







if __name__ == '__main__':
	main()
