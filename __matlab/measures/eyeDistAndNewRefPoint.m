

function [point1, point2] = eyeDistAndNewRefPoint(eyeDist, oneEye, twoEye)

if eyeDist < 5
    % TODO majd ellenorizni
    if strcmp(oneEye.pos, 'top')
        point1 = twoEye.xy(2);
        point2 = twoEye.perimPoint;
    else
        point1 = twoEye.xy(1);
        point2 = twoEye.perimPoint;
    end
else
    if strcmp(oneEye.pos, 'top')
        point1 = oneEye.xy(2);
        point2 = twoEye.xy(1);
    else
        point1 = oneEye.xy(1);
        point2 = twoEye.xy(2);
    end
end

end