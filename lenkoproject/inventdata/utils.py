import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.conf import settings
from django.views.generic import ListView, DetailView, DeleteView
from .models import ListData, EntryData, CSV
import base64
from io import BytesIO
from scipy.stats import zscore
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score, silhouette_samples
import numpy as np
import matplotlib.cm as cm
from sklearn_extra.cluster import KMedoids
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
from django.http import HttpResponseRedirect, FileResponse
import os

def get_graph():
	buffer= BytesIO()
	plt.savefig(buffer, format='png')
	buffer.seek(0)
	image_png = buffer.getvalue()
	graph= base64.b64encode (image_png)
	graph= graph.decode ("utf-8")
	buffer.close()
	return graph

def try_get_plot3 (request, xa,pk):
	listdata = ListData.objects.get(id=pk)
	if len(xa)>0:
		n_clusters=int(request.POST['nilaik'])
	   # Create a subplot with 1 row and 2 columns
		fig, (ax1, ax2) = plt.subplots(1, 2)
		fig.set_size_inches(10, 5)

	    # The 1st subplot is the silhouette plot
	    # The silhouette coefficient can range from -1, 1 but in this example all
	    # lie within [-0.1, 1]
		ax1.set_xlim([-0.1, 1])
	    # The (n_clusters+1)*10 is for inserting blank space between silhouette
	    # plots of individual clusters, to demarcate them clearly.
		ax1.set_ylim([0, len(xa) + (n_clusters + 1) * 10])

	    # Initialize the clusterer with n_clusters value and a random generator
	    # seed of 10 for reproducibility.
		KM_5_clusters = KMedoids(n_clusters=n_clusters, init='k-medoids++', random_state=0).fit(xa)
		clusterer = KMedoids(n_clusters=n_clusters, random_state=0, init='k-medoids++')
		cluster_labels = KM_5_clusters.labels_
		c_labels = clusterer.fit_predict(xa)

		silhouette_avg = silhouette_score(xa, cluster_labels)
	    #print("For n_clusters =", n_clusters,
	         # "The average silhouette_score is :", silhouette_avg)
	    # Compute the silhouette scores for each sample
		sample_silhouette_values = silhouette_samples(xa, c_labels)

		y_lower = 10
		for i in range(n_clusters):
	        # Aggregate the silhouette scores for samples belonging to
	        # cluster i, and sort them
			ith_cluster_silhouette_values = \
				sample_silhouette_values[cluster_labels == i]

			ith_cluster_silhouette_values.sort()

			size_cluster_i = ith_cluster_silhouette_values.shape[0]
			y_upper = y_lower + size_cluster_i

			cmap=cm.get_cmap("seismic")
			color = cmap(float(i) / n_clusters)
			ax1.fill_betweenx(np.arange(y_lower, y_upper),
	                          0, ith_cluster_silhouette_values,
	                          facecolor=color, edgecolor=color, alpha=0.7)

	        # Label the silhouette plots with their cluster numbers at the middle
			ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

	        # Compute the new y_lower for next plot
			y_lower = y_upper + 10  # 10 for the 0 samples

		ax1.set_title("The silhouette plot for the various clusters.")
		ax1.set_xlabel("The silhouette coefficient values")
		ax1.set_ylabel("Cluster label")

	    # The vertical line for average silhouette score of all the values
		ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

		ax1.set_yticks([])  # Clear the yaxis labels / ticks
		ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

	    # 2nd Plot showing the actual clusters formed
		cmap=cm.get_cmap("seismic")
		colors = cmap(cluster_labels.astype(float) / n_clusters)
		ax2.scatter(xa.iloc[:, 0], xa.iloc[:, 1], marker='.', s=30, lw=0, alpha=0.7,
	                c=colors, edgecolor='k')

	    # Labeling the clusters

		centers = KM_5_clusters.cluster_centers_
	    # Draw white circles at cluster centers
		ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
	                c="white", alpha=1, s=200, edgecolor='k')

		for i, c in enumerate(centers):
			ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
	                    s=50, edgecolor='k')

		ax2.set_title("The visualization of the clustered data.")
		ax2.set_xlabel("Feature space for the 1st feature")
		ax2.set_ylabel("Feature space for the 2nd feature")

		plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
	                  "with n_clusters = %d" % n_clusters),
	                 fontsize=14, fontweight='bold')

#		my_path = os.chdir("/media/reports/chart") # Figures out the absolute path for you in case your working directory moves around.
		file_name =  listdata.nama_list + str(listdata.id)+request.user.username+"analisis 3"+ ".png"
		plt.savefig(os.path.join(settings.MEDIA_ROOT, file_name), dpi=100)
		plt.tight_layout()
		graph= get_graph()
	else:
		fig = plt.figure()
		fig.set_size_inches(10, 5)
		file_name = listdata.nama_list + str(listdata.id)+request.user.username+"analisis 3"+ ".png"
		plt.savefig(os.path.join(settings.MEDIA_ROOT, file_name), dpi=100)
		graph= get_graph()
	return graph

def try_get_plot2 (request, xa,pk):
	listdata = ListData.objects.get(id=pk)
	if len(xa)>0:
		n_clusters=int(request.POST['nilaik'])
	   # Create a subplot with 1 row and 2 columns
		fig, (ax1, ax2) = plt.subplots(1, 2)
		fig.set_size_inches(10, 5)

	    # The 1st subplot is the silhouette plot
	    # The silhouette coefficient can range from -1, 1 but in this example all
	    # lie within [-0.1, 1]
		ax1.set_xlim([-0.1, 1])
	    # The (n_clusters+1)*10 is for inserting blank space between silhouette
	    # plots of individual clusters, to demarcate them clearly.
		ax1.set_ylim([0, len(xa) + (n_clusters + 1) * 10])

	    # Initialize the clusterer with n_clusters value and a random generator
	    # seed of 10 for reproducibility.
		KM_5_clusters = KMedoids(n_clusters=n_clusters, init='k-medoids++', random_state=0).fit(xa)
		clusterer = KMedoids(n_clusters=n_clusters, random_state=0, init='k-medoids++')
		cluster_labels = KM_5_clusters.labels_
		c_labels = clusterer.fit_predict(xa)

		silhouette_avg = silhouette_score(xa, cluster_labels)
	    #print("For n_clusters =", n_clusters,
	         # "The average silhouette_score is :", silhouette_avg)
	    # Compute the silhouette scores for each sample
		sample_silhouette_values = silhouette_samples(xa, c_labels)

		y_lower = 10
		for i in range(n_clusters):
	        # Aggregate the silhouette scores for samples belonging to
	        # cluster i, and sort them
			ith_cluster_silhouette_values = \
				sample_silhouette_values[cluster_labels == i]

			ith_cluster_silhouette_values.sort()

			size_cluster_i = ith_cluster_silhouette_values.shape[0]
			y_upper = y_lower + size_cluster_i

			cmap=cm.get_cmap("seismic")
			color = cmap(float(i) / n_clusters)
			ax1.fill_betweenx(np.arange(y_lower, y_upper),
	                          0, ith_cluster_silhouette_values,
	                          facecolor=color, edgecolor=color, alpha=0.7)

	        # Label the silhouette plots with their cluster numbers at the middle
			ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

	        # Compute the new y_lower for next plot
			y_lower = y_upper + 10  # 10 for the 0 samples

		ax1.set_title("The silhouette plot for the various clusters.")
		ax1.set_xlabel("The silhouette coefficient values")
		ax1.set_ylabel("Cluster label")

	    # The vertical line for average silhouette score of all the values
		ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

		ax1.set_yticks([])  # Clear the yaxis labels / ticks
		ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

	    # 2nd Plot showing the actual clusters formed
		cmap=cm.get_cmap("seismic")
		colors = cmap(cluster_labels.astype(float) / n_clusters)
		ax2.scatter(xa.iloc[:, 0], xa.iloc[:, 1], marker='.', s=30, lw=0, alpha=0.7,
	                c=colors, edgecolor='k')

	    # Labeling the clusters

		centers = KM_5_clusters.cluster_centers_
	    # Draw white circles at cluster centers
		ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
	                c="white", alpha=1, s=200, edgecolor='k')

		for i, c in enumerate(centers):
			ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
	                    s=50, edgecolor='k')

		ax2.set_title("The visualization of the clustered data.")
		ax2.set_xlabel("Feature space for the 1st feature")
		ax2.set_ylabel("Feature space for the 2nd feature")

		plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
	                  "with n_clusters = %d" % n_clusters),
	                 fontsize=14, fontweight='bold')

#		my_path = os.chdir("/media/reports/chart") # Figures out the absolute path for you in case your working directory moves around.
		file_name = listdata.nama_list + str(listdata.id)+request.user.username+"analisis 2"+".png"
		plt.savefig(os.path.join(settings.MEDIA_ROOT, file_name), dpi=100)
		plt.tight_layout()
		graph= get_graph()
	else:
		fig = plt.figure()
		fig.set_size_inches(10, 5)
		file_name = listdata.nama_list + str(listdata.id)+request.user.username+"analisis 2"+".png"
		plt.savefig(os.path.join(settings.MEDIA_ROOT, file_name), dpi=100)
		graph= get_graph()
	return graph



def try_get_plot (request, xa,pk):
	listdata = ListData.objects.get(id=pk)
	if len(xa)>0:
		n_clusters=int(request.POST['nilaik'])
	   # Create a subplot with 1 row and 2 columns
		fig, (ax1, ax2) = plt.subplots(1, 2)
		fig.set_size_inches(10, 5)

	    # The 1st subplot is the silhouette plot
	    # The silhouette coefficient can range from -1, 1 but in this example all
	    # lie within [-0.1, 1]
		ax1.set_xlim([-0.1, 1])
	    # The (n_clusters+1)*10 is for inserting blank space between silhouette
	    # plots of individual clusters, to demarcate them clearly.
		ax1.set_ylim([0, len(xa) + (n_clusters + 1) * 10])

	    # Initialize the clusterer with n_clusters value and a random generator
	    # seed of 10 for reproducibility.
		KM_5_clusters = KMedoids(n_clusters=n_clusters, init='k-medoids++', random_state=0).fit(xa)
		clusterer = KMedoids(n_clusters=n_clusters, random_state=0, init='k-medoids++')
		cluster_labels = KM_5_clusters.labels_
		c_labels = clusterer.fit_predict(xa)

		silhouette_avg = silhouette_score(xa, cluster_labels)
	    #print("For n_clusters =", n_clusters,
	         # "The average silhouette_score is :", silhouette_avg)
	    # Compute the silhouette scores for each sample
		sample_silhouette_values = silhouette_samples(xa, c_labels)

		y_lower = 10
		for i in range(n_clusters):
	        # Aggregate the silhouette scores for samples belonging to
	        # cluster i, and sort them
			ith_cluster_silhouette_values = \
				sample_silhouette_values[cluster_labels == i]

			ith_cluster_silhouette_values.sort()

			size_cluster_i = ith_cluster_silhouette_values.shape[0]
			y_upper = y_lower + size_cluster_i

			cmap=cm.get_cmap("seismic")
			color = cmap(float(i) / n_clusters)
			ax1.fill_betweenx(np.arange(y_lower, y_upper),
	                          0, ith_cluster_silhouette_values,
	                          facecolor=color, edgecolor=color, alpha=0.7)

	        # Label the silhouette plots with their cluster numbers at the middle
			ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

	        # Compute the new y_lower for next plot
			y_lower = y_upper + 10  # 10 for the 0 samples

		ax1.set_title("The silhouette plot for the various clusters.")
		ax1.set_xlabel("The silhouette coefficient values")
		ax1.set_ylabel("Cluster label")

	    # The vertical line for average silhouette score of all the values
		ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

		ax1.set_yticks([])  # Clear the yaxis labels / ticks
		ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

	    # 2nd Plot showing the actual clusters formed
		cmap=cm.get_cmap("seismic")
		colors = cmap(cluster_labels.astype(float) / n_clusters)
		ax2.scatter(xa.iloc[:, 0], xa.iloc[:, 1], marker='.', s=30, lw=0, alpha=0.7,
	                c=colors, edgecolor='k')

	    # Labeling the clusters

		centers = KM_5_clusters.cluster_centers_
	    # Draw white circles at cluster centers
		ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
	                c="white", alpha=1, s=200, edgecolor='k')

		for i, c in enumerate(centers):
			ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
	                    s=50, edgecolor='k')

		ax2.set_title("The visualization of the clustered data.")
		ax2.set_xlabel("Feature space for the 1st feature")
		ax2.set_ylabel("Feature space for the 2nd feature")

		plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
	                  "with n_clusters = %d" % n_clusters),
	                 fontsize=14, fontweight='bold')

#		my_path = os.chdir("/media/reports/chart") # Figures out the absolute path for you in case your working directory moves around.
		file_name = listdata.nama_list + str(listdata.id)+request.user.username+".png"
		plt.savefig(os.path.join(settings.MEDIA_ROOT, file_name), dpi=100)
		plt.tight_layout()
		graph= get_graph()
	else:
		fig = plt.figure()
		fig.set_size_inches(10, 5)
		file_name = listdata.nama_list + str(listdata.id)+request.user.username+".png"
		plt.savefig(os.path.join(settings.MEDIA_ROOT, file_name), dpi=100)
		graph= get_graph()
	return graph

def get_plot (xa,pk):
	listdata = ListData.objects.get(id=pk)
	if len(xa)>0:
		n_clusters=5
	   # Create a subplot with 1 row and 2 columns
		fig, (ax1, ax2) = plt.subplots(1, 2)
		fig.set_size_inches(10, 5)

	    # The 1st subplot is the silhouette plot
	    # The silhouette coefficient can range from -1, 1 but in this example all
	    # lie within [-0.1, 1]
		ax1.set_xlim([-0.1, 1])
	    # The (n_clusters+1)*10 is for inserting blank space between silhouette
	    # plots of individual clusters, to demarcate them clearly.
		ax1.set_ylim([0, len(xa) + (n_clusters + 1) * 10])

	    # Initialize the clusterer with n_clusters value and a random generator
	    # seed of 10 for reproducibility.
		KM_5_clusters = KMedoids(n_clusters=n_clusters, init='k-medoids++', random_state=0).fit(xa)
		clusterer = KMedoids(n_clusters=n_clusters, random_state=0, init='k-medoids++')
		cluster_labels = KM_5_clusters.labels_
		c_labels = clusterer.fit_predict(xa)

		silhouette_avg = silhouette_score(xa, cluster_labels)
	    #print("For n_clusters =", n_clusters,
	         # "The average silhouette_score is :", silhouette_avg)
	    # Compute the silhouette scores for each sample
		sample_silhouette_values = silhouette_samples(xa, c_labels)

		y_lower = 10
		for i in range(n_clusters):
	        # Aggregate the silhouette scores for samples belonging to
	        # cluster i, and sort them
			ith_cluster_silhouette_values = \
				sample_silhouette_values[cluster_labels == i]

			ith_cluster_silhouette_values.sort()

			size_cluster_i = ith_cluster_silhouette_values.shape[0]
			y_upper = y_lower + size_cluster_i

			cmap=cm.get_cmap("seismic")
			color = cmap(float(i) / n_clusters)
			ax1.fill_betweenx(np.arange(y_lower, y_upper),
	                          0, ith_cluster_silhouette_values,
	                          facecolor=color, edgecolor=color, alpha=0.7)

	        # Label the silhouette plots with their cluster numbers at the middle
			ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

	        # Compute the new y_lower for next plot
			y_lower = y_upper + 10  # 10 for the 0 samples

		ax1.set_title("The silhouette plot for the various clusters.")
		ax1.set_xlabel("The silhouette coefficient values")
		ax1.set_ylabel("Cluster label")

	    # The vertical line for average silhouette score of all the values
		ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

		ax1.set_yticks([])  # Clear the yaxis labels / ticks
		ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

	    # 2nd Plot showing the actual clusters formed
		cmap=cm.get_cmap("seismic")
		colors = cmap(cluster_labels.astype(float) / n_clusters)
		ax2.scatter(xa.iloc[:, 0], xa.iloc[:, 1], marker='.', s=30, lw=0, alpha=0.7,
	                c=colors, edgecolor='k')

	    # Labeling the clusters

		centers = KM_5_clusters.cluster_centers_
	    # Draw white circles at cluster centers
		ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
	                c="white", alpha=1, s=200, edgecolor='k')

		for i, c in enumerate(centers):
			ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
	                    s=50, edgecolor='k')

		ax2.set_title("The visualization of the clustered data.")
		ax2.set_xlabel("Feature space for the 1st feature")
		ax2.set_ylabel("Feature space for the 2nd feature")

		plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
	                  "with n_clusters = %d" % n_clusters),
	                 fontsize=14, fontweight='bold')

#		my_path = os.chdir("/media/reports/chart") # Figures out the absolute path for you in case your working directory moves around.
		file_name = listdata.nama_list + str(listdata.id)+".png"
		plt.savefig(os.path.join(settings.MEDIA_ROOT, file_name), dpi=100)
		plt.tight_layout()
		graph= get_graph()
	else:
		fig = plt.figure()
		fig.set_size_inches(10, 5)
		file_name = listdata.nama_list + str(listdata.id)+".png"
		plt.savefig(os.path.join(settings.MEDIA_ROOT, file_name), dpi=100)
		graph= get_graph()
	return graph

def get_plot2 (xo, xb):
	if len(xb)>0:
		n_clusters=5
	   # Create a subplot with 1 row and 2 columns
		fig, (ax1, ax2) = plt.subplots(1, 2)
		fig.set_size_inches(10, 5)

	    # The 1st subplot is the silhouette plot
	    # The silhouette coefficient can range from -1, 1 but in this example all
	    # lie within [-0.1, 1]
		ax1.set_xlim([-0.1, 1])
	    # The (n_clusters+1)*10 is for inserting blank space between silhouette
	    # plots of individual clusters, to demarcate them clearly.
		ax1.set_ylim([0, len(xb) + (n_clusters + 1) * 10])

	    # Initialize the clusterer with n_clusters value and a random generator
	    # seed of 10 for reproducibility.
		KM_5_clusters = KMedoids(n_clusters=n_clusters, init='k-medoids++', random_state=0).fit(xb)
		clusterer = KMedoids(n_clusters=n_clusters, random_state=0, init='k-medoids++')
		cluster_labels = KM_5_clusters.labels_
		c_labels = clusterer.fit_predict(xb)

		silhouette_avg = silhouette_score(xb, cluster_labels)
	    #print("For n_clusters =", n_clusters,
	         # "The average silhouette_score is :", silhouette_avg)
	    # Compute the silhouette scores for each sample
		sample_silhouette_values = silhouette_samples(xb, c_labels)

		y_lower = 10
		for i in range(n_clusters):
	        # Aggregate the silhouette scores for samples belonging to
	        # cluster i, and sort them
			ith_cluster_silhouette_values = \
				sample_silhouette_values[cluster_labels == i]

			ith_cluster_silhouette_values.sort()

			size_cluster_i = ith_cluster_silhouette_values.shape[0]
			y_upper = y_lower + size_cluster_i

			cmap=cm.get_cmap("Spectral")
			color = cmap(float(i) / n_clusters)
			ax1.fill_betweenx(np.arange(y_lower, y_upper),
	                          0, ith_cluster_silhouette_values,
	                          facecolor=color, edgecolor=color, alpha=0.7)

	        # Label the silhouette plots with their cluster numbers at the middle
			ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

	        # Compute the new y_lower for next plot
			y_lower = y_upper + 10  # 10 for the 0 samples

		ax1.set_title("The silhouette plot for the various clusters.")
		ax1.set_xlabel("The silhouette coefficient values")
		ax1.set_ylabel("Cluster label")

	    # The vertical line for average silhouette score of all the values
		ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

		ax1.set_yticks([])  # Clear the yaxis labels / ticks
		ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

	    # 2nd Plot showing the actual clusters formed
		colors = cmap(cluster_labels.astype(float) / n_clusters)
		ax2.scatter(xo.iloc[:, 0], xo.iloc[:, 1], marker='.', s=30, lw=0, alpha=0.7,
	                c=colors, edgecolor='k')

	    # Labeling the clusters

		centers = KM_5_clusters.cluster_centers_
	    # Draw white circles at cluster centers
		ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
	                c="white", alpha=1, s=200, edgecolor='k')

		for i, c in enumerate(centers):
			ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
	                    s=50, edgecolor='k')

		ax2.set_title("The visualization of the clustered data.")
		ax2.set_xlabel("Feature space for the 1st feature")
		ax2.set_ylabel("Feature space for the 2nd feature")

		plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
	                  "with n_clusters = %d" % n_clusters),
	                 fontsize=14, fontweight='bold')

		plt.savefig('sv2.png', dpi=100, figsize=(3,4))
		plt.tight_layout()
		graph= get_graph()
	else:
		fig, (ax1, ax2) = plt.subplots(1, 2)
		fig.set_size_inches(10, 5)
		graph= get_graph()		
	return graph


def generate_pdf(request):

	buffer = io.BytesIO()

	doc = SimpleDocTemplate('test')
	
	story = []

	doc.build(story)

	response = FileResponse(buffer.getvalue())

	return response