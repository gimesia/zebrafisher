

function mask = createCircMask(centerxy, width, height, r)

x = centerxy(1);
y = centerxy(2);

th = 0:pi/50:2*pi;
xunit = r * cos(th) + x;
yunit = r * sin(th) + y;

[xfit, yfit, Rfit] = circfit(xunit, yunit);

[x, y] = meshgrid(-(xfit-1):(width-xfit),-(yfit-1):(height-yfit));

mask = ((x .^ 2 + y .^ 2) <= Rfit^2);

end