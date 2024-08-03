#__author__ = "magnelPy"

####################
## MODULE IMPORTS ##
####################

import re
import numpy as np


########################################
## POSTPROCESS HEAT TRANSFER ANALYSIS ##
########################################

def read_TEM(file):
	"""
	Extract temperature for each timestep from a SAFIR TEM output file.

	Parameters:
		file (str): The path to the TEM file.

	Returns:
		tuple: A tuple containing two numpy arrays: (ts, Ts).
			- ts (ndarray): 1D numpy array of timestamps.
			- Ts (ndarray): 1D numpy array of temperature values corresponding to the timestamps.
	"""
	f=open(file, "rt")
	lines = [l for l in f]
	f.close()
	
	# timesteps 'ts'
	lines_ts = search_string_in_file(lines,'TIME=')
	
	ts = [float(re.findall(r"[-+]?(?:\d*\.*\d+)", lines[l])[0]) for l in lines_ts]
	Ts = [float(re.findall(r"[-+]?(?:\d*\.*\d+)", lines[l+2])[1]) for l in lines_ts]
	
	return np.array(ts), np.array(Ts)


#####################################
## POSTPROCESS MECHANICAL ANALYSIS ##
#####################################

def get_displacements(file,node=0,DOF=1):
	"""
	Extract displacement data from a SAFIR XML output file.

	Parameters:
		file (str): The path to the SAFIR XML output file.
		node (int, optional): The node index for which displacement data is to be extracted (default is 0).
		DOF (int, optional): The degree of freedom for which displacement data is to be extracted (default is 1).

	Returns:
		tuple: A tuple containing two numpy arrays: (ts, u).
			- ts (ndarray): 1D numpy array of timestamps.
			- u (ndarray): 1D numpy array of displacements corresponding to the specified node and degree of freedom.
	"""
	
	f=open(file, "rt")
	lines = [l for l in f]
	f.close()

	# timesteps 'ts'
	lines_ts = search_string_in_file(lines,'<STEP>')
	ts = [float(re.findall(r"[-+]?(?:\d*\.*\d+)", lines[l+1])[1]) for l in lines_ts]
	
	u = []

	for i in range(len(ts)):
		if i < len(ts)-1:
			lines_step = lines[lines_ts[i]:lines_ts[i+1]]
		else:
			lines_step = lines[lines_ts[i]:]

		# BEAM nodes (7 DOF)
		b_nds = search_string_in_file(lines_step,'<ND format="I1">7</ND>')
		# SHELL nodes (6 DOF)
		s_nds = search_string_in_file(lines_step,'<ND format="I1">6</ND>')
		# AUX nodes (1 DOF)
		a_nds = search_string_in_file(lines_step,'<ND format="I1">1</ND>')
		# AUX nodes 2 (0 DOF) not clear what these are --> RF?
		o_nds = search_string_in_file(lines_step,'<ND format="I1">0</ND>')
		
		# merged list of all nodes
		nds = b_nds + s_nds + a_nds + o_nds
		
		u.append(float(lines_step[nds[node]+1+DOF][3:-5]))
		
	return np.array(ts), np.array(u)


def get_beam_forces(file,beam=0,value='N',G=1):
	"""
	Extract beam forces data from a SAFIR XML output file.

	Parameters:
		file (str): The path to the SAFIR XML output file.
		beam (int, optional): The beam element index for which force data is to be extracted (default is 0).
		value (str, optional): The type of force to extract ('N' for axial force, 'Mz' for bending moment about the local z-axis) (default is 'N').
		G (int, optional): The point of Gauss for the beam element (default is 1).

	Returns:
		tuple: A tuple containing two numpy arrays: (ts, out).
			- ts (ndarray): 1D numpy array of timestamps.
			- out (ndarray): 1D numpy array of beam forces corresponding to the specified value and beam element.
	"""

	f=open(file, "rt")
	lines = [l for l in f]
	f.close()

	# timesteps 'ts'
	lines_ts = search_string_in_file(lines,'<STEP>')
	ts = [float(re.findall(r"[-+]?(?:\d*\.*\d+)", lines[l+1])[1]) for l in lines_ts]
	
	out = []

	for i in range(len(ts)):
		if i < len(ts)-1:
			lines_step = lines[lines_ts[i]:lines_ts[i+1]]
		else:
			lines_step = lines[lines_ts[i]:]

		# BEAM elements (7 DOF)
		b_elms = search_string_in_file(lines_step,' <BM>')
		
		if value == 'N':
			out.append(float(lines_step[b_elms[beam]+2][3:-5]))
		if value == 'Mz':
			out.append(float(lines_step[b_elms[beam]+3][4:-6]))
	
	return np.array(ts), np.array(out)



###################
## AUX FUNCTIONS ##
###################

def search_string_in_file(lines, string_to_search, startline = 0):
	"""
	Search for a given string in a list of lines (representing a file) and return the line numbers
	where the string occurs, along with the lines themselves.

	Parameters:
		lines (list): A list of strings representing lines of text in a file.
		string_to_search (str): The string to search for within the lines.
		startline (int, optional): The line number to start searching from (default is 0).

	Returns:
		list: A list containing tuples of line numbers and lines where the given string was found.
	"""
	line_number = 0
	list_of_results = []
	for line in lines:
		if line_number >= startline:
			if string_to_search in line: list_of_results.append(line_number)
		line_number += 1
	return list_of_results