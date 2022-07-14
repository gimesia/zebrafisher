function cmpBinFiltered = binarize4FishEye(fishEnc, thresh)

T = adaptthresh(real(fishEnc), thresh, 'ForegroundPolarity', 'dark');
binFiltered = imbinarize(real(fishEnc), T);

binFiltered = bwareaopen(binFiltered, 10);

% TODO: valami dinamikusra - 5 volt
se = strel('disk', 5);
% imdilate volt
binFiltMod = imdilate(binFiltered, se);
cmpBinFiltered = imcomplement(binFiltMod);
cmpBinFiltered = bwareaopen(cmpBinFiltered, 10);

% figure; imshow(cmpBinFiltered);

end