
% max ketto szeme lehet
function fishEyeProps = getFishEyes(eyeImg, fishProps, eyeProps)

global cw;
global ch;

x1 = fishProps.bbox(1);
y1 = fishProps.bbox(2);
x2 = fishProps.bbox(3);
y2 = fishProps.bbox(4);

segmentedFishEyeOrigSize = zeros(ch, cw);

if strcmp(fishProps.rotated, 'true')
    eyeImg = imrotate(eyeImg, 90);  
end

eyeDiam = getEyeDiameter(eyeImg, eyeProps);

segmentedFishEyeOrigSize(y1:y2, x1:x2) = eyeImg;

fishEyeProps.segmEyeOrig = segmentedFishEyeOrigSize;
fishEyeProps.eyeDiam = eyeDiam;
% figure; imshow(segmentedFishEyeOrigSize);

end


function eyeDiam = getEyeDiameter(eyeImg, eyeProps)

eyeNum = eyeProps.eyesNum;
se = strel('disk', 5);

if eyeNum == 1
    eyeImg = imclose(eyeImg, se);
    props = regionprops(eyeImg, 'EquivDiameter');
    eyeDiam = props.EquivDiameter;
else
    eyeImg = bwareafilt(eyeImg, 1);
    eyeImg = imclose(eyeImg, se);
    props = regionprops(eyeImg, 'EquivDiameter');
    eyeDiam = props.EquivDiameter;
end

end

% TODO - valamire nagyon jo lesz
%seTail = strel('disk', 17);
%illCorrected = imbothat(illCorrected, seTail);