
function possFishProps = fishSegmentationMain(image, wellProperties)

global originalCropped;
global inputImg;

segmentedFishOrigSize = false(size(inputImg, 1), size(inputImg, 2));
bBox = wellProperties.boundingBox;
maskCropped = wellProperties.croppedMask;
maskOriginal = wellProperties.intROIMask;

rng.mx = 1;
rng.mn = 0;
image = normaliseIntensityRange(image, rng);

illCorrected = homomorphic(image, 2, 0.015, 2, 1);

filteredImg = rangefilt(illCorrected);

croppedFilteredImg = filteredImg(bBox(2) : bBox(4), bBox(1) : bBox(3));

croppedFilteredImg = wiener2(croppedFilteredImg, [30 30]);
originalCropped = image(bBox(2) : bBox(4), bBox(1) : bBox(3));

% erzekeny a kernel meretere
T = adaptthresh(croppedFilteredImg, 0.95, 'ForegroundPolarity', 'dark', ...
    'Statistic', 'gaussian', 'NeighborhoodSize', 2*floor(size(croppedFilteredImg)/14)+1);
binFiltered = imbinarize(croppedFilteredImg, T);

binFiltered(maskCropped == 0) = 0;

possFishProps = getPossibleFish(binFiltered, maskCropped, ...
    wellProperties.boundingBox, wellProperties.grayImg, maskOriginal);

if strcmp(possFishProps.fish, 'true')
    x1 = possFishProps.bbox(1);
    y1 = possFishProps.bbox(2);
    x2 = possFishProps.bbox(3);
    y2 = possFishProps.bbox(4);
    temp = possFishProps.filledFish;
    if strcmp(possFishProps.rotated, 'true')
        temp = imrotate(temp, 90);
    end
    segmentedFishOrigSize(y1:y2, x1:x2) = temp;
end

se = strel('disk', 2);
segmentedFishOrigSize = imopen(segmentedFishOrigSize, se);
segmentedFishOrigSize = bwareafilt(segmentedFishOrigSize, 1);

possFishProps.segmentedOrigSizeFish = segmentedFishOrigSize;

end