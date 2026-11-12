"""Display-only figures for Lab 6's inference workflow.

Inputs are already-computed scores, sample means and interval rows. These
helpers never draw samples, change seeds, estimate intervals, or select
replications because of their results. Images carry descriptions for HTML
and notebook exports. Pillow is the only graphics dependency.
"""
from __future__ import annotations

import math
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from l6_figures import _font, _text, _linewrap, INK, MUTED, GRID

BLUE = '#176b93'
GREEN = '#32745b'
RUST = '#a34d34'
PURPLE = '#6b5a9b'


def _finite(values):
    values = np.asarray(values, dtype=float).reshape(-1)
    return values[np.isfinite(values)]


def _limits(values, truth=None, padding=.08):
    values = _finite(values)
    if truth is not None and np.isfinite(truth):
        values = np.append(values, float(truth))
    if not len(values):
        return (-.5, .5)
    lo, hi = float(values.min()), float(values.max())
    span = hi-lo
    if span <= 0:
        span = max(abs(lo)*.1, .1)
    return lo-padding*span, hi+padding*span


def _number(value, span):
    if span >= 10:
        return f'{value:.1f}'.rstrip('0').rstrip('.')
    if span >= 1:
        return f'{value:.2f}'.rstrip('0').rstrip('.')
    return f'{value:.3f}'.rstrip('0').rstrip('.')


def _dashed_vertical(draw, x, top, bottom, fill=INK, width=2):
    for y in range(int(top), int(bottom), 12):
        draw.line((x,y,x,min(y+7,bottom)),fill=fill,width=width)


def _histogram(draw, data, box, *, title, observation_label, xlabel,
               xlim=None, bins=25, color=BLUE, truth=None, y_max=None):
    """Draw a count histogram. A missing/nonfinite observation is disclosed."""
    panel_left, top, panel_right, bottom = box
    left, right = panel_left+50, panel_right-15
    raw = np.asarray(data,dtype=float).reshape(-1)
    values = _finite(raw)
    _linewrap(draw,(panel_left,top-105),title,panel_right-panel_left,23,INK,spacing=4)
    _text(draw,(panel_left,top-47),observation_label,18,fill=MUTED)
    _text(draw,(panel_left,top-23),f'{len(values):,} finite observations'+
          (f'; {len(raw)-len(values)} unavailable' if len(values)!=len(raw) else ''),17,fill=MUTED)
    if xlim is None:
        xlim=_limits(values,truth)
    lo,hi=xlim
    if hi <= lo:
        raise ValueError('Histogram axis must have positive width.')
    edges=np.linspace(lo,hi,bins+1) if np.isscalar(bins) else np.asarray(bins,dtype=float)
    counts,edges=np.histogram(values,bins=edges)
    # All supplied finite observations must fit; silently clipping a tail is forbidden.
    if counts.sum()!=len(values):
        raise ValueError('Histogram axis excludes a finite observation.')
    ymax = max(int(counts.max()) if len(counts) else 0, 1) if y_max is None else max(int(y_max),1)
    x=lambda value:left+(value-lo)/(hi-lo)*(right-left)
    y=lambda value:bottom-value/ymax*(bottom-top)
    for count in sorted(set([0,int(math.ceil(ymax/2)),ymax])):
        yp=y(count)
        draw.line((left,yp,right,yp),fill=GRID,width=1)
        _text(draw,(left-9,yp),str(count),17,anchor='rm',fill=MUTED)
    for count,a,b in zip(counts,edges[:-1],edges[1:]):
        if count:
            draw.rectangle((x(a)+.5,y(int(count)),x(b)-.5,bottom),fill=color,outline='white')
    if truth is not None and np.isfinite(truth):
        _dashed_vertical(draw,x(truth),top,bottom)
    draw.line((left,top,left,bottom,right,bottom),fill=INK,width=2)
    for tick in np.linspace(lo,hi,5):
        xp=x(tick)
        draw.line((xp,bottom,xp,bottom+6),fill=INK,width=1)
        _text(draw,(xp,bottom+12),_number(tick,hi-lo),17,anchor='mt')
    _linewrap(draw,(left,bottom+49),xlabel,right-left,19,INK,spacing=4)
    if not len(values):
        _text(draw,((left+right)/2,(top+bottom)/2),'No finite observations',20,anchor='mm')


def sampling_figure(scores, means75, means300, units, label, truth=None):
    """Individual scores versus repeated means; mean panels share both axes.

    ``scores`` is the selected n=75 sample, not a second resampled dataset.
    ``means75``/``means300`` are the precomputed repeated-sample means.
    The optional truth line denotes the fixed fictional eligible-roster mean.
    """
    im=Image.new('RGB',(1560,790),'white'); d=ImageDraw.Draw(im)
    _linewrap(d,(35,24),f'{label}: individual variation and uncertainty in a mean',1490,31,INK,spacing=3)
    _text(d,(35,95),'Fictional data | Same eligible roster; different units of observation',20,fill=MUTED)
    individual=_finite(scores); m75=_finite(means75); m300=_finite(means300)
    combined=np.concatenate([m75,m300])
    common=_limits(combined,truth)
    common_edges=np.linspace(*common,26)
    common_max=max(np.histogram(m75,common_edges)[0].max(),np.histogram(m300,common_edges)[0].max(),1)
    if len(individual) and np.all(individual==np.floor(individual)):
        low=min(0,float(individual.min())); high=float(individual.max())
        if 'ACE' in label.upper() or 'categor' in units.lower():high=max(high,10)
        edges=np.arange(low-.5,high+1.5,1); score_axis=(float(edges[0]),float(edges[-1]))
    elif len(individual) and individual.min()>=0 and individual.max()<=1:
        edges=np.linspace(0,1,11); score_axis=(0.,1.)
    else:
        score_axis=_limits(individual); edges=np.linspace(*score_axis,16)
    panels=[(35,290,495,575),(550,290,1010,575),(1065,290,1525,575)]
    _histogram(d,scores,panels[0],title='Individual scores in one sample',
        observation_label='Count: participants',xlabel=units,xlim=score_axis,bins=edges,color=BLUE)
    _histogram(d,means75,panels[1],title='Repeated sample means | n=75',
        observation_label='Count: samples',xlabel=f'Mean ({units})',xlim=common,bins=common_edges,color=GREEN,truth=truth,y_max=common_max)
    _histogram(d,means300,panels[2],title='Repeated sample means | n=300',
        observation_label='Count: samples',xlabel=f'Mean ({units})',xlim=common,bins=common_edges,color=PURPLE,truth=truth,y_max=common_max)
    _linewrap(d,(35,690),'Left: SD describes differences among people. Middle and right: the spread of sample means describes sampling variability. The two mean panels share horizontal and vertical scales.',1490,20,INK)
    if truth is not None:
        _text(d,(35,755),'Dashed line: fixed eligible-roster mean, known only because this is a teaching population.',18,fill=MUTED)
    im.info['description']=(f'{label}. Count histograms of {len(np.asarray(scores))} individual scores, '
        f'{len(np.asarray(means75))} repeated means at n=75 and {len(np.asarray(means300))} repeated means at n=300. '
        'Mean panels share axes. Individual-score SD and sampling spread describe different observations.')
    return im


def interval_figure(simulations, truth, units, label, max_rows=40):
    """Plot the first rows in their existing order; never select hits or misses.

    Required columns: mean, SE, lower, upper, valid. Undefined rows are shown
    explicitly and are not discarded from the displayed-row count.
    """
    required={'mean','SE','lower','upper','valid'}
    if not required.issubset(simulations.columns):raise ValueError('Interval rows lack required columns.')
    if max_rows<1:raise ValueError('max_rows must be positive.')
    rows=simulations.iloc[:max_rows].copy()
    n=len(rows);height=max(590,310+n*18+140)
    im=Image.new('RGB',(1180,height),'white');d=ImageDraw.Draw(im)
    _linewrap(d,(35,22),f'{label}: repeated 95% intervals',1110,30,INK,spacing=4)
    _text(d,(35,88),'Fictional data | Supplied interval rows in their original order',19,fill=MUTED)
    _text(d,(35,126),f'First {n} of {len(simulations):,} attempts — this subset is not the full coverage calculation.',20)
    _text(d,(35,165),'Blue line + circle: contains truth   Rust line + X: misses   Gray !: undefined',19,fill=MUTED)
    valid=rows['valid'].fillna(False).astype(bool)
    # Do not hide invalid finite-status inconsistencies; only bounds of valid rows set the axis.
    numbers=np.concatenate([rows.loc[valid,'lower'].to_numpy(float),rows.loc[valid,'upper'].to_numpy(float)])
    lo,hi=_limits(numbers,truth,padding=.12)
    left,right=125,1010;top=240;bottom=top+max(n-1,1)*18
    x=lambda v:left+(float(v)-lo)/(hi-lo)*(right-left)
    _dashed_vertical(d,x(truth),top-20,bottom+15,width=3)
    _text(d,(x(truth),top-29),f'Roster mean {truth:.3f}',18,anchor='mb')
    hit=miss=undefined=0
    for i,(_,r) in enumerate(rows.iterrows()):
        y=top+i*18
        if i==0 or (i+1)%5==0:_text(d,(left-18,y),str(i+1),14,anchor='rm',fill=MUTED)
        usable=bool(r['valid']) and np.isfinite(r['lower']) and np.isfinite(r['upper'])
        if not usable:
            undefined+=1
            _text(d,(right+18,y),'! undefined',14,anchor='lm',fill=MUTED)
            continue
        covered=float(r['lower'])<=truth<=float(r['upper'])
        color=BLUE if covered else RUST
        if covered:hit+=1
        else:miss+=1
        xa,xb=x(r['lower']),x(r['upper']);xm=x(r['mean'])
        d.line((xa,y,xb,y),fill=color,width=2)
        d.line((xa,y-3,xa,y+3),fill=color,width=1);d.line((xb,y-3,xb,y+3),fill=color,width=1)
        if covered:d.ellipse((xm-3,y-3,xm+3,y+3),fill=color)
        else:
            d.line((xm-4,y-4,xm+4,y+4),fill=color,width=2);d.line((xm-4,y+4,xm+4,y-4),fill=color,width=2)
    axis_y=bottom+27
    d.line((left,axis_y,right,axis_y),fill=INK,width=2)
    for tick in np.linspace(lo,hi,6):
        xp=x(tick);d.line((xp,axis_y,xp,axis_y+5),fill=INK,width=1)
        _text(d,(xp,axis_y+10),_number(tick,hi-lo),16,anchor='mt')
    _linewrap(d,(left,axis_y+43),f'Population mean in {units}',right-left,19,INK,spacing=4)
    footer=max(axis_y+90,height-83)
    _text(d,(35,footer),f'Shown: {hit} contain the roster mean; {miss} miss; {undefined} undefined.',20)
    _text(d,(35,footer+34),'Use the full results table for coverage. A real sample-based study usually would not know the target mean.',18,fill=MUTED)
    im.info['description']=(f'{label}: first {n} of {len(simulations)} attempted 95% intervals in original order, '
        f'{hit} cover the known fictional mean, {miss} miss and {undefined} are undefined. '
        'The figure is a fixed subset, not the full empirical coverage calculation.')
    return im


def smoking_figure(values, sim75, sim300, truth):
    """Display the supplied flower roster and interval-simulation sample means.

    Uses the same simulated draws as the coverage table; no additional
    sampling or outcome manipulation occurs here. Legitimate zeros remain.
    """
    for sim in [sim75,sim300]:
        if 'mean' not in sim:raise ValueError('Smoking simulation requires a mean column.')
    means75=sim75['mean'].to_numpy(float);means300=sim300['mean'].to_numpy(float)
    im=Image.new('RGB',(1560,790),'white');d=ImageDraw.Draw(im)
    _text(d,(35,24),'Smoked flower: outcome shape and the distribution of sample means',31,True)
    _text(d,(35,84),'Fictional data | Same draws as the conditions coverage table',20,fill=MUTED)
    _linewrap(d,(35,124),'This narrower product measure is a conditions demonstration. It is not an independent inference choice; genuine nonuse zeros remain in every calculation.',1490,20,INK)
    common=_limits(np.concatenate([_finite(means75),_finite(means300)]),truth)
    edges=np.linspace(*common,26)
    maximum=max(np.histogram(_finite(means75),edges)[0].max(),np.histogram(_finite(means300),edges)[0].max(),1)
    panels=[(35,295,495,575),(550,295,1010,575),(1065,295,1525,575)]
    _histogram(d,values,panels[0],title='Usable smoked-flower roster',observation_label='Count: participants',
        xlabel='Smoked-flower days in 30 days',xlim=(-.5,30.5),bins=np.arange(-.5,31.5,1),color=RUST)
    _histogram(d,means75,panels[1],title='Sample means | n=75',observation_label='Count: samples',
        xlabel='Mean smoked-flower days',xlim=common,bins=edges,color=BLUE,truth=truth,y_max=maximum)
    _histogram(d,means300,panels[2],title='Sample means | n=300',observation_label='Count: samples',
        xlabel='Mean smoked-flower days',xlim=common,bins=edges,color=PURPLE,truth=truth,y_max=maximum)
    _linewrap(d,(35,690),'Mean panels share both axes. Dashed line: fixed roster mean. Inspect these shapes together with coverage, directional misses and undefined intervals in the accompanying table.',1490,20,INK)
    _text(d,(35,755),'A larger n does not by itself establish adequate interval coverage.',18,fill=MUTED)
    im.info['description']=(f'Count histograms for {len(np.asarray(values))} usable smoked-flower values and '
        f'{len(sim75)} / {len(sim300)} supplied sample means at n=75 / n=300. '
        'True zeros retained; sample-mean panels share axes and show the fixed roster mean.')
    return im
