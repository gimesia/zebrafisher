

function eyePosProps = getEyeDistAndPos(contObj, eyeObject, headPos)

[hc, ~] = size(contObj);

% TODO-szar
eyeObject = bwareafilt(eyeObject, 1);

eprops = regionprops(eyeObject, 'Centroid');
ex = eprops.Centroid(1);
ey = eprops.Centroid(2);

[allR, ~] = find(contObj(:, ex:ex) == 1);

% TODO-szar
if ~isempty(allR)
    
    if strcmp(headPos, 'bot')
        tThreshPos = allR(1);
        bThreshPos = hc;
    else
        bThreshPos = allR(2);
        tThreshPos = 1;
    end
    
    distT = abs(tThreshPos - ey);
    distB = abs(bThreshPos - ey);
    
    if distT < distB
        eyePosProps.pos = 'top';
        eyePosProps.perimPoint = allR(2);
    else
        eyePosProps.pos = 'bot';
        eyePosProps.perimPoint = allR(1);
    end
    
else
    half = floor(hc/2);
    if ey < half
        eyePosProps.pos = 'bot';
        eyePosProps.perimPoint = 1;
    else
        eyePosProps.pos = 'top';
        eyePosProps.perimPoint = half;
    end
end

end