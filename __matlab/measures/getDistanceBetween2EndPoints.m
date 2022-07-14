

function endPointsProps = getDistanceBetween2EndPoints(skelProps, image, head, fishProps)

global cw;
global ch;

fittedCurve = skelProps.EPLstSkel;
contImg = bwperim(image);

se = strel('disk', 3);
fittedCurve = imdilate(fittedCurve, se);

ePointImg = zeros(size(image, 1), size(image, 2));
ePointImg(fittedCurve & contImg) = 1;

[ye, xe] = find(ePointImg > 0);

% TODO rekurzio?
if numel(xe) < 2
    if strcmp(head, 'r')
        coords = [1, floor(ch/2), cw, floor(ch/2)];
    else
        coords = [cw, floor(ch/2), 1, floor(ch/2)];
    end
else
    coords = getPointPos([ye, xe], head);
end

hx = coords(1);
hy = coords(2);
tx = coords(3);
ty = coords(4);
if strcmp(head, 'r')
    if abs(hx - tx) < 20
        hx = cw;
        hy = floor(ch/2);
    end
else
    if abs(hx - tx) < 20
        hx = 1;
        hy = floor(ch/2);
    end
end

X = [hx, hy; tx, ty];
dist = pdist(X, 'euclidean');

endPointsProps.endDist = dist;
endPointsProps.points = X;
endPointsProps.endImage = ePointImg;

% se = strel('disk', 3);
% ePointImg = imdilate(ePointImg, se);

% figure; imshow(image);
% hold on; visboundaries(ePointImg);

end


function endPointsCoord = getPointPos(points, head)

x = points(:, 2);
y = points(:, 1);

if strcmp(head, 'r')
    tailPosX = max(x);
    txPos = find(tailPosX == x, 1);
    tailPosY = y(txPos);
    
    headPosX = min(x);
    hxPos = find(headPosX == x, 1);
    headPosY = y(hxPos);
else
    tailPosX = min(x);
    txPos = find(tailPosX == x, 1);
    tailPosY = y(txPos);
    
    headPosX = max(x);
    hxPos = find(headPosX == x, 1);
    headPosY = y(hxPos);
end

endPointsCoord = [headPosX, headPosY, tailPosX, tailPosY];

end