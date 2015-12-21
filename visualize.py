from pylab import *
import os

# make a square figure and axes
def pie_chart(vLabels,vCounts,charTitle):
	figure(1, figsize=(6,6))
	#ax = axes([0.1, 0.1, 0.8, 0.8])

	# The slices will be ordered and plotted counter-clockwise.
	labels = vLabels
	fracs = vCounts
	#explode=(0, 0.05, 0, 0)

	pie(fracs, labels=labels,
					autopct='%1.1f%%', shadow=True, startangle=90)
					# The default startangle is 0, which would start
					# the Frogs slice on the x-axis.  With startangle=90,
					# everything is rotated counter-clockwise by 90 degrees,
					# so the plotting starts on the positive y-axis.

	title(charTitle, bbox={'facecolor':'0.8', 'pad':5})

	save('visualize/'+charTitle)

def save(path, ext='png', close=True, verbose=True):
	"""
	Save a figure from pyplot.
	Parameters
	----------
	path : string
		The path (and filename, without the extension) to save the
		figure to.
	ext : string (default='png')
		The file extension. This must be supported by the active
		matplotlib backend (see matplotlib.backends module).  Most
		backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.
	close : boolean (default=True)
		Whether to close the figure after saving.  If you want to save
		the figure multiple times (e.g., to multiple formats), you
		should NOT close it in between saves or you will have to
		re-plot it.
	verbose : boolean (default=True)
		Whether to print information about when and where the image
		has been saved.
	"""
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
		print("Saving figure to '%s'..." % savepath)

	# Actually save the figure
	pylab.savefig(savepath)