function [x1, y1, x2, y2] = getBBoxCoordinates(image)

[actH, actW] = size(image);

% TODO-szar
image = bwareafilt(image, 1);

props = regionprops(image, 'BoundingBox');
x1 = ceil(props.BoundingBox(1));
y1 = ceil(props.BoundingBox(2));
x2 = floor(x1 + props.BoundingBox(3));
y2 = floor(y1 + props.BoundingBox(4));

if actH <= y2
    y2 = y2 - 1; 
end
if actW <= x2
    x2 = x2 - 1;
end

end