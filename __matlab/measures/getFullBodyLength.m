

function fullBodySkelProps = getFullBodyLength(image, fishProps, eyeProps)

global cw;
global ch;

bodySkeletonImage = zeros(ch, cw); 
bodySkeletonImageEP = zeros(ch, cw); 
bodySkeletonImageEPLst = zeros(ch, cw);

head = fishProps.head;
tail = fishProps.tail;

[objThinHead, objThinPartHead] = getThinnedImg(image, head);
[objThinTail, objThinPartTail] = getThinnedImg(image, tail);

partialResults = {objThinPartHead, objThinPartTail};

[h, w] = size(objThinHead);

half = floor(w/2);

fishThin = false(h, w);

if strcmp(head, 'r')
    fishThin(:, half:end) = objThinHead(:, half:end);
    fishThin(:, 1:half-1) = objThinTail(:, 1:half-1);
    
else
    fishThin(:, 1:half-1) = objThinHead(:, 1:half-1);
    fishThin(:, half:end) = objThinTail(:, half:end);
end

[modFishSkel, newXYPos] = ...
    getPlusHeadAndTailPoint4Fitting(fishThin, fishProps, eyeProps, head);

fishSkeleton = fittingCurve4FishSkel(modFishSkel, head, partialResults, newXYPos);

modFishSkel = complSkeleton(fishSkeleton);
modFishSkel = modFishSkel(:, 1:w);
fishSkeleton = fishSkeleton(:, 1:w);

modFishSkel = logical(modFishSkel);

eyeNum = eyeProps.eyesNum;

% TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!! valamiert nagyobb kep lesz, de a
% fishSkel is mar fura
onlyFishSkeleton = false(h, w);
if eyeNum ~= 2
    modFishSkelP = postMod4BodyLength(image, eyeProps, modFishSkel, head);       
    if size(modFishSkelP, 1) * size(modFishSkelP, 2) ~= w*h
        onlyFishSkeleton(modFishSkelP & image) = 1;
    else
        onlyFishSkeleton(modFishSkelP & image) = 1;
    end
    modFishSkel = modFishSkelP;
else
    if size(modFishSkel, 1) * size(modFishSkel, 2) ~= w*h
        onlyFishSkeleton(modFishSkel & image) = 1;
    else
        onlyFishSkeleton(modFishSkel & image) = 1;
    end
end

props = regionprops(onlyFishSkeleton, 'Area');

x1 = fishProps.bbox(1);
y1 = fishProps.bbox(2);
x2 = fishProps.bbox(3);
y2 = fishProps.bbox(4);

tempSkel = onlyFishSkeleton;
temp4EPSkel = modFishSkel;
temp4EPSkelLst = fishSkeleton;

if strcmp(fishProps.rotated, 'true')
    tempSkel = imrotate(tempSkel, 90);
    temp4EPSkel = imrotate(temp4EPSkel, 90);
    temp4EPSkelLst = imrotate(temp4EPSkelLst, 90);
end

bodySkeletonImage(y1:y2, x1:x2) = tempSkel;
bodySkeletonImageEP(y1:y2, x1:x2) = temp4EPSkel;
bodySkeletonImageEPLst(y1:y2, x1:x2) = temp4EPSkelLst;

fullBodySkelProps.skeleton = onlyFishSkeleton;
fullBodySkelProps.skel4Endpoints = modFishSkel;
fullBodySkelProps.length = props.Area;
fullBodySkelProps.origSizeSkeleton = bodySkeletonImage;
fullBodySkelProps.origSkel4Endpoints = bodySkeletonImageEP;
% TODO fentebbre pakolni!!
fullBodySkelProps.EPLstSkel = bodySkeletonImageEPLst;
% figure; imshow(image);
% hold on; visboundaries(onlyFishSkeleton);

end


function modSkeleton = complSkeleton(skeleton)

ePoints = bwmorph(skeleton, 'endpoints');

ePoints(:, 1:10) = 0;
ePoints(:, end-10:end) = 0;

[ey, ex] = find(ePoints > 0);

if ~isempty(ex) && size(ex, 2) > 2
    x1 = ex(1); 
    y1 = ey(1);
    x2 = ex(end);
    y2 = ey(end);
    
    drawLineImg = insertShape(uint8(skeleton), 'Line', [x1 y1 x2 y2],'LineWidth', 1, 'Color','white');
    if size(drawLineImg, 3) > 1
        drawLineImg = rgb2gray(drawLineImg);
        drawLineImg = drawLineImg > 0;
    end
    modSkeleton = skeleton + drawLineImg;
else
    modSkeleton = skeleton;
end

end


function [modObjThin, threshSpur, partialThin] = thinCleaning(objThin, head, threshSpur, itNum, partialThin)

bPoints = bwmorph(objThin, 'branchpoints');
ePoints =  bwmorph(objThin, 'endpoints');

[~, w] = size(objThin);

half = floor(w/2);

modObjThin = objThin;
while threshSpur > 0
    threshSpur = getNumber4Spur(objThin, bPoints, ePoints, head, half);
    modObjThin = bwmorph(objThin, 'spur', threshSpur);
    itNum = itNum + 1;
    partialThin{itNum} = modObjThin;
    [modObjThin, threshSpur, partialThin] = thinCleaning(modObjThin, head, threshSpur, itNum, partialThin);
end

end


function [thinImg, partialRes3] = getThinnedImg(image, head)

objThin = bwmorph(image, 'thin', 'Inf');
objThin = bwmorph(objThin, 'thin', 'Inf');
ePoints =  bwmorph(objThin, 'endpoints');

threshSpur = 1;
itNum = 1;
if nnz(ePoints) >  2
    partialRes{itNum} = objThin;
    [thinImg, ~, partialRes3] = thinCleaning(objThin, head, threshSpur, itNum, partialRes);
else
    thinImg = objThin;
    partialRes3{1} = objThin;
end


end


function maxArea = getNumber4Spur(objThin, bPoints, ePoints, head, half)

objThinTemp = objThin;

if strcmp(head, 'l')
    objThinTemp(:, half:end) = 0;
    bPoints(:, half:end) = 0;
    ePoints(:, half:end) = 0;
else
    objThinTemp(:, 1:half-1) = 0;
    bPoints(:, 1:half-1) = 0;
    ePoints(:, 1:half-1) = 0;
end

se = strel('disk', 3);
bPoints = imdilate(bPoints, se);

objThinTemp(bPoints) = 0;

maxArea = 0;
[labeled, num] = bwlabel(objThinTemp);
for j = 1 : num
    thisObj = getObjects(j, labeled);
    tempObj = thisObj.cc;
    
    olapped = nnz(tempObj & ePoints);
    if olapped == 0
        objThinTemp(tempObj) = 0;
    else
        props = regionprops(tempObj, 'Area');
        if props.Area > maxArea && nnz(ePoints) > 1
            maxArea = props.Area;
        end
    end
end

end


function [origSkel, newSkelXY] = ...
    getPlusHeadAndTailPoint4Fitting(origSkel, fishProps, eyeProps, head)

eyeImg = fishProps.eyePosCent.eyeImg;
eyeNum = eyeProps.eyesNum;
filledImg = fishProps.filledFish;

contFilled = bwfill(filledImg + eyeImg, 'holes');

[~ , w] = size(contFilled);

halfSize = floor(w / 2);

if strcmp(head, 'r')
    tempContFish = contFilled(:, halfSize:end);
    newPoint = getNewEyeRefPoint(tempContFish, eyeNum, eyeProps);
    newx = floor(newPoint(1));
    newy = floor(newPoint(2));
    newSkelXY = [newx + 1, newy];
    newx = newx + halfSize;
else
    tempContFish = contFilled(:, 1:halfSize-1);
    newPoint = getNewEyeRefPoint(tempContFish, eyeNum, eyeProps);
    newx = floor(newPoint(1));
    newy = floor(newPoint(2));
    newSkelXY = [newx, newy];
end

origSkel(newy, newx) = 1;

end


function eyePerimPoint = getNewEyeRefPoint(tempContFish, eyeNum, eyeProps)

perimCont = bwperim(tempContFish);

if eyeNum == 1
    centroid = eyeProps.lstCent;
    ex = centroid(1);
    ey = centroid(2);
    perimPoint = find(perimCont(:, ex:ex) > 0);
    if strcmp(eyeProps.lstPos, 'top')
        perimPoint = perimPoint(end);
        skelY = getSkeletonNewPos(ey, perimPoint);
    else
        perimPoint = perimPoint(1);
        skelY = getSkeletonNewPos(ey, perimPoint);
    end
    skelX = ex;
elseif eyeNum == 2
    centroid1 = eyeProps.fstCent;
    centroid2 = eyeProps.lstCent;
    ex1 = centroid1(1);
    ey1 = centroid1(2);
    ex2 = centroid2(1);
    ey2 = centroid2(2);
    
    skelX = ceil((ex1 + ex2) / 2);
    skelY = getSkeletonNewPos(ey1, ey2);
else
    if strcmp(eyeProps.lstPos, 'top')
        centroid = eyeProps.lstCent;
        ex = centroid(1);
        ey = centroid(2);
        perimPoint = find(perimCont(:, ex:ex) > 0);
        perimPoint = perimPoint(end);
        skelY = getSkeletonNewPos(ey, perimPoint);
        skelX = ex;
    else
        centroid = eyeProps.fstCent;
        ex = centroid(1);
        ey = centroid(2);
        perimPoint = find(perimCont(:, ex:ex) > 0);
        perimPoint = perimPoint(1);
        skelY = getSkeletonNewPos(ey, perimPoint);
        skelX = ex;
    end
end

eyePerimPoint = [skelX, skelY];

end


function newSkelPos = getSkeletonNewPos(eyeCent, perimPoint)

newSkelPos = ceil((eyeCent + perimPoint) / 2);

end


function modFishSkel = postMod4BodyLength(image, eyeProps, fishSkeleton, head)

se = strel('disk', 2);
thinImg = imdilate(fishSkeleton, se);

remSkelFish = image;
remSkelFish(thinImg) = 0;

[labeledImg, num] = bwlabel(remSkelFish);

eyeCent = eyeProps.lstCent;
eyeCentImg = false(size(thinImg, 1), size(thinImg, 2));

if strcmp(head, 'r')
    eyeX = floor(eyeCent(1)) + floor(size(thinImg, 2) / 2);
else
    eyeX = floor(eyeCent(1));
end

eyeY = floor(eyeCent(2));
eyeCentImg(eyeY, eyeX) = 1;
eyeCentImg = imdilate(eyeCentImg, se);

ovlp = zeros(1, num);

for j = 1 : num
    tempObj = getObjects(j, labeledImg);
    ovlp(j) = nnz(tempObj.cc & eyeCentImg);
end

if num == 1
    modFishSkel = fishSkeleton;
else
    if ovlp(1) > ovlp(2)
        actFishRed = getObjects(2, labeledImg);
        actFishRed = actFishRed.cc;
    else
        actFishRed = getObjects(1, labeledImg);
        actFishRed = actFishRed.cc;
    end
    
    if strcmp(head, 'r')
        tail = 'l';
    else
        tail = 'r';
    end
    
    actFishRed = logical(actFishRed);
    [objThinHead, objThinPartHead] = getThinnedImg(actFishRed, head);
    [objThinTail, objThinPartTail] = getThinnedImg(actFishRed, tail);
    
    partialResults = {objThinPartHead, objThinPartTail};
    [h, w] = size(objThinHead);
    
    half = floor(w/2);
    
    fishThin = false(h, w);
    
    cont = bwperim(actFishRed);
    [cy, cx] = find(cont > 0);
    if strcmp(head, 'r')
        fishThin(:, half:end) = objThinHead(:, half:end);
        fishThin(:, 1:half-1) = objThinTail(:, 1:half-1); 
        tx = cx(1);
        ty = cy(1);
    else
        fishThin(:, 1:half-1) = objThinHead(:, 1:half-1);
        fishThin(:, half:end) = objThinTail(:, half:end);
        tx = cx(end);
        ty = cy(end);
    end    
    
    [~, ttx] = find(fishThin > 0);
    if abs(ttx(1) - ttx(end)) < half
        modFishSkel = fishSkeleton;
    else        
        sndSkel = fittingCurve4FishSkel(fishThin, head, partialResults, [tx, ty]);
        modFishSkel = complSkeleton(sndSkel);
        modFishSkel = logical(modFishSkel);
    end
end

end





