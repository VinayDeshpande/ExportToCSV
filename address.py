import geocoder
l=[[12.971599, 77.594563],[5.850499, 14.499974],[47.606209, -122.332071],[31.968599, -99.901813]]
for i in range(len(l)):
	g=geocoder.bing(l[i], method='reverse')
	print g.address


