
function contrastStrechedImg = function3(grayScaleImg, nu, lambda, nu0)

[h, w] = size(grayScaleImg);

contrastStrechedImg = double(zeros(size(grayScaleImg, 1), size(grayScaleImg, 2)));

grayScaleImg = normalise(grayScaleImg);

for i = 1 : h
    for j = 1 : w
        contrastStrechedImg(i, j) = ...
        calcNewIntensities(lambda, nu, grayScaleImg(i,j), nu0);
    end
end

end

function result = calcNewIntensities(lambda, nu, x, nu0)

result = 1 / ( 1 + (1 - nu0) / nu0 * (((1 - x) / x) * ((nu / (1 - nu)) ^ lambda)));

end