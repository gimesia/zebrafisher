
function saveMeasures(measures, filename)

fileID = fopen(filename, 'w');

fprintf(fileID, '{');
for m = 1 : size(measures, 1)
    meas = measures{m};

    if size(meas{2}, 2) > 1
        measVal = splitAndMerge2STR(meas{2});
    else
        measVal = meas{2};
    end
    
    if isa(measVal, 'double') 
        fprintf(fileID, '"%s": %.2f', meas{1}, measVal);
    else
        fprintf(fileID, '"%s": %s', meas{1}, measVal);
    end
    
    if m ~= size(measures, 1)  
        fprintf(fileID, ', ');
    end
end
fprintf(fileID, '}');

fclose(fileID);

end


function roiSTR = splitAndMerge2STR(roi)

if size(roi, 2) == 2
    roiSTR = sprintf('[%.0f, %.0f]', roi(1), roi(2));
else
    roiSTR = sprintf('[%.0f, %.0f, %.0f, %.0f]', roi(1), roi(2), roi(3), roi(4));
end
    
end
