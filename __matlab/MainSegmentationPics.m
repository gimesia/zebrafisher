function MainSegmentationPics(filePath, oscpPath, sfileName)

warning off;

addpath(genpath(oscpPath));

global cw;
global ch;
global inputImg;

inputImg = imread(filePath);

if size(inputImg, 3) ~= 1
    inputImg = rgb2gray(inputImg);
end

[ch, cw] = size(inputImg);
rng.mx = 255;
rng.mn = 0;
inputImg = normaliseIntensityRange(inputImg, rng);
inputImg = uint8(inputImg);

wellProps = wellSegmentationMain(inputImg);

if strcmp(wellProps.findWell, 'true')
    
    measures{1, :} = {'well_roi', wellProps.boundingBox};
    
    fishProps = fishSegmentationMain(inputImg, wellProps);
    measures{2, :} = {'fish_roi', fishProps.bbox};
    
    if strcmp(fishProps.fish, 'true')
        
        measProps = measuresMain(fishProps);
        
        meas = measProps.measures;
        measures{3 ,:} = {'tail_length', meas.endPointsDist};
        measures{4, :} = {'eye_diameter', meas.eyeDiam};
        ePoints = measProps.endXY;
        measures{5, :} = {'head_endpoint', ePoints(1, :)};
        measures{6, :} = {'tail_endpoint', ePoints(2, :)};   

    else
        measures{1, :} = {'well_roi', wellProps.boundingBox};
        measures{2, :} = {'fish_roi', fishProps.bbox};
        measures{3 ,:} = {'tail_length', 0};
        measures{4, :} = {'eye_diameter', 0};
        measures{5, :} = {'head_endpoint', []};
        measures{6, :} = {'tail_endpoint', []};
    end
else
    measures{1, :} = {'well_roi', []};
    measures{2, :} = {'fish_roi', []};
    measures{3 ,:} = {'tail_length', 0};
    measures{4, :} = {'eye_diameter', 0};
    measures{5, :} = {'head_endpoint', []};
    measures{6, :} = {'tail_endpoint', []};
end

saveMeasures(measures, sfileName);

end

