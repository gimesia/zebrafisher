    
% ha nincs szem, akkor megnezni a szomszedsagot is
% TODO - beepiteni, hogy ha nincs feje a szerencsetlennek
% Csak arra van szuksegem, hogy van-e szemszerusege
function possFishProps = postFishExamination(image, num, maskOrig, varargin)

global cutHeadBB;

mask = image.mask;

cutHeadBB = image.bbox;

possFishProps = realFishOrNot(image, mask, maskOrig);

if isfield(possFishProps, 'newBbox')
    possFishProps.bbox = possFishProps.newBbox;
else
    possFishProps.bbox = image.bbox;
end

if num == 2 && strcmp(possFishProps.findFish, 'false')
    cutHeadBB = varargin{1}.bbox;
    possFishProps = realFishOrNot(varargin{1}, varargin{1}.mask, maskOrig);
    
    if isfield(possFishProps, 'newBbox')
        possFishProps.bbox = possFishProps.newBbox;
    else
        possFishProps.bbox = varargin{1}.bbox;
    end
end

end

% TODO valami dinamikusra
function revFishProps = realFishOrNot(image, mask, maskOrig)

global wellCroppedGray;

illCorrected = illumination_correction(image.input);

illCorrOrig = illumination_correction(wellCroppedGray);

rng.mx = 1;
rng.mn = 0;
image = normaliseIntensityRange(illCorrected, rng);
illCorrOrig = normaliseIntensityRange(illCorrOrig, rng);

fishEnc = imsharpen(image, 'Radius', 2, 'Amount', 1);

cmpBinFiltered = binarize4FishEye(fishEnc, 0.095);

if strcmp(checkEmptyImageOrNot(cmpBinFiltered), 'true')
    revFishProps = examineEyeProps(cmpBinFiltered, mask, illCorrected);
    if strcmp(revFishProps.findFish, 'false')
        reFilt = checkFishHasHeadOrNot(mask, illCorrOrig, maskOrig);
        if strcmp(reFilt.find, 'false')
            revFishProps.findFish = 'false';
        else
            mask = getCroppedImage(reFilt.possFish2nd);
            eyeImg = reFilt.possFish2ndEye;
            origMask = getCroppedImage(reFilt.newfish);
            
            x1 = mask.bbox(1);
            y1 = mask.bbox(2);
            x2 = mask.bbox(3);
            y2 = mask.bbox(4);
            eyeImgCrop = eyeImg(y1:y2, x1:x2);
            
            illCorrected = illCorrOrig(origMask.bbox(2):origMask.bbox(4), ...
                origMask.bbox(1):origMask.bbox(3));
            
            revFishProps = examineEyeProps(eyeImgCrop, mask.mask, illCorrected);
            revFishProps.newBbox = origMask.bbox;
        end
    end
else
    revFishProps.findFish = 'false';
end

end


function revFishProps = examineEyeProps(cmpBinFiltered, mask, illCorrected)

tempCmp = cmpBinFiltered;
cmpBinFiltered(mask > 0) = 1;
filledCompImg = imfill(cmpBinFiltered, 'holes');
se = strel('disk', 2);
filledCompImg = imerode(filledCompImg, se);
filledCompImg = bwareafilt(filledCompImg, 1);

[h, w] = size(filledCompImg);
halfSize = floor(w/2);

if h > w
    filledCompImg = imrotate(filledCompImg, -90);
    tempCmp = imrotate(tempCmp, -90);
    revFishProps.rotated = 'true';
    halfSize = floor(h/2);
else
    revFishProps.rotated = 'false';
end

range = floor(halfSize * .6);
[h, t] = headTailPosition(filledCompImg, range);

tempCmp(~filledCompImg) = 0;
tempFilled = filledCompImg;

if strcmp(h, 'r')
    tempCmp(:, 1:end-range-1) = 0;
    tempFilled(:, 1:end-range-1) = 0;
else
    tempCmp(:, range + 1:end) = 0;
    tempFilled(:, range + 1:end) = 0;
end

if strcmp(checkEmptyImageOrNot(tempCmp), 'true')
    someProps4Measures = getPossFishEye(tempCmp, tempFilled, h);
    
    if strcmp(checkEmptyImageOrNot(someProps4Measures.eyeImg), 'true')
        eyePosCentProps = getAnotherEyeAndRemoveFalseSegment(someProps4Measures, ...
            filledCompImg, illCorrected, h, revFishProps.rotated);
        
        revFishProps.findFish = 'true';
        revFishProps.filledFish = filledCompImg;
        revFishProps.possSegmentedEyeWithOthers = someProps4Measures.filtedBin;
        revFishProps.possSegmentedEye = eyePosCentProps.eyeImg;
        revFishProps.head = h;
        revFishProps.tail = t;
        revFishProps.croppedGray = illCorrected;
        revFishProps.eyePosCent = eyePosCentProps;
    else
        revFishProps.findFish = 'false';
    end
else
    revFishProps.findFish = 'false';
end

end


function sndChance = checkFishHasHeadOrNot(mask, illCorrOrig, maskOrig)

global cw;
global ch;
global cutHeadBB;

maskOrig = bwperim(maskOrig);

x1 = cutHeadBB(1);
x2 = cutHeadBB(3);
y1 = cutHeadBB(2);
y2 = cutHeadBB(4);

[~, w] = size(mask);
halfSize = floor(w/2);

if (w / cw) < .1
    sndChance.find = 'false';
else
    range = floor(halfSize * .6);
    [head, ~] = headTailPosition(mask, range);
    
    diffY = abs(mean([y1, y2]));
    perimPoint = find(maskOrig(diffY:diffY, :) > 0);
    
    if strcmp(head, 'r')
        if ~isempty(perimPoint) && numel(perimPoint) > 1
            perimPoint = perimPoint(end);
        else
            perimPoint = cw;
        end
        
        [plusX, plusY] = getPlusPixelsSize(abs(perimPoint - x2));
        
        if x2 + plusX > size(illCorrOrig, 2)
            plusX = abs(size(illCorrOrig, 2) - x2);
        end
        if (y1 - plusY < 0) | (y2 + plusY > size(illCorrOrig, 1))
            plusY = 0;
        end

        bigHeadGray = illCorrOrig(y1-plusY:y2+plusY, ...
            x1:x2+plusX);
        
        newx1 = x1;
        newx2 = x2 + plusX;
    else
        if ~isempty(perimPoint) && numel(perimPoint) > 1
            perimPoint = perimPoint(1);
        else
            perimPoint = 1;
        end
        
        [plusX, plusY] = getPlusPixelsSize(abs(perimPoint - x2));
        
        if x1 - plusX < 0
            plusX = 0;
        end
        if (y1 - plusY < 0) | (y2 + plusY > size(illCorrOrig, 1))
            plusY = 0;
        end
        
        bigHeadGray = illCorrOrig(y1-plusY:y2+plusY, ...
            x1-plusX:x2);
        
        newx1 = x1 - plusX;
        newx2 = x2;
    end
    
    newy1 = y1 - plusY;
    newy2 = y2 + plusY;
    
    %0.135 jo a szemre
    fishEnc = imsharpen(bigHeadGray, 'Radius', 2, 'Amount', 1);
    
    [count, intensity] = imhist(fishEnc);
    [~, maxpos] = max(count);
    thVal = intensity(maxpos);
    binFiltered = fishEnc < thVal * .8;
    possFish2nd = bwareafilt(binFiltered, 1);
    
    possFish2ndEye = binarize4FishEye(fishEnc, 0.095);
    
    newfish = false(ch, cw);
    newfish(newy1:newy2, newx1:newx2) = possFish2nd;
    
    sndChance.find = 'true';
    sndChance.possFish2nd = possFish2nd;
    sndChance.possFish2ndEye = possFish2ndEye;
    sndChance.newfish = newfish;
end

end


function [pixX, pixY] = getPlusPixelsSize(distance)

if distance > 200
    pixX = 40;
    pixY = 40;
else
    pixX = floor(distance * .75);
    pixY = floor(distance * .45);
end

end


function someProps4Measures = getPossFishEye(image, cropHead, head)

prop4AreaThresh = regionprops(image, 'Area');
threshArea = floor(mean([prop4AreaThresh.Area]));
areaThresh = bwareaopen(image, threshArea);

% figure; imshow(areaThresh);

% elnyal, ha tobbfele szakad
[~, num] = bwlabel(cropHead);
cropHPerim = bwperim(cropHead);
propsPerim = regionprops(cropHPerim, 'BoundingBox');

if num < 2
    if strcmp(head, 'r')
        pThreshX = propsPerim.BoundingBox(1) + propsPerim.BoundingBox(3);
    else
        pThreshX = propsPerim.BoundingBox(1);
    end
    
    resultEyeImg = false(size(areaThresh, 1), size(areaThresh, 2));
    
    [labeled, num] = bwlabel(areaThresh);
    for j = 1 : num
        thisObj = getObjects(j, labeled);
        tempObj = thisObj.cc;
        
        prop4EccThresh = regionprops(tempObj, 'Eccentricity', 'Centroid');
        
        if prop4EccThresh.Eccentricity < .85
            resultEyeImg(tempObj) = 1;
        else
            if abs(prop4EccThresh.Centroid(1) - pThreshX) < 70 && ...
                    prop4EccThresh.Eccentricity < .90
                resultEyeImg(tempObj) = 1;
            end
        end
        
    end
else
    resultEyeImg = false(size(areaThresh, 1), size(areaThresh, 2));
end

% figure; imshow(resultEyeImg);

someProps4Measures.filtedBin = areaThresh;
someProps4Measures.eyeImg = resultEyeImg;

end


function [head, tail] = headTailPosition(binData, range)

leftSide = binData(:, 1:range + 1);
rightSide = binData(:, end-range-1:end);

if nnz(leftSide) ~= 0 && nnz(rightSide) ~= 0
    leftMax = getOnes(leftSide, range);
    rightMax = getOnes(rightSide, range);
    
    if leftMax < rightMax
        head = 'r';
        tail = 'l';
    else
        head = 'l';
        tail = 'r';
    end
else
    if nnz(leftSide) == 0
        head = 'r';
        tail = 'l';
    elseif nnz(rightSide) == 0
        head = 'l';
        tail = 'r';
    end
end

end


function meandist = getOnes(list, range)

s = 1;
for i = 1 : range
    onespos = find(list(:, i) == 1);
    
    if isempty(onespos)
        onespos = find(list(:, end) == 1);
    end
    
    if ~isempty(onespos)
        fst = onespos(1);
        lst = onespos(end);
        dist(s) = abs(lst - fst);
        s = s + 1;
    end
end

meandist = mean(dist(:));


end







