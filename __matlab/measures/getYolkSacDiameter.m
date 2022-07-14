

function getYolkSacDiameter(fishProps, eyeProps, fullBodySkelProps, endPProps)

fishImg = fishProps.filledFish;
eyeImg = fishProps.eyePosCent.eyeImg;
head = fishProps.head;
eyeProperties = fishProps.eyePosCent;
eyeNum = eyeProps.eyesNum;

grayFish = fishProps.croppedGray;
if strcmp(fishProps.rotated, 'true')
    grayFish = imrotate(grayFish, -90);
end

fishPos = getFishPosition(eyeProperties, eyeNum);

getPossibleYolkSacRegion(grayFish, fishImg, eyeImg, eyeNum, head);

plusFishProps.fishPosition = fishPos;

end


function fishPosition = getFishPosition(eyeProperties, eyeNum)

pos = eyeProperties.fstPos;

if eyeNum == 2
    fishPosition = 'facedown';
elseif eyeNum == 1
    if strcmp(pos, 'top')
        fishPosition = 'rightside';
    else
        fishPosition = 'leftside';
    end
else
    if strcmp(pos, 'top')
        fishPosition = 'rightsideskew';
    else
        fishPosition = 'leftsideskew';
    end
end

end


function getPossibleYolkSacRegion(grayFish, binFish, eyeImg, eyeNum, head)

maskGrayImg = uint8(logical(binFish)) .* uint8(grayFish);

[~, w] = size(binFish);
half = floor(w / 2);

if strcmp(head, 'r')
    halfEye = eyeImg(:, half:end);
    halfMask = binFish(:, half:end);
    halfGray = maskGrayImg(:, half:end);
else
    halfEye = eyeImg(:, 1:half);
    halfMask = binFish(:, 1:half);
    halfGray = maskGrayImg(:, 1:end);
end

[~, ex] = find(halfEye > 0);

if strcmp(head, 'r')
    cPos = ex(1);
    cropMask = halfMask(:, 1:cPos);
    cropGray = halfGray(:, 1:cPos);
else
    cPos = ex(end);
    cropMask = halfMask(:, cPos:end);
    cropGray = halfGray(:, cPos:end);
end

profile = zeros(1, size(cropMask, 2));
for i = 1 : size(cropMask, 2)
    profile(i) = sum(cropMask(:, i:i));
end
profile = sgolayfilt(profile, 3, 35);
[pks, locs] = findpeaks(profile);

[~, wc] = size(cropMask);
halfPos = floor(wc / 2);

if ~isempty(pks)
    locsNum = size(locs, 2);
    if strcmp(head, 'r')
        if locsNum == 1
            possYolkPoint = locs(1);
        else
            poses = find(pks > 0) ;
            pos1X = locs(poses(end));
            pos2X = locs(poses(end-1));
            
            eyeDist1 = abs(wc - pos1X);
            
            sideDist1 = abs(halfPos - pos1X);
            sideDist2 = abs(halfPos - pos2X);
            
            if sideDist1 < sideDist2
                possYolkPoint = pos1X;
            else
                if eyeDist1 / wc  > .25
                    possYolkPoint = pos1X;
                else
                    possYolkPoint = pos2X;
                end
            end
        end
    else
        if locsNum == 1
            possYolkPoint = locs(1);
        else
            poses = find(pks > 0, 2) ;
            pos1X = locs(poses(1));
            pos2X = locs(poses(2));
            
            eyeDist1 = abs(1 - pos1X);
            
            sideDist1 = abs(wc - pos1X);
            sideDist2 = abs(wc - pos2X);
            
            if sideDist1 < sideDist2
                possYolkPoint = pos1X;
            else
                if eyeDist1 / wc  > .25
                    possYolkPoint = pos1X;
                else
                    possYolkPoint = pos2X;
                end
            end
        end
    end

    yolkSacFound = 'true';
else
    if eyeNum == 2
        if strcmp(head, 'r')
            possYolkPoint = floor(wc - wc * .25);
        else
            possYolkPoint = floor(wc * .25);
        end
        yolkSacFound = 'true';
    else
        yolkSacFound = 'false';
    end
end

yolkRange = floor(wc / 4);
if strcmp(yolkSacFound, 'true')
    getYolkSacSegmentAndDiameter(cropGray, cropMask, head, possYolkPoint, yolkRange, eyeNum);
end

% figure; imshow(cropMask);

end


function getYolkSacSegmentAndDiameter(grayFish, cropMask, head, yPos, range, eyeNum)

if eyeNum == 2
    props = regionprops(cropMask, 'EquivDiameter', 'MinorAxisLength', 'Orientation');
    diam = props.EquivDiameter;
else
    if strcmp(head, 'r')
        if yPos - floor(range*1.5) > 0
            grayFish = grayFish(:, yPos - floor(range*1.5):yPos+range);
        else
            grayFish = grayFish(:, yPos - range:yPos+range);
        end
    else
        if floor(yPos+range*1.5) < size(cropMask, 2)
            grayFish = grayFish(:, yPos - range:floor(yPos+range*1.5));
        else
            grayFish = grayFish(:, yPos - range:yPos+range);
        end
    end
    
    gmag = imgradient(grayFish);
    se = strel('disk', 35);
    grayFish2 = imopen(gmag, se);
%         figure; imshow(grayFish, []);
%     hold on; visboundaries(grayFish2);
end

end




