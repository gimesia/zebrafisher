
function mask = getInnerROI(image)

global cw;
global ch;

[lehisto, ~] = imhist(image);
[level] = triangle_th(lehisto, 256);
threshImg = im2bw(image, level); %#ok<IM2BW>

if ~isempty(threshImg > 0)
    
    possBoundary = bwareafilt(threshImg, 1);
    [B, ~, N, A] = bwboundaries(possBoundary);
    
    boundary = 0;
    for k = 1:N
        if (nnz(A(:,k)) > 0)
            boundary = B{k};
        end
    end
    
    if boundary == 0
        [xCoords, yCoords] = getInnerCircle(possBoundary);
    else
        xCoords = boundary(:, 2);
        yCoords = boundary(:, 1);
    end
    
    [xfit, yfit, Rfit] = circfit(xCoords, yCoords);
    
    [x, y] = meshgrid(-(xfit-1):(cw-xfit),-(yfit-1):(ch-yfit));
    mask = ((x.^2+y.^2)<=Rfit^2);
    
else
    mask = zeros(size(image, 1), size(image, 2));
end

end

function [xCoords, yCoords] = getInnerCircle(image)

global cw;
global ch;

xCenter = floor(cw/2);
yCenter = floor(ch/2);
theta = 0:45:315;
radius = cw/2;

[startposX, startposY, endposX, endposY] = ...
    getCoordinates(xCenter, yCenter, theta, radius);

o = 1;

for i = 1 : size(startposX, 2)
    xline = [startposX(i), endposX(i)];
    yline = [startposY(i), endposY(i)];
    
    [cx, cy, c] = improfile(image, xline, yline);
    
    innerPos = find(c == 1);
    
    if ~isempty(innerPos)
        xCoords(o) = cx(innerPos(end));
        yCoords(o) = cy(innerPos(end));
        o = o + 1;
    end
end

end

function [startposX, startposY, endposX, endposY] ...
    = getCoordinates(xCenter, yCenter, theta, radius)

x = radius * cos(degtorad(theta)) + xCenter;
y = radius * sin(degtorad(theta)) + yCenter;

j = 1;
endposX = zeros(1, 8);
endposY = zeros(1, 8);
startposX = zeros(1, 8);
startposY = zeros(1, 8);

startposX(:) = xCenter;
startposY(:) = yCenter;

for i = 1 : size(x, 2)
    if i < 31
        endposX(j) = x(i);
        endposY(j) = y(i);
        j = j + 1;
    end
end

end

