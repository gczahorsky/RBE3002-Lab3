#!/usr/bin/env python

import rospy
from astar import aStar
from nav_msgs.msg import GridCells, Path
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Point, Pose, PoseStamped, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry, OccupancyGrid
from kobuki_msgs.msg import BumperEvent
import tf
import numpy
import math 
import rospy, tf, numpy, math

class Node:
	def __init__(self,value,point):
		self.value = value
		self.point = point
		self.parent = None
		self.H = 0
		self.G = 0
	def move_cost(self,other):
		return 0 if self.value == '.' else 1
		
	def children(point,grid):
		x,y = point.point
		links = [grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]]
		return [link for link in links if link.value != '%']

	def manhattan(point,point2):
		return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[0])

def getLowestF(openset):
	lowest = openSet[0]
	for i in range(0,len(openSet)):
		if( (i.G + i.H) < (lowest.G + lowest.H) ):
			lowest = i
	return lowest

def aStar(start, goal, grid):
	global resolution
	global offsetX
	global offsetY


	print "astar called"
	#The open and closed sets
	openset = set()
	closedset = set()
	#Current point is the starting point

	j = int((current.x - offsetX - (.5 * resolution)) / resolution)
	i = int((current.y - offsetY - (.5 * resolution)) / resolution)
	

	print "start"
	#Add the starting point to the open set
	openset.add(current)
	#While the open set is not empty





	print "In loop?"
	while openset:
		#Find the item in the open set with the lowest G + H score
		current = getLowestF(openset)
		#If it is the item we want, retrace the path and return it
		if current == goal:
			path = []
			while current.parent:
				path.append(current)
				current = current.parent
			path.append(current)
			return path[::-1]
		#Remove the item from the open set
		openset.remove(current)
		#Add it to the closed set
		closedset.add(current)


		print "here"

		print children(current,grid)


		#Loop through the node's children/siblings
		for node in children(current,grid):
			#If it is already in the closed set, skip it
			if node in closedset:
				continue
			#Otherwise if it is already in the open set
			if node in openset:
				#Check if we beat the G score 
				new_g = current.G + current.move_cost(node)
				if node.G > new_g:
					#If so, update the node to have a new parent
					node.G = new_g
					node.parent = current
			else:
				#If it isn't in the open set, calculate the G and H score for the node
				node.G = current.G + current.move_cost(node)
				node.H = manhattan(node, goal)
				#Set the parent to our current item
				node.parent = current
				#Add it to the set
				openset.add(node)
	#Throw an exception if there is no path
	raise ValueError('No Path Found')

def next_move(pacman,food,grid):
	#Convert all the points to instances of Node
	for x in xrange(len(grid)):
		for y in xrange(len(grid[x])):
			grid[x][y] = Node(grid[x][y],(x,y))
	#Get the path
	path = aStar(grid[pacman[0]][pacman[1]],grid[food[0]][food[1]],grid)
	#Output the path
	print len(path) - 1
	for node in path:
		x, y = node.point
		print x, y
	pacman_x, pacman_y = [ int(i) for i in raw_input().strip().split() ]
	food_x, food_y = [ int(i) for i in raw_input().strip().split() ]
	x,y = [ int(i) for i in raw_input().strip().split() ] 
	grid = []

	for i in xrange(0, x):
		grid.append(list(raw_input().strip()))
		next_move((pacman_x, pacman_y),(food_x, food_y), grid)
