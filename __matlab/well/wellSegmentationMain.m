function processed = wellSegmentationMain(image)

global cw;
global ch;

if ch > cw
    minCirc = ch - 400;
    maxCirc = ch;
else
    minCirc = 100;%cw - 400;
    maxCirc = 200;%cw;
end

[centers, radii] = imfindcircles(image, [floor(minCirc/2) floor(maxCirc/2)], 'Sensitivity', .99, 'Method', 'twostage' ,...
    'ObjectPolarity', 'dark');

if ~isempty(centers)
    centerxy = centers(1:1, :);
    r = radii(1:1);
    
    if  r < ch / 2  * .8
        preProcImg = preProcessing(image);
        mask = getInnerROI(preProcImg);
    else
        mask = createCircMask(centerxy, cw, ch, r);
    end
else
    preProcImg = preProcessing(image);
    mask = getInnerROI(preProcImg);
end

if strcmp(checkEmptyImageOrNot(mask), 'true')
    processed.findWell = 'true';
    [x1, y1, x2, y2] = getBBoxCoordinates(mask);
    cropMaskImg = mask(y1 : y2, x1 : x2);
    grayMaskImg = uint8(mask) .* uint8(image);
    cropGMaskImg = grayMaskImg(y1 : y2, x1 : x2);
    processed.intROIMask = mask;
    processed.croppedMask = cropMaskImg;
    processed.croppedGray = cropGMaskImg;
    processed.grayImg = grayMaskImg;
    processed.boundingBox = [x1, y1, x2, y2];
else
    processed.findWell = 'false';
end

end






