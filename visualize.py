from pylab import *
import os

# make a square figure and axes
def pie_chart(vLabels,vCounts,charTitle):
	figure(1, figsize=(16,16))
	#ax = axes([0.1, 0.1, 0.8, 0.8])

	# The slices will be ordered and plotted counter-clockwise.
	labels = vLabels
	fracs = vCounts
	#explode=(0, 0.05, 0, 0)

	pie(fracs, labels=labels,
					autopct='%1.1f%%', shadow=False, startangle=90)
					# The default startangle is 0, which would start
					# the Frogs slice on the x-axis.  With startangle=90,
					# everything is rotated counter-clockwise by 90 degrees,
					# so the plotting starts on the positive y-axis.

	title(charTitle, bbox={'facecolor':'0.8', 'pad':5})

	save('visualize/'+charTitle)

def save(path, ext='png', close=True, verbose=True):
	# Extract the directory and filename from the given path
	print path
	print os.path.split(path)[0]

	directory = os.path.split(path)[0]
	filename = "%s.%s" % (os.path.split(path)[1], ext)
	if directory == '':
		directory = '.'
	# If the directory does not exist, create it
	if not os.path.exists(directory):
		os.makedirs(directory)

	# The final path to save to
	savepath = os.path.join(directory, filename)

	if verbose:
		print("Figure saved to '%s'" % savepath)

	# Actually save the figure
	savefig(path)