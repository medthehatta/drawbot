import pytest

import numpy as np
import pygame
import geometry
import drawing

prec = 1e-12

def normsq(vec):
    return (vec**2).sum()

def norm(vec):
    return np.sqrt(normsq(vec))

def near(v1,v2):
    return norm(v2-v1) < prec

@pytest.fixture
def coordinates():
    c = geometry.CoordinateSystem()
    return c

def test_coord_trans(coordinates):
    c = coordinates
    c.angle = 90
    assert near(c.to_coords([1,0]), np.array([0,1]))
    c.angle = -90
    assert near(c.to_coords([1,0]), np.array([0,-1]))
    c.angle = 0
    assert near(c.to_coords([1,0]), np.array([1,0]))
    c.angle = 2
    expected = geometry.transform([1,0],angle=2)
    assert near(c.to_coords([1,0]), expected)

def test_inv_coord_trans(coordinates):
    c = coordinates
    c.angle = 90
    assert near(c.from_coords([0,1]), np.array([1,0]))
    c.angle = -90
    assert near(c.from_coords([0,-1]), np.array([1,0]))
    c.angle = 0
    assert near(c.from_coords([1,0]), np.array([1,0]))
    c.angle = 2
    expected = geometry.transform([1,0],angle=2)
    assert near(c.from_coords(expected), np.array([1,0]))

@pytest.fixture
def stacked_coords():
    c = geometry.CoordinateSystem()
    d = geometry.CoordinateSystem(parent=c)
    return (c,d)

def test_stacked_coords(stacked_coords):
    (c, d) = stacked_coords
    c.angle = 0
    assert near(d.to_coords([1,0],rel=True), np.array([1,0]))
    c.angle = 90
    assert near(d.to_coords([1,0],rel=True), np.array([0,1]))
    print('Doing nested test')
    d.angle = 90
    vec = d.to_coords([1,0],rel=True)
    assert near(vec, np.array([-1,0]))

@pytest.fixture
def canvas():
    c_rect = pygame.Rect(0,0,100,100)
    return drawing.Canvas(c_rect,pxres=72)

def test_canvas(canvas):
    c = canvas
    assert near(c.world_coords([0,1]), np.array([50,-22]))
    c.coords.scale = 10
    assert near(c.world_coords([0,1]), np.array([50,-670]))

@pytest.fixture
def stacked_canvases():
    c_rect = pygame.Rect(0,0,100,100)
    d_rect = pygame.Rect(0,0,100,100)
    c = drawing.Canvas(c_rect,pxres=72)
    d = drawing.Canvas(d_rect,pxres=72,parent=c)
    return (c,d)

def test_stacked_canvases(stacked_canvases):
    (c, d) = stacked_canvases
    c.coords.angle = 0
    assert near(d.world_coords([0,1]), np.array([50,-22]))
    c.coords.angle = 90
    assert near(d.world_coords([1,0],rel=True), np.array([50,-22]))
    print('Doing nested test')
    d.coords.angle = 90
    vec = d.world_coords([0,1],rel=True)
    assert near(vec, np.array([50,122]))

