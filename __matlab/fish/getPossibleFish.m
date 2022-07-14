% TODO - HIBAKEZELES!!!!!!! + leesett feju halak kezelese
function possFishProps = getPossibleFish(binaryImg, cropMask, bBox, cropGray, maskOriginal)

global cont;
global modCont;
global ch;
global cw;
global wellCroppedGray;

wellCroppedGray = cropGray;

segmentedFishOrigSizeFst = false(ch, cw);
segmentedFishOrigSizeSnd = false(ch, cw);

cont = bwperim(cropMask);

binaryImg = bwareaopen(binaryImg, 100);

threshMask = getPlateWidthAndRemoveSides(binaryImg, cropMask, 'false');
modCont = threshMask;

binaryImg(threshMask > 0) = 0;

% figure; imshow(binaryImg);

se = strel('disk', 5);
binaryImg = imclose(binaryImg, se); 

binFiltered = bwareafilt(binaryImg, 2);

possFishNum = 1;

if strcmp(checkEmptyImageOrNot(binFiltered), 'true')
    
    fish = whichIsThePossFish(binFiltered, cropMask);
    
    if strcmp(checkEmptyImageOrNot(fish.fishMask), 'true')
        segmentedFishOrigSizeFst(bBox(2):bBox(4), bBox(1):bBox(3)) = fish.fishMask;
        fstFishImg = getCroppedImage(segmentedFishOrigSizeFst);
        
        if strcmp(checkEmptyImageOrNot(fish.tempFish), 'true')
            segmentedFishOrigSizeSnd(bBox(2):bBox(4), bBox(1):bBox(3)) = fish.tempFish;
            sndFishImg = getCroppedImage(segmentedFishOrigSizeSnd);
            possFishNum = possFishNum + 1;
            examFishProps = postFishExamination(fstFishImg, possFishNum, maskOriginal, sndFishImg);
        else
            examFishProps = postFishExamination(fstFishImg, possFishNum, maskOriginal);
        end
        
        if strcmp(examFishProps.findFish, 'true')
            possFishProps = examFishProps;
            possFishProps.fish = 'true';
        else
            possFishProps.fish = 'false';
        end
        
    else
        possFishProps.fish = 'false';
    end
else
    % TODO - ha nem talalunk halat.
    possFishProps.fish = 'false';
end

end


function possWellSizeThresh = getPlateWidthAndRemoveSides(binImage, wellMask, corrected)

possWellSizeThresh = zeros(size(binImage, 1), size(binImage, 2));

remBinImg = binImage;

if strcmp(corrected, 'false')
    se = strel('disk', 21);
    erodedWell = imerode(wellMask, se);
    
    remBinImg(erodedWell > 0) = 0;
    remBinImg = bwareaopen(remBinImg, 100);
end

[mh, mw] = size(binImage);

lt = remBinImg(1:floor(mh/2), 1:floor(mw/2));
lb = remBinImg(floor(mh/2:mh), 1:floor(mw/2));
rt = remBinImg(1:floor(mh/2), floor(mw/2):mw);
rb = remBinImg(floor(mh/2):mh, floor(mw/2):mw);

ltThresh = getMeanColSum4Strel(lt, 'lt', corrected);
lbThresh = getMeanColSum4Strel(lb, 'lb', corrected);
rtThresh = getMeanColSum4Strel(rt, 'rt', corrected);
rbThresh = getMeanColSum4Strel(rb, 'rb', corrected);

possWellSizeThresh(1:floor(mh/2), 1:floor(mw/2)) = ltThresh;
possWellSizeThresh(floor(mh/2:mh), 1:floor(mw/2)) = lbThresh;
possWellSizeThresh(1:floor(mh/2), floor(mw/2):mw) = rtThresh;
possWellSizeThresh(floor(mh/2):mh, floor(mw/2):mw) = rbThresh;

end


function threshWell = getMeanColSum4Strel(data, whichCorner, correctedStep)

global cont;
global modCont;

threshWell = zeros(size(data, 1), size(data, 2));

colSum = sum(data');
meanData = floor(mean(colSum(colSum > 0)));

if strcmp(correctedStep, 'false')
    image = cont;
else
    image = modCont;
end


if ~isnan(meanData)
    se = strel('disk', meanData);
    if strcmp(whichCorner, 'lt')
        threshWell = imdilate(image(1:floor(size(image, 1)/2), 1:floor(size(image, 2)/2)), se);
    elseif strcmp(whichCorner, 'lb')
        threshWell = imdilate(image(floor(size(image, 1)/2:size(image, 1)), 1:floor(size(image, 2)/2)), se);
    elseif strcmp(whichCorner, 'rt')
        threshWell = imdilate(image(1:floor(size(image, 1)/2), floor(size(image, 2)/2):size(image, 2)), se);
    elseif strcmp(whichCorner, 'rb')
        threshWell = imdilate(image(floor(size(image, 1)/2):size(image, 1), floor(size(image, 2)/2):size(image, 2)), se);
    end
end

end


function [fish, someProps] = fishOrNot(data)

props = regionprops(data, 'Eccentricity', 'Area', 'BoundingBox');

if props.Eccentricity < .9 %.92
    fish = 'false';
else
    fish = 'true';
end

someProps.area = props.Area;
someProps.objWidth = props.BoundingBox(3);
someProps.objHeight = props.BoundingBox(4);

end


function whichFish = whichIsThePossFish(binImage, maskCropped)

global cw;
global ch;

biggerBinImg = binImage;
[labeled, num] = bwlabel(binImage);
for j = 1 : num
    thisObj = getObjects(j, labeled);
    tempObj = thisObj.cc;
    
    [tempFish, ~] = fishOrNot(tempObj);
    
    if strcmp(tempFish, 'true')
        objFishProps = checkFishyPropsFst(tempObj, maskCropped);
        objFish = objFishProps.notFish;
        if objFish == 1
            tempFish = 'true';
            biggerBinImg(objFishProps.corrFishMask) = 1;
        else
            tempFish = 'false';
        end
        
        if strcmp(tempFish, 'false')
            tempFishBool(j) = 0;            
        else
            tempFishBool(j) = 1;
        end
    else
        tempFishBool(j) = 0;
    end
end

labeledMod = bwlabel(biggerBinImg);
if sum(tempFishBool) == 2
    whichFish.fishIs = 'true';
    labNum = moreFisherObject(getObjects(1, labeledMod), getObjects(2, labeledMod));
    if labNum == 1
        fMask = getObjects(1, labeledMod);
        whichFish.fishMask = fMask.cc;
        tMask = getObjects(2, labeledMod);
        whichFish.tempFish = tMask.cc;
    else
        fMask = getObjects(2, labeledMod);
        whichFish.fishMask = fMask.cc;
        tMask =  getObjects(1, labeledMod);
        whichFish.tempFish = tMask.cc;
    end
elseif sum(tempFishBool) == 1
    whichFish.fishIs  = 'true';
    fishLabel = find(tempFishBool == 1);
    
    obj = getObjects(fishLabel, labeledMod);
    object = obj.cc;
    whichFish.fishMask = object;
    whichFish.tempFish = zeros(ch, cw);
else
    whichFish.fishIs = 'false';
    whichFish.fishMask = zeros(ch, cw);
    whichFish.tempFish = zeros(ch, cw);
end

end


function preFishProps = checkFishyPropsFst(possibleFish, mask)

global cw;

% TODO dinamikusra a meretet!
complImage = imcomplement(possibleFish);
se = strel('disk', 51);
filledImg = imcomplement(imopen(complImage, se));

complMask = imcomplement(mask);
complBiggerCirc = modifyCirc(complMask, 5, 'd');

complBiggerCirc(1:5, :) = 1;
complBiggerCirc(end-5:end, :) = 1;
complBiggerCirc(:, 1:5) = 1;
complBiggerCirc(:, end-5:end) = 1;

objProps = regionprops(filledImg, 'Area', 'Solidity', 'MajorAxisLength');

if nnz(complBiggerCirc & filledImg) < 500 || objProps.MajorAxisLength > cw/5

    wellProps = regionprops(mask, 'Area');

    objArea = objProps.Area;
    wellArea = wellProps.Area;
    
    ratio = objArea / wellArea * 100;
    
    if ratio < 1.1 %0.85 %1.1
        notFish = 0;
    else
        notFish = 1;
    end
else
    notFish = 0;
end

preFishProps.notFish = notFish;
preFishProps.corrFishMask = filledImg;

end


function modBinary = modifyCirc(image, kernelSize, erodeOrDilate)

se = strel('disk', kernelSize);

if strcmp(erodeOrDilate, 'e')
    modBinary = imerode(image, se);
elseif strcmp(erodeOrDilate, 'd')
    modBinary = imdilate(image, se);
end

end


function fisherObj =  moreFisherObject(possFishImageFst, possFishImageSnd)

global originalCropped;

meanIntFstImg = possFishImageFst.cc .* originalCropped;
meanIntSndImg = possFishImageSnd.cc .* originalCropped;

if std(nonzeros(meanIntFstImg)) > std(nonzeros(meanIntSndImg))
    fisherObj = 1;
else
    fisherObj = 2;
end

end



