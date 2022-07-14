

function fishBodySkel = fittingCurve4FishSkel(skeleton, head, partialResults, newXY)

possSkeleton = skeleton;

prHead = partialResults{1};
partHNum = size(prHead, 2);

prTail = partialResults{2};
partTNum = size(prTail, 2);

[~, w] = size(skeleton);

half = floor(w / 2);

if strcmp(head, 'r')
    
    headPart = skeleton(:, half:end);
    if partHNum > 1
        partHeadImg = prHead{partHNum - 1};
        partHeadImg = partHeadImg(:, half:end);
    else
        partHeadImg = headPart;
    end
    
    [hp, wp] = size(headPart);
    fittedPartHead = fitHeadCurve(headPart, wp, hp, partHeadImg, newXY, head);
    possSkeleton(:, half:end) = fittedPartHead;
    
    tailPart = skeleton(:, 1:half);
    if partTNum > 2
        partTailImg = prTail{partHNum - 1};
        partTailImg = partTailImg(:, 1:half);
    else
        partTailImg = tailPart;
    end
    
    [hp, wp] = size(tailPart);
    fittedPartTail = fitTailCurve(tailPart, wp, hp, partTailImg, head);
    possSkeleton(:, 1:half) = fittedPartTail;
    
else
    
    headPart = skeleton(:, 1:half);
    if partHNum > 1
        partHeadImg = prHead{partHNum - 1};
        partHeadImg = partHeadImg(:, 1:half);
    else
        partHeadImg = skeleton;
    end
    
    [hp, wp] = size(headPart);
    partHeadImg = partHeadImg(:, 1:half);
    fittedPartHead = fitHeadCurve(headPart, wp, hp, partHeadImg, newXY, head);
    possSkeleton(:, 1:half) = fittedPartHead;
    
    tailPart = skeleton(:, half:end);
    if partTNum > 2
        partTailImg = prTail{partHNum - 1};
        partTailImg = partTailImg(:, half:end);
    else
        partTailImg = tailPart;
    end
    
    [hp, wp] = size(tailPart);
    fittedPartTail = fitTailCurve(tailPart, wp, hp, partTailImg, head);
    possSkeleton(:, half:end) = fittedPartTail;
    
end

fishBodySkel = possSkeleton;

% figure; imshow(possSkeleton);
% hold on;
% visboundaries(skeleton);

end


function headCurve = fitHeadCurve(data, width, height, partHeadImg, newXY, head)

tempData = bwareafilt(data, 1);
[ty, tx] = find(tempData > 0);

partTempData = bwareafilt(partHeadImg, 1);
% TODO - szar
if nnz(partTempData) == 0
    partTempData(floor(size(data, 1)/2):floor(size(data, 1)/2), :) = 1;
end
[pty, ptx] = find(partTempData > 0);

if strcmp(head, 'r')
    tempXY = [tx(end), ty(end)];
    partTempXY = [ptx(end), pty(end)];
    [useAnotherSkel, dist] = pointsDistanceExam(tempXY, newXY, partTempXY);
else
    tempXY = [tx(1), ty(1)];
    partTempXY = [ptx(1), pty(1)];
    [useAnotherSkel, dist] = pointsDistanceExam(tempXY, newXY, partTempXY);
end

if strcmp(useAnotherSkel, 'true')
    data = partHeadImg;
end

[~, x] = find(data > 0);

if dist > 50
    frange = dist + 50;
else
    frange = 50;
end

if frange > width
    frange = floor(width / 2) ;
end

if strcmp(head, 'r')
    skelPoint = x(end-1);
    eyePoint = x(end);
    if skelPoint - frange > 1
        chData = data(:, skelPoint-frange:eyePoint);
    else
        chData = data(:, 1:eyePoint);
    end
else
    skelPoint = x(2);
    eyePoint = x(1);
    if skelPoint + frange < width
        chData = data(:, eyePoint:skelPoint+frange);
    else
        chData = data(:, eyePoint:width);
    end
end

eVal = abs(eyePoint-skelPoint);

partResult = lineFitting(chData, height);

partHeadCurve = data;

if strcmp(head, 'r')
    partHeadCurve(:, skelPoint+1:eyePoint) = ....
        partResult(:, size(partResult, 2)-eVal+1:size(partResult, 2));
else
    partHeadCurve(:, eyePoint:skelPoint) =  partResult(:, 1:1+eVal);
end

partHeadCurve = postLineFitProc(partHeadCurve, 7);

[~, x2] = find(partHeadCurve);
frange = 30;
if strcmp(head, 'r')
    lstPoint = x2(end);
    chData = partHeadCurve(:, lstPoint-frange:width);
    eVal = abs(lstPoint - width);
else
    lstPoint = x2(1);
    chData = partHeadCurve(:, 1:lstPoint+frange);
    eVal = abs(lstPoint - 1);
end

partResult = lineFitting(chData, height);

if strcmp(head, 'r')
    partHeadCurve(:, lstPoint+1:width) = ....
        partResult(:, size(partResult, 2)-eVal+1:size(partResult, 2));
else
    partHeadCurve(:, 1:lstPoint) =  partResult(:, 1:1+eVal);
end

headCurve = postLineFitProc(partHeadCurve, 7);

% figure; imshow(headCurve);
% hold on; visboundaries(data)

end


function tailCurve = fitTailCurve(data, width, height, partTailImg, head)

[y, x] = find(data > 0);
[py, px] = find(partTailImg > 0);

if strcmp(head, 'r')
    tempXY = [x(1), y(1)];
    partTempXY = [px(1), py(1)];
else
    tempXY = [x(end), y(end)];
    partTempXY = [px(end), py(end)];
end

dist = pdist2(tempXY, partTempXY);

if dist > 40
    lstPoint = partTempXY(1);
    data = partTailImg;
else
    lstPoint = tempXY(1);
end

frange = 50;
if frange > width
    frange = floor(width / 2) ;
end

if strcmp(head, 'r')
    if lstPoint + frange < width
        chData = data(:, 1:lstPoint+frange);
    else
        frange = abs(width - lstPoint);
        chData = data(:, 1:lstPoint+frange);
    end
    eVal = abs(lstPoint-1);
else
    if lstPoint - frange < 0
        frange = abs(lstPoint - 1);
        chData = data(:, lstPoint-frange:width);
    else
        chData = data(:, lstPoint-frange:width);
    end
    eVal = abs(width-lstPoint);
end

partResult = lineFitting(chData, height);

partTailCurve = data;

if strcmp(head, 'l')
    partTailCurve(:, max(x)+1:width) = partResult(:, size(partResult, 2)-eVal+1:size(partResult, 2));
else
    if size(partTailCurve(:, 1:min(x)), 1) ~=  size(partResult(:, 1:1+eVal), 1) | ...
        size(partTailCurve(:, 1:min(x)), 2) ~=  size(partResult(:, 1:1+eVal), 2)
        [ph, pw] = size(partTailCurve(:, 1:min(x))); 
        partTailCurve(:, 1:min(x)) = false(ph, pw);
    else
        partTailCurve(:, 1:min(x)) = partResult(:, 1:1+eVal);
    end
end

[curved, newSkel] = curveFishExamination(data, head);

if strcmp(curved, 'true')
    tailCurve = newSkel;
else
    tailCurve = postLineFitProc(partTailCurve, 0);
end
% figure; imshow(partTailCurve);

end


function [useAnotherSkel, dist] = pointsDistanceExam(skelXY, eyeXY, prTempXY)

point1 = [skelXY(1), skelXY(2)];
point2 = [eyeXY(1), eyeXY(2)];
point3 = [prTempXY(1), prTempXY(2)];

origDist = pdist2(point1, point2);
lstStepDist = pdist2(point2, point3);

if origDist > 50
    if lstStepDist < origDist
        useAnotherSkel = 'true';
        dist = lstStepDist;
    else
        useAnotherSkel = 'false';
        dist = origDist;
    end
else
    useAnotherSkel = 'false';
    dist = origDist;
end

end


function partResult = lineFitting(chData, height)

x4fit = 1:size(chData, 2);
x4fit = x4fit';

[yR, xR] = find(chData);

coeffs = polyfit(xR, yR, 1);
fittedY = polyval(coeffs, x4fit);
partResult = zeros(size(chData, 1), size(chData, 2));

fittedY = floor(fittedY);
fittedY(fittedY <= 0) = 1;

for i = 1 :  size(chData, 2)
    if fittedY(i) <= height
        partResult(fittedY(i), x4fit(i)) = 1;
    else
        partResult(height, x4fit(i)) = 1;
    end
end

end


function postCurve = postLineFitProc(image, spurTh)

se = strel('disk', 14);
postCurve = imclose(image, se);
postCurve = bwmorph(postCurve, 'thin', 'Inf');
postCurve = bwmorph(postCurve, 'spur', spurTh);
% postCurve = bwareafilt(postCurve, 1);

end


function [extraCurved, resultImg] = curveFishExamination(image, head)

extraCurved = 'false';

[y, x] = find(image > 0); 

if strcmp(head, 'r')
%     maxX = x(1);
    maxY = y(1);
else
%     maxX = x(end);
    maxY = x(end);
end

tempImg = image;
tempImg(1:floor(maxY), :) = 0;

% TODO, hogy ha oldalra gorbe, akkor arra illesszunk gorbet
if strcmp(checkEmptyImageOrNot(tempImg), 'true')
    [ty, tx] = find(tempImg > 0);
    yDist = abs(ty(end) - ty(1));
    skelNumbs = nnz(tempImg);
    
    if yDist > 40 & tx(end) ~= size(tempImg, 2)
        resultImg = image;
        resultImg(ty(end):size(image, 1), tx(end):tx(end)) = 1;
        extraCurved = 'true';
    elseif skelNumbs > 40 && yDist  < 40
        %TODO
        resultImg = image;
    else
        resultImg = image;
    end
else
    resultImg = image;
end

% figure; imshow(resultImg);

end




