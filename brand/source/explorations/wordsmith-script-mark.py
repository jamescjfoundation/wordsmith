from shapely.geometry import LineString, box, Point, Polygon
from shapely import affinity
import math, sys

def mark(dx=34, H=118, w=27, hole_r=6.2, slit=2.6, hole_y=None):
    # symmetric twin-V: apex points at bottom, middle peak at top
    ext = 40
    k = dx/H
    pts = [(0-k*ext, -ext), (dx, H), (2*dx, -ext), (3*dx, H), (4*dx+k*ext, -ext)]
    ln = LineString(pts)
    g = ln.buffer(w/2, cap_style='flat', join_style='mitre', mitre_limit=20)
    g = g.intersection(box(-200, 0, 400, 400))
    # nib tips: find lowest points
    minx, miny, maxx, maxy = g.bounds
    cuts = []
    half = math.atan(k)
    miter = (w/2)/math.sin(half)
    for cx in (dx, 3*dx):
        inner_y = H - miter     # inner vertex (top of solid tip)
        tip_y = H + miter
        hy = hole_y if hole_y else inner_y + (tip_y-inner_y)*0.30
        cuts.append(Point(cx, hy).buffer(hole_r, 64))
        cuts.append(box(cx-slit/2, hy, cx+slit/2, tip_y+5))
    for c in cuts: g = g.difference(c)
    return g

def to_path(g, ox=0, oy=0, s=1):
    def ring(r):
        c = list(r.coords)
        return "M" + " L".join(f"{(x-ox)*s:.2f},{(y-oy)*s:.2f}" for x,y in c[:-1]) + "Z"
    geoms = getattr(g, 'geoms', [g])
    d = ""
    for p in geoms:
        d += ring(p.exterior) + "".join(ring(i) for i in p.interiors)
    return d

if __name__ == "__main__":
    g = mark()
    b = g.bounds
    print(b)
    d = to_path(g, b[0], b[1])
    W, Hh = b[2]-b[0], b[3]-b[1]
    open('mark_test.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -20 {W+40} {Hh+40}" width="600"><rect x="-20" y="-20" width="{W+40}" height="{Hh+40}" fill="#fff"/><path fill-rule="evenodd" fill="#1C2340" d="{d}"/></svg>')
