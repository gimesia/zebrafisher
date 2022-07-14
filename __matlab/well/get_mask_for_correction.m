%% get a mask for the structured pixels (dart regions (vessels and macula)
%% and bright regions (papilla)

function mask = get_mask_for_correction(input)
%

%fprintf('get mask for correcton\n');

bX = double(input(:));
bY = unique(bX);
bN = histc(bX, bY);
bN(1) = [];
bY(1) = [];
bC = cumsum(bN);
bZ = bC/bC(end);

%figure; plot(bY,bN); % histogram
%figure; plot(bY,bC); % cumulative histogram
%figure; plot(bY,bZ); % normalized cumulative histogram (for percentiles)

lowperc = .15;
highperc= .85;

TL = bY(find(bZ < lowperc, 1, 'last'));
TH = bY(find(bZ > highperc, 1, 'first'));

Xmask = zeros(size(input));
Xmask(find(input < TL | input > TH)) = 1;
Xmask2 = bwmorph(Xmask, 'dilate');

%gd = input;
%gd(Xmask2) = 0;
%figure; imshow(gd);

mask = Xmask2;
