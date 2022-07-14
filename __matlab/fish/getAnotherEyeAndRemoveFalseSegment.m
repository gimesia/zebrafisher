
% lekezelni, hogy ne vagja szet a szemet.. - Hough trafo miatt..

% most eleg, ha az egyertelmuek megvannak
function eyePosCentProps = getAnotherEyeAndRemoveFalseSegment(measProps, ...
    fish, illCorrected, head, rotated)

preSegEye = measProps.eyeImg;

[~, num] = bwlabel(preSegEye);

% figure; imshow(preSegEye);

if strcmp(rotated, 'true')
    illCorrected = imrotate(illCorrected, -90);
end

if num > 2
    preSegEye = bwareafilt(preSegEye, 2);
    eyePosCentProps = examineAnotherEye(preSegEye, illCorrected, head, fish);
    % TODO okosabbra!!
    %     [~, num] = bwlabel(preSegEye);
elseif num == 1
    eyePosCentProps = examineAnotherEye(preSegEye, illCorrected, head, fish);
elseif num == 2
    [labeled, num] = bwlabel(preSegEye);
    centroids = zeros(2, 2);
    for i = 1 : num
        obj = getObjects(i, labeled);
        propE = regionprops(obj.cc, 'Centroid');
        centroids(i, :) = propE.Centroid;
    end
    eye1Cent = centroids(1, :);
    eye2Cent = centroids(2, :);
    
    eyePosCentProps.fstPos = 'top';
    eyePosCentProps.lstPos = 'bot';
    if eye1Cent(2) < eye2Cent(2)
        eyePosCentProps.eyeImg = preSegEye;
        eyePosCentProps.fstCent = eye1Cent;
        eyePosCentProps.lstCent = eye2Cent;
    else
        eyePosCentProps.eyeImg = preSegEye;
        eyePosCentProps.fstCent = eye2Cent;
        eyePosCentProps.lstCent = eye1Cent;
    end
    eyePosCentProps.eyesNum = 2;
end

% eyePosCentProps
% figure; imshow(eyePosCentProps.eyeImg);
% TODO! ha van plusz kiszegmentalt resz!!

end


function eyePosCentProps = examineAnotherEye(preSegEye, illCorrected, head, fish)

[h, w] = size(preSegEye);
half = floor(w/2);
resultSegmentedEyes = false(h, w);
% ill = illCorrected;

illCorrected = imsharpen(illCorrected, 'Radius', 3, 'Amount', 7);

se = strel('disk', 11);
illCorrected = imclose(illCorrected, se);

if strcmp(head, 'r')
    halfPre = preSegEye(:, half+1:end);
    halfIll = illCorrected(:, half+1:end);
    %     halfIllO = ill(:, half+1:end);
    halfFish = fish(:, half+1:end);
else
    halfPre = preSegEye(:, 1:half);
    halfIll = illCorrected(:, 1:half);
    %     halfIllO = ill(:, 1:half);
    halfFish = fish(:, 1:half);
end

[x1, ~, x2, ~] = getBBoxCoordinates(halfPre);
partFilled = fish(:, x1:x2);
[ph, ~] = size(partFilled);

partCont = bwperim(partFilled);
cropTempObj = halfPre(:, x1:x2);

topOnes = nnz(partFilled(1:floor(ph/2), :));
botOnes = nnz(partFilled(floor(ph/2):end, :));

if botOnes > topOnes
    eyePos = getEyeDistAndPos(partCont, cropTempObj, 'bot');
else
    eyePos = getEyeDistAndPos(partCont, cropTempObj, 'top');
end

rng.mx = 1;
rng.mn = 0;
halfIll = normaliseIntensityRange(halfIll, rng);

% TODO - szar
halfPre = bwareafilt(halfPre,1);
propEye = regionprops(halfPre, halfIll, 'MeanIntensity', 'Centroid');

distMap = bwdist(halfPre);
intDiff = halfIll - propEye.MeanIntensity;

% TODO dinamikusra!!
dThresh = mat2gray(distMap) < .2;
dInt = intDiff < 0.085;

preSegPossEye = dThresh & dInt;
preSegPossEye(~halfFish) = 0;

eyePos.centroid = [propEye.Centroid(1) propEye.Centroid(2)];

onlyNewPossEye = preSegPossEye;
onlyNewPossEye(halfPre) = 0;

preDiffDThresh = dThresh;
preDiffDThresh(halfPre) = 0;

if (nnz(onlyNewPossEye & preDiffDThresh) / nnz(preDiffDThresh)) > 0.5
    % eredmenykep a szemrol
    segmentedEyes = preSegPossEye;
else
    segmentedEyes = getRealNewFishEye(halfPre, preSegPossEye, eyePos, halfFish);
end

se = strel('disk', 1);
segmentedEyes = imerode(segmentedEyes, se);

eyePosCentProps = getSomePropsFromEyes4Measures(segmentedEyes, eyePos);
if strcmp(head, 'r')
    resultSegmentedEyes(:, half+1:end) = segmentedEyes;
else
    resultSegmentedEyes(:, 1:half) = segmentedEyes;
end
eyePosCentProps.eyeImg = resultSegmentedEyes;

% figure;
% subplot(1, 2, 2); imshow(halfIllO);
% hold on;
% visboundaries(segmentedEyes);
% hold off;
% subplot(1, 2, 1); imshow(halfIllO);
% figure; imshow(segmentedEyes);

end


function resultNewEyeImg = getRealNewFishEye(origEyeImg, newSegmentEyeImg, eyepos, halfFish)

[labeled, num] = bwlabel(newSegmentEyeImg);

if num == 1
    resultNewEyeImg = seperateEyesIfPossible(origEyeImg, newSegmentEyeImg, eyepos);
elseif num > 2
    % TODO - ez buta
    resultNewEyeImg = bwareafilt(newSegmentEyeImg, 2);
else
    resultNewEyeImg = ...
        reallyNewEyeSegment(labeled, eyepos, origEyeImg, num, halfFish);
end

end


function postEyeImg = reallyNewEyeSegment(labeled, preProps, ...
    origEyeImg, labelNum, halfFish)

segmentedPost = labeled > 0;

preCent = preProps.centroid;
preX = preCent(1);
preY = preCent(2);

actDist = double(ones(1, 2));
actCentroid = double(ones(1, 2));
actBBox = double(ones(1, 4));

for j = 1 : labelNum
    thisObj = getObjects(j, labeled);
    tempObj = thisObj.cc;
    
    postProps = regionprops(tempObj, 'Centroid');
    postCent = postProps.Centroid;
    postX = postCent(1);
    postY = postCent(2);
    
    X = [preX, preY];
    Y = [postX, postY];
    
    actDist(j) = pdist2(X, Y, 'euclidean');
    actCentroid(j, :) = Y;
    [x1, y1, x2, y2] = getBBoxCoordinates(tempObj);
    actBBox(j, :) = [x1, y1, x2, y2];
    
end

if actDist(1) > actDist(2)
    newEyeLabel = 1;
    oldEyeLabel = 2;
else
    newEyeLabel = 2;
    oldEyeLabel = 1;
end

perFish = bwperim(halfFish);
post = actBBox(newEyeLabel, :);

diffX = abs(mean([post(1), post(3)]));
diffY = abs(mean([post(2), post(4)]));
perimPointY = find(perFish(:, diffX:diffX) > 0);
perimPointX = find(perFish(diffY:diffY, :) > 0);

if strcmp(preProps.pos, 'bot')
    if ~isempty(perimPointY)
        perimPointY = perimPointY(end);
    else
        perimPointY = 1;
    end
    distPerimNewEyeY = abs(perimPointY - post(2));
else
    if ~isempty(perimPointY & perimPointX)
        perimPointY = perimPointY(1);
    else
        perimPointY = size(halfFish, 1);
    end
    distPerimNewEyeY = abs(perimPointY - post(4));
end

if preProps.perimPoint < (size(perFish, 2) / 2)
    if ~isempty(perimPointX)
        perimPointX = perimPointX(1);
    else
        perimPointX = 1;
    end
    distPerimNewEyeX = abs(perimPointX - post(1));
else
    if ~isempty(perimPointX)
        perimPointX = perimPointX(end);
    else
        perimPointX = size(halFish, 2);
    end
    distPerimNewEyeX = abs(perimPointX - post(3));
end

if distPerimNewEyeX < 70 || distPerimNewEyeY < 70
    postEyeImg = origEyeImg | segmentedPost;
else
    oldEye = getObjects(oldEyeLabel, labeled);
    postEyeImg = oldEye.cc;
end

end


function postEyeImg = seperateEyesIfPossible(origEye, postEye, eyeprops)

contEye = bwperim(postEye);

prop4Hough = regionprops(postEye, 'EquivDiameter');

diam = prop4Hough.EquivDiameter;
minRad = floor((diam / 2) * 0.75);
maxRad = floor(diam * 1.5);

[centers, radii, ~] = imfindcircles(contEye, [minRad, maxRad], ...
    'ObjectPolarity', 'bright', 'Sensitivity', 0.9, 'EdgeThreshold', 0.1);

fatterPostEye = origEye | postEye;

if ~isempty(centers)
    detectCircNum = size(centers, 1);
    
    if detectCircNum == 1
        postEyesProps = getEyeOrEyes(fatterPostEye, centers, radii);
        postEyeImg = postEyesProps.result2Eyes;
    elseif detectCircNum == 2
        postEyesProps = ...
            diffBetweenCircleAndSegmentedEye(fatterPostEye, centers, radii, eyeprops.pos);
        postEyeImg = postEyesProps.result2Eyes;
    else
        centers = centers(1:2, :);
        radii = radii(1:2);
        postEyesProps = ...
            diffBetweenCircleAndSegmentedEye(fatterPostEye, centers, radii, eyeprops.pos);
        postEyeImg = postEyesProps.result2Eyes;
    end
    
else
    postEyeImg = fatterPostEye;
end

end


function possEyes = diffBetweenCircleAndSegmentedEye(fatterPostEye, centers, radii, tbpos)

[hf, wf] = size(fatterPostEye);

separatedEyes = false(hf, wf);

if strcmp(tbpos, 'bot')
    circ1xy = centers(1, :);
    circ2xy = centers(2, :);
    
    if circ1xy(2) > circ2xy(2)
        circMaskInv = createCircMask(circ2xy, wf, hf, radii(2));
    else
        circMaskInv = createCircMask(circ1xy, wf, hf, radii(1));
    end
else
    circ1xy = centers(1, :);
    circ2xy = centers(2, :);
    
    if circ1xy(2) > circ2xy(2)
        circMaskInv = createCircMask(circ1xy, wf, hf, radii(1));
    else
        circMaskInv = createCircMask(circ2xy, wf, hf, radii(2));
    end
end

possAnotherEyeInv = logical(fatterPostEye) - logical(circMaskInv);
se = strel('disk', 3);
possAnotherEyeInv = imopen(possAnotherEyeInv, se);
possAnotherEyeInv = bwareafilt(logical(possAnotherEyeInv), 1);

possAnotherEye = logical(fatterPostEye) - logical(possAnotherEyeInv);
possAnotherEye = bwareafilt(logical(possAnotherEye), 1);
possAnotherEyeSep = logical(possAnotherEye) - bwperim(logical(possAnotherEye));

possAnotherEyeSep = logical(possAnotherEyeSep);
possAnotherEyeInv = logical(possAnotherEyeInv);
possAnotherEye = logical(possAnotherEye);

separatedEyes(possAnotherEyeSep) = 1;
separatedEyes(possAnotherEyeInv) = 1;
separatedEyes = logical(separatedEyes);

possEyes.origOneEye = possAnotherEye;
possEyes.reFiltAnotherEye = possAnotherEyeInv;
possEyes.result2Eyes = separatedEyes;

end


function possEyes = getEyeOrEyes(fatterPostEye, centers, radii)

[hf, wf] = size(fatterPostEye);

circleMask = createCircMask(centers, wf, hf, radii(1));

possAnotherEyeSegment = logical(fatterPostEye) - logical(circleMask);

possAnotherEyeSegment(possAnotherEyeSegment < 0) = 0;
fatterPostEye = logical(fatterPostEye);

oneEyeSep = false(hf, wf);
anotherEye = false(hf, wf);
separatedEyes = false(hf, wf);

if (nnz(possAnotherEyeSegment) / nnz(fatterPostEye)) > .1
    oneEye = fatterPostEye;
    oneEye(~circleMask) = 0;
    anotherEye = possAnotherEyeSegment;
    oneEyeSep = logical(oneEye) - bwperim(logical(oneEye));
    anotherEye = logical(anotherEye);
    oneEyeSep = logical(oneEyeSep);
    separatedEyes(oneEyeSep) = 1;
    separatedEyes(anotherEye) = 1;
    separatedEyes = logical(separatedEyes);
else
    separatedEyes = fatterPostEye;
    separatedEyes = logical(separatedEyes);
    separatedEyes(logical(possAnotherEyeSegment)) = 0;
end

possEyes.origOneEye = oneEyeSep;
possEyes.reFiltAnotherEye = anotherEye;
possEyes.result2Eyes = separatedEyes;

end


function eyePosCentProps = ...
    getSomePropsFromEyes4Measures(segmentedEyes, eyePos)

[labeled, num] = bwlabel(segmentedEyes);

bBoxes = uint8(zeros(2, 4));
centroids = double(zeros(2, 2));

if num == 1
    fstPos = eyePos.pos;
    fstProp = regionprops(segmentedEyes, 'Centroid');
    fstCent = fstProp.Centroid;
    lstPos = fstPos;
    lstCent = fstCent;
    eyesNum = 1;
else
    
    for i  = 1 : num
        obj = getObjects(i, labeled);
        props = regionprops(obj.cc, 'Centroid');
        [x1, y1, x2, y2] = getBBoxCoordinates(obj.cc);
        
        centroids(i, :) = props.Centroid;
        bBoxes(i, :) = [x1, y1, x2, y2];
    end
    
    eye1Cent = centroids(1, :);
    eye2Cent = centroids(2, :);
    diffDist = pdist2(eye1Cent, eye2Cent, 'euclidean');
    
    if diffDist < 30
        fstPos = eyePos.pos;
        lstPos = eyePos.pos;
        
        if eye1Cent(2) < eye2Cent(2)
            fstCent = eye1Cent;
            lstCent = eye2Cent;
        else
            fstCent = eye2Cent;
            lstCent = eye1Cent;
        end
        eyesNum = 3;
    else
        fstPos = 'top';
        lstPos = 'bot';
        if eye1Cent(2) < eye2Cent(2)
            fstCent = eye1Cent;
            lstCent = eye2Cent;
        else
            fstCent = eye2Cent;
            lstCent = eye1Cent;
        end
        eyesNum = 2;
    end
end

% eyesNum = 2;
eyePosCentProps.eyesNum = eyesNum;
eyePosCentProps.fstPos = fstPos;
eyePosCentProps.lstPos = lstPos;
eyePosCentProps.fstCent = fstCent;
eyePosCentProps.lstCent = lstCent;

end






