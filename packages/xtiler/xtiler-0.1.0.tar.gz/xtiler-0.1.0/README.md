# Hexa-tiling
Coordinate system for tiling with hexagons.

## What does the grid look like?

![Explaining illustration](images/illustration.jpg)

## How does it work?

### Rings and angles
The grid can be viewed as accumulation of concentric **rings**.
On the image, the **origin** is labelled 0,
surrounded by the **ring #1** composed of tiles 1-6,
surrounded by the **ring #2** composed of tiles 7-18.

### Numbering
Tiles are numbered from 0, in increasing order, starting at the
**origin** (center of the grid), spiraling around the **origin**,
with the first tile of each **ring** at 0°.

### Coordinates
Polar coordinates can be used to find a tile.
Each tile has a **radius** and an **angle**.

- The **radius** is the distance to the **origin**,
corresponding to the rank of the **ring** the tile belongs to.
- The **angle**, in degrees, is measured between the direction
"noon" (or "up", "north", etc) and the position of the tile.

## The maths behind it

### Ring length (Perimeter)
Let the ring length be $P$ and its rank $n$.

$$P(0) = 1$$

$$P(1) = 6$$

$$\forall n > 1, \quad P(n) = 2P(n-1)$$

$$\forall n > 0, \quad P(n) = 6 * 2^{n-1}$$

### Grid size (Area)
Let the number of tiles for a grid with $n$ rings be $A$.

$$A(n) = \sum^{n}_{i = 0}{P(i)}$$

$$= 1 + \sum^{n}_{i = 1}{6 * 2^{i-1}}$$

$$= 1 + 6 * \sum^{n-1}_{i = 0}{2^{i}}$$

$$= 1 + 6 * (2^n - 1)$$

$$= 6 * 2^n - 5$$

### Number from coordinates
Let the number of a tile be $X$, its radius $n$ and its angle $\alpha$.

$$X(0, \alpha) = 0$$

$$\forall n > 0, \quad  X(n, \alpha) = A(n - 1) + \frac{\alpha}{360}P(n)$$

$$= 6 * 2^{n-1} - 5 + \frac{\alpha}{360}*6 * 2^{n-1}$$

$$= 6 * 2^{n-1}(1 + \frac{\alpha}{360}) -5$$

### Radius
To find the radius $n$ given the number $X$:

$$X = 0 \Leftrightarrow n = 0$$

$$0 \le \alpha < 360$$

$$\implies \forall n > 0, \quad X(n, 0) \quad \le \quad X(n,\alpha) \quad < \quad X(n, 360)$$

$$\implies \forall n > 0, \quad A(n - 1) + \frac{0}{360}P(n) \quad \le \quad X \quad < \quad A(n - 1) + \frac{360}{360}P(n)$$

$$\implies \forall n > 0, \quad A(n - 1) \quad \le \quad X \quad < \quad A(n - 1) + P(n) = A(n)$$

$$\implies \forall n > 0, \quad 6 * 2^{n-1} - 5 \quad \le \quad X \quad < \quad 6 * 2^n - 5$$

$$\implies \forall n > 0, \quad 2^{n-1} \quad \le \quad \frac{X + 5}{6} \quad < \quad 2^n$$

$$\implies \forall n > 0, \quad n-1 \quad \le \quad \log _2(\frac{X + 5}{6}) \quad < \quad n$$

$$\implies \forall n > 0, \quad n = \lfloor \log _2(\frac{X + 5}{6}) \rfloor + 1$$

### Angle
Tile 0 has no angle.

$$\forall n > 0, \quad X(n, \alpha) = 6 * 2^{n-1}(1 + \frac{\alpha}{360}) -5$$

$$X + 5 = 6 * 2^{n-1}(1 + \frac{\alpha}{360})$$

$$\frac{X + 5}{6 * 2^{n-1}} = 1 + \frac{\alpha}{360}$$

$$360(\frac{X + 5}{6 * 2^{n-1}} - 1) = \alpha$$

$$360(\frac{X + 5}{6 * 2^{\lfloor \log _2(\frac{X + 5}{6}) \rfloor + 1-1}} - 1) = \alpha$$

$$360(\frac{X + 5}{6 * 2^{\lfloor \log _2(\frac{X + 5}{6}) \rfloor }} - 1) = \alpha$$
