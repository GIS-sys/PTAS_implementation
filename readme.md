# How to run

Change input points directly in main.py, then run

```python main.py```

# Plan of proof of algorithm

(the step-by-step description of algorithm for now can be found if you start reading comments in main.py and go into every package on the way)

1) moving and scaling points while preprocessing obviously do not change the approximation factor of algorithm

2) rounding while preprocessing changes optimal length in not more than 1+1/n times (lemma 2.1 in paper (1))

*) def: Imagine dissecting LxL square into 1x1 squares, starting with 1 LxL square and cutting each square into 4 smaller ones on each step;
let square be at level k (0<=k<=log2(L)) if it has appeared on the kth step of dissection

*) def: let line be at level k (1<=k<=log2(L)) if it has been used to divide square of level (k-1) into 4 smaller squares;
sides of square LxL are defined to be lines at level 0

*) def: let's call a system of 4*M points on sides of a square S at level k "M-portals" if they are uniformly spaced
with 4 of them positioned in corners of the square S (so there are M-1 portals on each side, not counting portals in corners);
also let's suppose that M is a power of 2, so portals of square S at level k are also portals of smaller squares

3) Let's make 4 assumptions;

a) points are on the grid LxL and optimum path length is not less than L (obvious after preprocessing - LxL square is the smallest square that contains points)

b) the tour enters and exits only through portals

c) the tour enters/exits through each portal no more than c=O(1) times (imagine it being c mini-portals very close to each other, each one being crossed at most once)

d) the tour is not self-intersecting in terms of mini-portals

as was said in step 2, assumption a) increases optimal tour length not more than by 1+1/n times; for other assumption similar result is shown in chapter 4 in paper (1)

4) find optimal algorithm using DP (under assumptions): ??????????????????????????????????????????????????????????????????????????

# Source paper

(1) http://viswa.engin.umich.edu/wp-content/uploads/sites/169/2019/03/9.pdf

(2) https://users.exa.unicen.edu.ar/catedras/aydalgo2/docs/AroraTSP.pdf

