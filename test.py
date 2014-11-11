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

@pytest.fixture
def coordinates():
    c = geometry.CoordinateSystem()
    return c

def test_coord_trans(coordinates):
    c = coordinates
    c.angle = 90
    assert norm(c.from_coords([1,0]) - np.array([0,1])) < prec
    c.angle = -90
    assert norm(c.from_coords([1,0]) - np.array([0,-1])) < prec
    c.angle = 0
    assert norm(c.from_coords([1,0]) - np.array([1,0])) < prec
    c.angle = 2
    expected = geometry.transform([1,0],angle=2)
    assert norm(c.from_coords([1,0]) - expected) < prec

def test_inv_coord_trans(coordinates):
    c = coordinates
    c.angle = 90
    assert norm(c.to_coords([0,1]) - np.array([1,0])) < prec
    c.angle = -90
    assert norm(c.to_coords([0,-1]) - np.array([1,0])) < prec
    c.angle = 0
    assert norm(c.to_coords([1,0]) - np.array([1,0])) < prec
    c.angle = 2
    expected = geometry.transform([1,0],angle=2)
    assert norm(c.to_coords(expected) - np.array([1,0])) < prec

@pytest.fixture
def stacked_canvases():
    cr = pygame.Rect(0,0,100,100)
    dr = pygame.Rect(0,0,100,100)

    c = drawing.Canvas(cr)
    d = drawing.Canvas(dr, parent=c)
    return (c,d)

def test_canvas_coords(stacked_canvases):
    (c, d) = stacked_canvases
    c.angle = 0
    assert norm(c.canvas_coords([1,0],rel=True) - np.array([1,0])) < prec
    c.angle = 90
    assert norm(c.canvas_coords([1,0],rel=True) - np.array([0,1])) < prec

def test_stacked_canvas_coords(stacked_canvases):
    (c, d) = stacked_canvases
    c.angle = 0
    assert norm(d.world_coords([1,0],rel=True) - np.array([1,0])) < prec
    c.angle = 90
    assert norm(d.world_coords([1,0],rel=True) - np.array([0,1])) < prec
    print('Doing nested test')
    d.angle = 90
    vec = d.world_coords([1,0],rel=True)
    assert norm(vec - np.array([-1,0])) < prec

